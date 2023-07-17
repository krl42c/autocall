FROM python:3.10
WORKDIR /autocall

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD ["python3", "-m", "autocall", "tests/sets/default.yaml"]
