FROM ubuntu:18.04
MAINTAINER Changbeom Choi <cbchoi@handong.edu>

ADD ./sources.list /etc/apt/sources.list
ADD ./requirements.txt /data/

RUN apt update && apt install -y python3 \
	python3-dev \
	python3-pip \
	git

RUN pip3 install -r /data/requirements.txt

WORKDIR /data/tutorsim/tutor_periodic/

VOLUME ["/data/tutorsim","/data/tutorsim/tutor_periodic/assessment", "/data/tutorsim/tutor_periodic/instance"]

ENTRYPOINT ["python3", "/data/tutorsim/tutor_periodic/tutor.py"]	
