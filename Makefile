init: 
	pip3 install -r requirements.txt
	pip3 install . 

test:
	TEST=1 python3 -m pytest tests

coverage:
	TEST=1 coverage run --source=autocall/ -m pytest tests
	coverage html

release: init test coverage
	rm -rf build
	mkdir -p build/dist
	python3 -m build
	mv htmlcov build/coverage
	mv dist/* build/dist/
	
	
	

