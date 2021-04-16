import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_project import create_app, db

app = create_app('develop')
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':

    manager.run()
