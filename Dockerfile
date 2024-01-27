FROM python:3

WORKDIR /drf_api

COPY ./r.txt ./r.txt

RUN pip install -r r.txt

COPY . .