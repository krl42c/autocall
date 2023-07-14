# set up 
set -e 
rm -rf build
mkdir build

# run tests and coverage
pip3 install .
TEST=1 python3 -m pytest tests

TEST=1 coverage run --source=autocall/ -m pytest tests
coverage html

# build the thing
python3 -m build

cp htmlcov/index.html build/coverage.html
cp dist/autocall-0.0.1.tar.gz build/autocall-0.0.1.tar.gz

