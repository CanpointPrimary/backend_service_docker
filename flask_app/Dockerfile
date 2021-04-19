FROM pypy:3.7

# maintains information
MAINTAINER glltch@yeah.net

ENV PYTHONUNBUFFERED 1

# assign workDIR
WORKDIR /flask_app
COPY requirements.txt .
RUN pip3 install --quiet -r requirements.txt
# add flask_app
ADD . /flask_app

ENV SPIDER=/flask_app




