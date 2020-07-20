import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.payment.models import db

app = create_app(os.getenv("APP_SETTINGS", "config.Config"))


manager = Manager(app)
manager.add_command("db", MigrateCommand)
migrate = Migrate(app, db)

if __name__ == "__main__":
    manager.run()

