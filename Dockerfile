FROM python:3.5.2
ENV PYTHONUNBUFFERED 1

ARG DEFAULT_REQUIREMENTS
ENV REQUIREMENTS $DEFAULT_REQUIREMENTS

RUN mkdir /interview360
WORKDIR /interview360

ADD ./requirements /interview360/requirements
RUN pip install -r ./requirements/$REQUIREMENTS
ADD . /interview360/
