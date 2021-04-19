import os

"""
set global variable
"""
FLASK_HOST = '0.0.0.0'
FLASK_PORT = '8000'
HOST_IP = os.getenv('FLASK_HOST', FLASK_HOST)
