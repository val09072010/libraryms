# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .navigation_labels import NavigationLabels

web = Flask(__name__)
web.config.from_object('config')
db = SQLAlchemy(web)
migrate = Migrate(web, db)

lm = LoginManager(web)
lm.login_view = 'login'

text = NavigationLabels()

from web import views, models, errors, text
