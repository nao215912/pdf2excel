FROM python:3.9-buster

WORKDIR /usr/src/server
ADD requirements.txt .
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get -y install netcat && apt-get -y install default-jre
