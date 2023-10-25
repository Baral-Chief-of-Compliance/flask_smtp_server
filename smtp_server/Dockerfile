from python:3.9-slim as builder

run mkdir wd
workdir wd

copy . ./

run pip3 install -r requirements.txt

cmd ["python3", "main.py"]
