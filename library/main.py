import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import app_config


config_name = os.getenv('FLASK_ENV', 'default')

app = Flask(__name__)
# app.config.from_object(Config)
app.config.from_object(app_config[config_name])
db = SQLAlchemy(app)



migrate = Migrate(app, db, render_as_batch=True) # obj for db migrations
CORS(app)

# from library import models, resources
import library.resources as resources

with app.app_context():
    db.create_all()
    db.session.commit()