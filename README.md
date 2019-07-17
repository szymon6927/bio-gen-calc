# Gene-Calc 

[Gene Calc - Website](https://gene-calc.pl/)

The Gene-Calc is a constantly developed tool dedicated for calculations related to biological sciences, especially focused in field of genetics. Application offers couple of tools such as:
 
- Hardy–Weinberg equilibrium calculator
- Chi-square tests:
    - Independence (Associations) chi-square
- Chi-square goodness of fit test:
    - Estimator of genetic distance
    - Polymorphic information content and heterozygosity calculator


## Stack

- Python 3.6
- Flask
- MySQL

## Local development

1. Create a virtual environment
```
python3 -m venv venv
```

2. Run a virtualenv environment
```
source venv/bin/activate
```

3. Install required packages with dev dependencies
```
pip install -r requirements/dev.txt
```

4. Create `config.env` file by copying `config.env.tmp` and fill these with required environment variables

6. Export local environment variables

On Mac OS
```bash
set -o allexport; source config.env; set +o allexport;
```

In root directory
```
$ mkdir instance
```

and then

```
touch config.py
```

and here is an example config which you can paste into `config.py` file:

```
from os import environ

SECRET_KEY = environ.get('SECRET_KEY', 'secret')

DB_USER = environ.get('DB_USER', 'root')
DB_PASSWORD = environ.get('DB_PASSWORD', '')
DB_NAME = environ.get('DB_NAME', 'gene_calc')
DB_HOST = environ.get('DB_HOST', 'localhost')

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
flask db migrate
```

Next import data into your local database:
```
$ mysql -u root gene_calc < fixtures/data.sql
```

To start application locally type:
```
flask run
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