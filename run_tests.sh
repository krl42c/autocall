if [[ -z "{INSTALL_PKG}" ]]; then
    pip3 install -e .
fi
cd tests/test_server/
./start.sh  &
cd ../../
pytest tests

# clean
kill $(lsof -t -i:8000)

