import os

from flask_project import create_app, setting
app = create_app(os.getenv('FLASK_ENV', 'default'))


if __name__ == '__main__':
    host_ip = setting.HOST_IP
    app.run(host=host_ip)
