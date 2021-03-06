import os
import sys
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(
    sys.modules['__main__'].__file__)))

__version__ = '0.5'


setup(
    name="extrapypi",
    version=__version__,
    description='pypi server built on flask, aimed to be an extra index\
    for private dependencies, including basic permissions',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    url='https://github.com/karec/extrapypi',
    download_url="https://github.com/karec/extrapypi/releases",
    author='karec',
    author_email='manu.valette@gmail.com',
    license='MIT',
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='web flask pypi',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.11',
        'SQLAlchemy==1.3.22',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-Login',
        'WTForms==2.3.3',
        'Flask-WTF==0.14.3',
        'Flask-Principal',
        'passlib',
        'blinker',
        'docutils',
        'pkginfo',
        'boto3==1.17.3'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'tests': ['pytest', 'pytest-flask'],
        'docs': ['sphinx']
    },
    entry_points={
        'console_scripts': [
            'extrapypi = extrapypi.manage:cli'
        ]
    }
)
