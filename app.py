from flask import Flask, render_template

from flask_login import LoginManager

from config import Config

from models.models import (
    db,
    Recruiter
)

from routes.recruiter_routes import register_routes
from routes.student_routes import student_bp
from routes.interview_routes import interview_bp
from routes.technical_prep_routes import technical_prep_bp
from routes.technical_routes import technical_bp
from routes.analytics_routes import analytics_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


# =========================================
# LOGIN MANAGER
# =========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "home"


@login_manager.user_loader
def load_user(user_id):

    return Recruiter.query.get(int(user_id))


# =========================================
# REGISTER ROUTES
# =========================================

register_routes(app)

app.register_blueprint(student_bp)

app.register_blueprint(interview_bp)

app.register_blueprint(technical_prep_bp)
app.register_blueprint(technical_bp)
app.register_blueprint(analytics_bp)


# =========================================
# CREATE DATABASE TABLES
# =========================================

with app.app_context():

    db.create_all()


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
