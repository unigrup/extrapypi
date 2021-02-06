Generic single-database configuration.

## Creation of new database migration

In order to update the database schema a new version/migration has to be created.

From the root of the project run: 

### Step 1
In case you are using custom values (the values you put in your custom configuration file). You have to export this configuration
in order to correctly connect to the db
(execute only in case you have custom configuration, otherwise go directly to step 2)
```sh
export EXTRAPYPI_CONFIG=config.cfg
```

### Step 2
To create new migration just run:
```sh 
FLASK_APP=extrapypi.wsgi:app flask db migrate -m "migration name here"
```
Once the command finishes at migration directory under the versions' folder you fill find the new da schema.


### Step 3
Now just update the database by running: 
```sh 
FLASK_APP=extrapypi.wsgi:app flask db upgrade
```
