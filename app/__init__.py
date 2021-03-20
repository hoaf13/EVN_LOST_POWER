from flask import Flask, render_template, url_for, redirect, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.mod_pages.controllers import mod_pages as pages_module
from app.api.controllers import api as api_module 

app.register_blueprint(pages_module)
app.register_blueprint(api_module)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')




