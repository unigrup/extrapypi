"""Storage package

This package groups all storage "drivers" that can be used by extrapypi as a storage backend.
Using custom classes to handle storage make us be more flexible in this task, allowing to use
the storage of our choice (local file, cloud storage, etc.).

For more control we provide a base class for drivers.
"""
from .local import LocalStorage
from .aws_s3 import AwsS3Storage

__all__ = [
    'LocalStorage',
    'AwsS3Storage'
]
