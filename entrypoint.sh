#!/bin/bash

./wait-for-it.sh database:3306
flask db upgrade
flask run --host=0.0.0.0
