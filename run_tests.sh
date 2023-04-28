pip3 install -e .

cd tests/test_server/
./start.sh  &
cd ../../
pytest tests

# clean
kill $(lsof -t -i:8000)
