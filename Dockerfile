FROM python:3.8

WORKDIR /home

RUN pip install -U pip requests
COPY *.py ./

ARG api_key
ARG biz_1
ARG biz_2

ENV API_KEY $api_key
ENV BIZ1 $biz_1
ENV BIZ2 $biz_2

ENTRYPOINT ["python", "server.py"]

