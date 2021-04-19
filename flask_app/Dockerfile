FROM pypy:3.7
MAINTAINER glltch@yeah.net
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip3 install  -r requirements.txt
WORKDIR /flask_app
ADD . /flask_app
ENV SPIDER=/flask_app




