# Powertrain

Powertrain is a system designed to manage and execute large-scale neuroimaging projects across [VUIIS][vuiis].

It is currently in the planning stages. Documentation can be found [here][rtfd]

## Who

Powertrain is supported by [VUIIS][vuiis]. The following people are involved:

* Scott Burns
* Brian Boyd
* Benjamin Yvernault
* Kevin Wilson
* Stephen Damon
* Adam Anderson
* Bennett Landman

## Dev environment

Where possible, we try to follow [12 Factor Application](http://12factor.net) principles including:

* Explicit dependencies (see the `req` folder)
* Config in the environment
* Development/production parity

Powertrain will most likely be built upon:

* [Flask](http://flask.pocoo.org), a minimal web framework for python.
* [SQLAlchemy](http://www.sqlalchemy.org), the database toolkit for python.
* [Postgres](http://postgresql.org), the worlds most advanced open source database.

### Setting up the virtual environment

You should use a [virtualenv](https://virtualenv.pypa.io/en/latest/) & [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to setup your environment. After setting up these tools, make a virtual environment like so:

```bash
$ mkvirtualenv powertrain
$ workon powertrain
$ git clone https://github.com/VUIIS/powertrain powertrain
$ cd powertrain && pip install -r reqs/dev.txt
```
### Environment variables

Powertrain honors the following envvars:

* `SECRET_KEY`: used by Flask all over the place, notably secure cookies
* `FLASK_CONFIG`: see `config.config`. String describing config environment
* `MAIL_SERVER`: SMTP server
* `MAIL_PORT`: SMTP server port
* `MAIL_USERNAME`: username for mail server
* `MAIL_PASSWORD`: SMTP password
* `DEV_DATABASE_URL`: database url for development purposes
* `TEST_DATABASE_URL`: database url for testing purposes
* `ADMIN`: email account that has administrator rights
* `FLASK_COVERAGE`: `./manage.py test` will display coverage report after finishing unittests.

### Postgres

Powertrain uses Postgres under the hood. On OS X, download & start [Postgres.app](http://postgresapp.com). When Postgres.app is running, a fully-featured Postgres 9.3 (at the time of this writing) server is running on the system. When you quit, the server is not running. With the server running, make a development & testing database.

On Linux, use your package manager of choice to install postgres. Then:

```bash
$ createdb -E utf-8 -U `whoami` powertrain
$ createdb -E utf-8 -U `whoami` powertrain_testing
$ export DEV_DATABASE_URL=postgres://`whoami`@localhost/powertrain
$ export TEST_DATABASE_URL=postgres://`whoami`@localhost/powertrain_testing
```


Powertrain uses [Alembic](http://alembic.readthedocs.org/en/latest/) and [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/) for schema migrations. To update your dev database after a new migration:

```bash
$ ./manage.py db upgrade
```

To generate a new migration (when models change):

```bash
$ ./manage.py db migrate
```

This will create a new migration in `migrations/versions` that **must be reviewed** before placed into source-control.

### Testing

```bash
$ export FLASK_COVERAGE=1; make test
```

Run it early, run it often.

[vuiis]: http://vuiis.vanderbilt.edu
[rtfd]: http://powertrain.rtfd.org
