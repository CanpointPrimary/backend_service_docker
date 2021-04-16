FROM pypy:3.7

# maintains information
MAINTAINER glltch@yeah.net

ENV PYTHONUNBUFFERED 1

# assign workDIR
WORKDIR /flask_app

# add flask_app
ADD . /flask_app

# using pip install
# RUN apt-get update && apt-get add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt 

ENV SPIDER=/flask_app




