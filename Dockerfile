FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y libmagic1

RUN mkdir -p /usr/src/app

WORKDIR /usr/src

COPY requirements.txt /usr/src

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

WORKDIR /usr/src/app/src

EXPOSE 443
EXPOSE 800
