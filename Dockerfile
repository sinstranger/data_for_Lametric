FROM python:3.8

WORKDIR /home

RUN pip install -U pip requests
COPY *.py ./

ENTRYPOINT ["python", "server.py"]

