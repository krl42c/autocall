#!/bin/sh
TEST=1 coverage run --source=autocall/ -m pytest tests
coverage html
open htmlcov/index.html
