if [[ -z "$INSTALL" ]]; then
    pip3 install -e .
fi
cd tests/test_server/
./start.sh > stdout 2>&1 & 
cd ../../
python3 -m pytest tests

# clean
kill $(lsof -t -i:8000)
echo Tests completed
