#python version
FROM pypy:3.7

# maintainer information
MAINTAINER glltch@yeah.net

# specify working directory
WORKDIR /flask_app

# copy requirements.txt to flask_app directory
COPY requirements.txt /flask_app

# install dependencies
RUN pip3 install  -r requirements.txt

# copy the command to the current directory
COPY . /flask_app

# specify python enviroment variables
ENV PYTHONUNBUFFERED 1
ENV SPIDER=/flask_app




