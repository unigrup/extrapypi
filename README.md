# extrapypi

[![Build Status](https://travis-ci.org/karec/extrapypi.svg?branch=master)](https://travis-ci.org/karec/extrapypi)
[![Coverage Status](https://coveralls.io/repos/github/karec/extrapypi/badge.svg?branch=master)](https://coveralls.io/github/karec/extrapypi?branch=master)
[![Documentation Status](https://readthedocs.org/projects/extrapypi/badge/?version=latest)](http://extrapypi.readthedocs.io/en/latest/?badge=latest)

External pypi server with web ui and basics permissions management

extrapypi don't mirror official pypi packages, and will not. It's just not build with 
this goal in mind.
extrapypi is just here to provide you an extra index to upload and install private packages
simply.


* [Installation](#installation)
* [Deployment](#deployment)
* [Usage](#usage)

Little preview

![demo image](docs/images/demo.gif)

## Features

* Upload packages from twine / setuptools
* Install packages with pip using only extra-index option
* Basics permissions management using roles (currently admin, developer, maitainer, installer)
* Easy deployment / installation using the WSGI server you want
* MySQL, PostgresSQL and SQLite support and tested
* Extensible storage system
* CLI tools to help you deploy / init / test extrapypi
* Basic dashboard to visualize packages and users
* Codebase aim to be simple and hackable

## Roadmap

Features that we want to implement for future releases :

* interface for pip search
* prefix management

## Installation

You can install extrapypi with pip

```bash
pip install extrapypi
```

Or from source 

```bash
python setup.py install
```

**NOTE** if you want to use anything else than sqlite, you must download appropriate drivers (like psycopg2 for postgres)

## Deployment

First thing, you will need to create a configuration file for your extrapypi. We provide 
a cli command to generate a sample :

```bash
extrapypi start --filename myconfig.cfg
```

This command will create a file named `myconfig.cfg` in your current directory with the following content 

```python
"""Sample configuration
"""

# Database connexion string
SQLALCHEMY_DATABASE_URI = "sqlite:///extrapypi.db"

# Update this secret key for production !
SECRET_KEY = "changeit"

# Storage settings
# You need to update at least packages_root setting
STORAGE_PARAMS = {
    'packages_root': "/path/to/my/packages"
}

```

Once you've updated your configuration, you will need to init database 

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi init
```

Note that you can also export `EXTRAPYPI_CONFIG` variable

This will create tables and two users : 

* an admin with login and password set to `admin`
* an install with login and password set to `pip`

You can check full `init` usage in documentation.


Here we are, you can now run extrapypi

For testing purpose 

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi run
```

With gunicorn

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg gunicorn extrapypi.wsgi:app
```

with uwsgi

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg uwsgi --http 0.0.0.0:8000 --module extrapypi.wsgi:app
```

Once done, you can access the dashboard at the following address :

`http://mydomainorip:8000/dashboard`

You can see full examples for deploying extrapypi in production in the documentation

### Run as a service (Ubuntu 20.04)
In this example we are going to run extrapypi as a service. So extrapypi will be initialized automatically on start/reboot.
##### Step 1 - clone the repo
```sh 
git clone https://github.com/karec/extrapypi.git
```
##### Step 2 - Enter inside extrapypi folder 
```sh
cd extrapypi 
```
##### Step 3 - Create virtual environment
```sh
python3 -m venv venv 
```
##### Step 4 - activate vistual environmet
```sh 
source ./venv/bin/activate
```
##### Step 5 - Install extrapypi 
```sh 
python setup.py install
```
##### Step 6 install uwsgi
```sh 
pip3 install uwsgi
```
##### Step 7 - Create configuration file
```sh
extrapypi start --filename myconfig.cfg
```
##### Step 8 - Update value from myconfig.cfg
In this step we want to adapt the values from myconfig.cfg to adap them to our needs.
##### Step 9 - Init database
```sh 
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi init
```
##### Step 10 - Create a file that will load the service configuration 
```sh 
nano /lib/systemd/system/extrapypi.service
```
Now a service definition is created.
Make sure to change path-project-files, path-to-file and path-to-env to your paths.

```sh 
[Unit]
Description=uWSGI instance to serve extrapypi
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/path-project-files/extrapypi
Environment="EXTRAPYPI_CONFIG=/path-to-file/myconfig.cfg"
ExecStart=/path-to-env/venv/bin/uwsgi --http 0.0.0.0:8000 --module extrapypi.wsgi:app

[Install]
WantedBy=multi-user.target
```

##### Step 11 - enable extrapypi service
```sh 
sudo systemctl enable extrapypi
```

##### Step 12 - Start extrapypi service
```sh 
sudo systemctl start extrapyp
```

##### Step 13 - Check extrapypi service status
```sh 
sudo systemctl status extrapyp
```

##### Step 14 - Go to url
Open a browser and type: http://your-ip:8000/dashboard/

Example:
* http://192.168.1.14:8000/dashboard/
* http://127.0.0.1:8000/dashboard/

Every time you change extrapypi.service file, you will need to reload the configuration again and restart the service:
```sh 
systemctl daemon-reload
```
```sh 
systemctl restart extrapypi
```

To check service logs:
```sh 
journalctl -u extrapypi
```

### Run with nginx (Ubuntu 20.04)
In this example configuration we are going to run extrapypi behind nginx web server.

##### Step 1 - Update/adapt extrapypi service

Make sure to change path-project-files, path-to-file, path-to-env and path-to-scket to your paths.

```sh 
nano /lib/systemd/system/extrapypi.service
```

```sh 
[Unit]
Description=uWSGI instance to serve extrapypi
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/path-project-files/extrapypi
Environment="EXTRAPYPI_CONFIG=/path-to-file/myconfig.cfg"
ExecStart=/path-to-env/venv/bin/uwsgi --master --http 0.0.0.0:8000 --module extrapypi.wsgi:app --socket /path-to-scket/extrapypi.sock --chmod-socket=666 --vacuum --die-on-term


[Install]
WantedBy=multi-user.target
```
Reload new configuration
```sh 
systemctl daemon-reload
```
Restart service
```sh 
systemctl restart extrapypi
```


##### Step 2 - Install nginx
```sh 
apt install nginx
```

##### Step 3 - Edit nginx configuration
In this case we are going to edit the default configuration to serve extrapypi
```sh 
nano /etc/nginx/sites-available/default
```

Make sure to change your-domain and path-to-socket to your stuff!
```sh 
server {
        listen 80;
        server_name your-domain;
        location / {
                include uwsgi_params;
                uwsgi_pass unix:/path-to-socket/extrapypi.sock;
        }
}

```
##### Step 4 - Check configuration file for errors
After saving the changes we check the configuration file for errors:
```sh 
nginx -t
```

##### Step 5 - Restart nginx 
Once we make sure that the configuration file does not have any errors, we restart the service: 
```sh 
systemctl restart nginx
```

To check the status of nginx service:
```sh 
systemctl status nginx
```

In case of errors we can consult nginx error logs:
```sh 
less /var/log/nginx/error.log
```

##### Step 6 - Go to url
Open a browser and type: http://your-domain/dashboard/

Example:
* http://example.com/dashboard/
* http://192.168.1.14/dashboard/


**WARNING** since extrapypi use basic auth, we strongly advise to run it behind a reverse proxy (like nginx) and use 
https

## Usage


### Uploading packages

extrapypi is compliant with setuptools / twine, you just need to update your `.pypirc` like this

```
[distutils]
index-servers =
    local

[local]
username=admin
password=admin
repository=http://127.0.0.1:5000/simple/
```

And then you can run

```bash
python setup.py bdist_wheel upload -r local
```

Or using twine

```bash
twine upload -r local dist/extra_pypi-0.1-py3.5.egg
```

### Installing packages with pip

extrapypi is built to be used as an extra index, so you can simply run :

```bash
pip install extrapypi --extra-index-url http://user:password@mypypiurl.org/simple/ 
```

or directly updating your `pip.conf` file 

```bash
[global]
extra-index-url = http://user:password@mypypiurl.org/simple/
```


## Development

Install main package

```
python setup.py install
```

Then you can use included cli to setup your env

```
extrapypi init
extrapypi run
```

### Running server

extrapypi use flask cli, `extrapypi` command is only a hook to `extrapypi.manage` that include several commands 
but anything present in flask script can be used for extrapypi too.

For exemple you can start application using `flask run` with debug on like this :

```
FLASK_DEBUG=1 flask run
```

### Running test


First install tox

```
pip install tox
```

Then you can just run 

```
tox -e sqlite
```

You can also run tox in all envs if needed


### Docker
In case you want to run in inside docker
#### Build docker
```sh 
docker build -t extrapypi .
```

#### Run docker
default configuration 
```sh 
docker run -p 80:80 -t extrapypi:latest
```
