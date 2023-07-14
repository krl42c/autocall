init: 
	pip3 install -r requirements.txt

test:
	TEST=1 python3 -m pytest tests

coverage:
	TEST=1 coverage run --source=autocall/ -m pytest tests
	coverage html
