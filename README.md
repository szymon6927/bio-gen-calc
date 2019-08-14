# Gene-Calc

[Gene Calc - Website](https://gene-calc.pl/)

The Gene-Calc is a constantly developed tool dedicated for calculations related to biological sciences, especially focused in field of genetics. Application offers couple of tools such as:

- Hardy–Weinberg equilibrium calculator
- Chi-square tests:
    - Independence (Associations) chi-square
- Chi-square goodness of fit test:
    - Estimator of genetic distance
    - Polymorphic information content and heterozygosity calculator
- Polymorphic information content & Heterozygosity
- Estimation of genetic distance
- Sequences Analysis Tools
    - Dot plot
    - Tool to obtain consensus sequence
    - Additional tools


## Stack

- Python 3.7
- Flask
- MySQL 5.7
- Docker & Docker Compose


## Prerequisites

Make sure you have installed all of the following prerequisites on your development machine:

- [GIT](https://git-scm.com/downloads)
- [Make](http://gnuwin32.sourceforge.net/packages/make.htm)
- [Python 3.7](https://www.python.org/downloads/)
- [Docker version >= 19.03.1](https://www.docker.com/get-started)
- [docker-compose version >= 1.24.1](https://docs.docker.com/compose/install/)

If you don't want to use Docker you have to install:
- [MySQL 5.7](https://dev.mysql.com/downloads/mysql/5.7.html)


## Local development [virtualenv]

Create a virtual environment
```
$ python3 -m venv venv
```

Run a virtualenv environment
```
$ source venv/bin/activate
```

Install required packages with dev dependencies
```
$ pip install -r requirements/dev.txt
```

If you have problems with installation `mysqlclient` package with the above command.
Try to install it by hand with `pip install mysqlclient`

Create `config.env` file by copying `config.env.tmp` and fill these with required environment variables

Export local environment variables

On Mac OS
```bash
$ set -o allexport; source config.env; set +o allexport;
```

In root directory
```
$ mkdir instance
```

and then

```
$ touch config.py
```

and here is an example config which you can paste into `config.py` file:

```
from os import environ

SECRET_KEY = environ.get('SECRET_KEY', 'secret')

DB_USER = environ.get('DB_USER', 'root')
DB_PASSWORD = environ.get('DB_PASSWORD', '')
DB_NAME = environ.get('DB_NAME', 'gene_calc')
DB_HOST = environ.get('DB_HOST', 'localhost')

MYSQL_DATABASE = environ.get('MYSQL_DATABASE')
MYSQL_USER = environ.get('MYSQL_USER')
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')

USE_DOCKER = int(environ.get('DOCKER', 0))

if USE_DOCKER == 1:
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@database/{MYSQL_DATABASE}'
else:
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
```

In your local MySQL database
```
$ mysql -u root
$ CREATE DATABASE gene_calc;
$ exit
```

Apply application migrations:
```
$ flask db migrate
```

Next import data into your local database:
```
$ mysql -u root gene_calc < fixtures/data.sql
```

To start application locally type:
```
$ flask run
```

Application should be available under URL:
```
http://127.0.0.1:5000
```

To login into userpanel
```
Login: test123
Password: test123test123
```

#### Important info

If you want to run tests without docker you have to physically install a few tools:
- [wkhtmltopdf](https://wkhtmltopdf.org/)
- [muscle](https://www.drive5.com/muscle/manual/install.html)

without this tools it is impossible to correctly run the tests


## Local development [docker]

To start local development using docker:

Export local environment variables

On Mac OS
```bash
$ set -o allexport; source config.env; set +o allexport;
```

Start local containers:
```
$ docker-compose -f docker-compose.local.yml up
```

Load data into docker container
```
$ docker exec -i database mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < fixtures/data.sql
```

Docker hints:
```
Rebuild containers:
$ docker-compose -f docker-compose.local.yml up --build

Stop containers:
$ docker-compose -f docker-compose.local.yml down

Stop containers with volume delete:
$ docker-compose -f docker-compose.local.yml down -v
```

Application should be available under URL:
```
http://127.0.0.1:5000
```

To login into userpanel
```
Login: test123
Password: test123test123
```

## Env variables

If you want to start local development by docker you have to remember to correctly set up env variables in `config.env`
```
DOCKER=1
```

In case local development by `virtualenv`
```
DOCKER=0
```

## Tests

To run tests via docker-compose type:
```
docker-compose -f docker-compose.local.yml exec backend pytest -v
```

If you want to run the tests without docker you have to install dependencies which I have mentioned before in section
`Local development [virtualenv]` then in root app directory type:
```
pytest -v
```

## Pre-commit config

We use a pre-commit hook which checking a quality of code.
To install a hook on your local repository, you have to run a command given below, after install required packages:

```
$ pre-commit install
```

## Makefile

We use Makefile to automate some common stuff

If you want to update dependencies type:
```
$ make update-deps
```

If you want to format code type:
```
$ make format
```

## Git flow

Create your feature branch from master.

Branch naming:
- pattern: trello-task_id-short-description
- eg: trello-20-remove-flask-admin

Commit names conventions:
- pattern. [trello-task_id]: commit description
- eg. [trello-20]: Removed flask-admin package

After finishing implementation of your feature - create pull request to master branch.


### Theoretical information available from:

[https://gene-calc.pl/about](https://gene-calc.pl/about)


### Authors

[Szymon Miks](https://szymonmiks.pl) & [Jan Bińkowski](https://www.linkedin.com/in/jan-bi%C5%84kowski-a16b99141/)

#### License

This project is licensed under the GNU GPL License

#### Moreover

If you have any questions or ideas how to develop this app, please let us know via e-mail: contact@gene-calc.pl
