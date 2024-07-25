from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app=Flask(__name__)
import config
import models
import routes

from models import db

migrate = Migrate(app, db)

if __name__=="__main__":
    app.run(debug=True)
    