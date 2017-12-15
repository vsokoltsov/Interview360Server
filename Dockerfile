FROM python:3.5.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /interview360
WORKDIR /interview360
ADD requirements.txt /interview360/
RUN pip install -r requirements.txt
ADD . /interview360/
