FROM ubuntu:18.04
MAINTAINER Changbeom Choi <cbchoi@handong.edu>

ADD ./sources.list /etc/apt/sources.list

RUN apt update && apt install -y python3 \
	python3-dev \
	python3-pip \
	git

WORKDIR /data
RUN git clone http://github.com/cbchoi/tutorsim.git

WORKDIR /data/tutorsim
RUN git pull
RUN pip3 install -r /data/tutorsim/telegrambot/requirements.txt

VOLUME ["/data", "/data/tutorsim/telegrambot/instance"]

ENTRYPOINT ["python3", "/data/tutorsim/telegrambot/tutorsim_bot.py"]	
