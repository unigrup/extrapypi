"""
AwsS3Storage
------------

Simple Amazon webservices S3 storage that create directories for packages and
put releases files in it.
"""
import os
import re
import pathlib

import boto3

from .base import BaseStorage
import pkginfo
from hashlib import md5
import io


class AwsS3Storage(BaseStorage):
    NAME = 'AwsS3Storage'

    def __init__(self, access_key=None, secret_key=None, bucket=None):

        if access_key is None:
            raise RuntimeError("Cannot use AwsS3Storage without access_key set. Please configure STORAGE_PARAMS")
        if secret_key is None:
            raise RuntimeError("Cannot use AwsS3Storage without secret_key set. Please configure STORAGE_PARAMS")
        if bucket is None:
            raise RuntimeError("Cannot use AwsS3Storage without bucket set. Please configure STORAGE_PARAMS")

        self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket = bucket

    def _get_metadata(self, release):
        path = os.path.join(str(pathlib.Path().absolute()), release.split('/')[1])
        self.s3.download_file(Filename=path, Bucket=self.bucket, Key=release)

        try:
            metadata = pkginfo.get_metadata(path).__dict__
        except Exception:  # bad archive
            metadata = {}

        md5_hash = md5()

        with open(path, 'rb') as fp:
            for content in iter(lambda: fp.read(io.DEFAULT_BUFFER_SIZE), b''):
                md5_hash.update(content)  # pragma: no cover

        metadata.update({'md5_digest': md5_hash.hexdigest()})

        os.remove(path)
        return metadata

    def get_releases_metadata(self):
        response = self.s3.list_objects(Bucket=self.bucket)
        for content in response.get('Contents', []):
            if content.get('Key').split('/')[1] != '':  # Ex: ['package_name', 'file_name']
                yield content.get('Key').split('/')[0], self._get_metadata(content.get('Key'))

    def delete_package(self, package):
        """
        Delete entire package directory
        """
        try:
            response = self.s3.list_objects(Bucket=self.bucket, Prefix=package.name)
            for content in response.get('Contents', []):
                self.s3.delete_object(Bucket=self.bucket, Key=content.get('Key'))
            return True
        except Exception as e:
            print(e)
            return False

    def delete_release(self, package, version):
        """
        Delete all files matching specified version
        """
        try:
            response = self.s3.list_objects(Bucket=self.bucket, Prefix=package.name)
            for content in response.get('Contents', []):
                if version in content.get('Key'):
                    self.s3.delete_object(Bucket=self.bucket, Key=content.get('Key'))
            return True
        except Exception:
            return False

    def create_package(self, package):
        """
        Create new directory for a given package
        """
        try:
            self.s3.put_object(Bucket=self.bucket, Key=(package.name + '/'))
            return True
        except Exception:
            return False

    def create_release(self, package, release_file):
        """
        Copy release file inside package directory
        """
        try:
            self.s3.put_object(Bucket=self.bucket, Body=release_file.stream,
                               Key=package.name + '/' + release_file.filename)
            return True
        except Exception:
            return False

    def get_files(self, package, release=None):
        """Get all files associated to a package

        If release is not None, it will filter files on release version,
        based on a regex
        """
        files = []
        response = self.s3.list_objects(Bucket=self.bucket, Prefix=package.name)
        for content in response.get('Contents', []):
            files.append(content.get('Key').split('/')[1])

        if release is not None:
            regex = '.*-(?P<version>[0-9\.]*)[\.-].*'.format(package.name)
            r = re.compile(regex)
            v = release.version

            files = filter(
                lambda f: r.match(f) and r.match(f).group('version') == v,
                files
            )
            files = list(files)

        return files

    def get_file(self, package, file, release=None):
        """
        Get a single file from filesystem
        """
        file = self.s3.get_object(Bucket=self.bucket, Key=os.path.join(package.name, file))
        file_content = file['Body']
        return file_content
