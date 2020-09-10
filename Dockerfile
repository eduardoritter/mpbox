FROM ubuntu:16.04

MAINTAINER Your Name "eduardoritter@gmail.com"

FROM python:3

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose
EXPOSE  5000

# Run
CMD [ "python", "./run.py" ]
