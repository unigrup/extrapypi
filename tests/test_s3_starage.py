import os

from moto import mock_s3
import pytest

from extrapypi.models import Package
from extrapypi.storage import AwsS3Storage


def bucket_name():
    return "my-test-bucket"


@mock_s3
def test_list_buckets(app, db, s3_client, werkzeug_file, tmpdir):

    with pytest.raises(RuntimeError):
        AwsS3Storage()

    with pytest.raises(RuntimeError):
        AwsS3Storage(access_key=os.environ["AWS_ACCESS_KEY_ID"])

    with pytest.raises(RuntimeError):
        AwsS3Storage(access_key=os.environ["AWS_ACCESS_KEY_ID"], secret_key=os.environ["AWS_SECRET_ACCESS_KEY"])

    with pytest.raises(RuntimeError):
        AwsS3Storage(access_key=os.environ["AWS_ACCESS_KEY_ID"], bucket=bucket_name())

    package = db.session.query(Package).first()
    s3_client.create_bucket(Bucket=bucket_name())

    ls = AwsS3Storage(access_key=os.environ["AWS_ACCESS_KEY_ID"], secret_key=os.environ["AWS_SECRET_ACCESS_KEY"], bucket=bucket_name())

    status = ls.create_package(package)
    body = s3_client.list_objects(Bucket=bucket_name(), Prefix=package.name)['Contents'][0]['Key']
    assert body == 'unknow-package/'
    assert status is True

    assert isinstance(ls.get_files(package), list)
    assert len(ls.get_files(package)) == 1

    assert ls.create_release(package, werkzeug_file) is True
    assert len(ls.get_files(package, package.releases[0])) == 1

    s3_client.put_object(Bucket=bucket_name(), Body=werkzeug_file.stream, Key=package.name + '/' + werkzeug_file.filename)

    # test get releases metadata
    metadata = list(ls.get_releases_metadata())
    for path, meta in metadata:
        assert 'unknow-package' in path
        assert 'md5_digest' in meta

    f = ls.get_file(package, "test-0.1.tar.gz")
    assert f is not None
    assert ls.delete_release(package, '0.1') is True
    assert ls.delete_package(package) is True

    # bad data
    assert ls.create_package(None) is False
    assert ls.create_release(None, werkzeug_file) is False
    assert ls.delete_release(None, '0.1') is False
    assert ls.delete_package(None) is False
    assert ls.get_files(Package(name='new-test')) == []


