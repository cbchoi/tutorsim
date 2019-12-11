FROM ubuntu:18.04
MAINTAINER Changbeom Choi <cbchoi@handong.edu>

ADD ./sources.list /etc/apt/sources.list
ADD ./requirements.txt /data/
ADD ./run.script /data/
ADD ./init.script /data/

RUN apt update && apt install -y python3 \
	python3-dev \
	python3-pip \
	git

RUN chmod +x /data/run.script
RUN chmod +x /data/init.script

WORKDIR /data/

RUN pip3 install -r /data/requirements.txt
RUN /data/init.script

VOLUME ["/home/cbchoi/Service/tutorsimbot.instance/instance", "/data/tutorsim/telegrambot/instance"]

