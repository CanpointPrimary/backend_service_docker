#!/bin.bash
python app.py db init&&
python app.py db migrate&&
python app.py db upgrade&&
python app.py runserver&&
gunicorn flask_app.wsgi:application -c gunicorn.conf
