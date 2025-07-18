#!/usr/bin/env python3
"""
Production Flask app for Render.com deployment
Connects to EC2 backend API and AWS RDS database
"""

import logging
import os

from flask import Flask, flash, jsonify, redirect, render_template, session, url_for
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Import your existing modules
from config import Config
from ec2_api_client import EC2APIClient
from forms import LoginForm, RegistrationForm
from models import User

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)


class ProductionConfig(Config):
    """Production configuration with environment variables"""

    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "fallback-secret-key-change-in-production"
    )

    # EC2 Backend API URL
    EC2_API_URL = os.environ.get(
        "EC2_API_URL", "http://ec2-54-221-34-34.compute-1.amazonaws.com:5000"
    )

    # Database config (if using RDS directly)
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Other production settings
    DEBUG = False
    TESTING = False


app.config.from_object(ProductionConfig)

# Enable CORS for API calls
CORS(
    app,
    origins=[
        "https://*.onrender.com",
        "http://ec2-54-221-34-34.compute-1.amazonaws.com:5000",
    ],
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Initialize API client
api_client = EC2APIClient(app.config["EC2_API_URL"])


@login_manager.user_loader
def load_user(user_id):
    """Load user from session data"""
    try:
        # Check if user data exists in session
        if (
            "user_id" in session
            and "username" in session
            and str(session["user_id"]) == str(user_id)
        ):

            # Create User object from session data
            user = User(
                id=session["user_id"],
                username=session["username"],
                role=session.get("user_role", "freelancer"),
            )
            return user
        return None
    except Exception as e:
        logger.error(f"User loader error: {e}")
        return None


@app.route("/")
def index():
    """Homepage"""
    user_data = current_user if current_user.is_authenticated else None
    return render_template("index.html", user=user_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    form = LoginForm()

    if form.validate_on_submit():
        # Try to authenticate with EC2 backend using username
        try:
            user_data = api_client.login(form.username.data, form.password.data)

            if user_data and user_data.get("token"):
                # Store user session data for Flask-Login
                session["user_id"] = user_data["user_id"]
                session["username"] = user_data["username"]
                session["user_role"] = user_data.get("role", "freelancer")
                session["auth_token"] = user_data["token"]

                # Create user object and login
                user = User(
                    id=user_data["user_id"],
                    username=user_data["username"],
                    role=user_data.get("role", "freelancer"),
                )
                login_user(user)

                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password", "error")
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash("Login failed. Please try again.", "error")

    return render_template("auth/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page"""
    form = RegistrationForm()

    if form.validate_on_submit():
        # Try to register with EC2 backend
        try:
            response = api_client.register(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                role=form.user_type.data,
            )

            success_msg = "User registered successfully"
            if response and response.get("message") == success_msg:
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))
            else:
                error_msg = response.get("error", "Registration failed")
                flash(error_msg, "error")
        except Exception as e:
            logger.error(f"Registration error: {e}")
            flash("Registration failed. Please try again.", "error")

    return render_template("auth/register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard"""
    user_type = session.get("user_role", "freelancer")

    try:
        dashboard_data = api_client.get_user_dashboard(session["user_id"])

        if user_type == "freelancer":
            return render_template(
                "freelancer/dashboard.html",
                user=current_user,
                freelancer=dashboard_data.get("freelancer"),
                bids=dashboard_data.get("bids", []),
                active_projects=dashboard_data.get("active_projects", 0),
                completed_projects=dashboard_data.get("completed_projects", 0),
                success_rate=dashboard_data.get("success_rate", 0),
                matching_posts=dashboard_data.get("matching_posts", []),
            )
        else:
            return render_template(
                "client/dashboard.html",
                user=current_user,
                client=dashboard_data.get("client"),
                posts=dashboard_data.get("posts", []),
                new_bids=dashboard_data.get("new_bids", 0),
                assigned_projects=dashboard_data.get("assigned_projects", 0),
            )
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        flash("Error loading dashboard", "error")
        return redirect(url_for("index"))


@app.route("/browse_posts")
@login_required
def browse_posts():
    """Browse available posts"""
    try:
        posts = api_client.get_posts()
        return render_template(
            "posts/browse.html",
            title="Browse Posts",
            posts=posts,
            pagination=None,
            form=None,
            keywords="",
            search_filters={},
            current_filters={},
            domains=[],
        )
    except Exception as e:
        logger.error(f"Browse posts error: {e}")
        flash("Error loading posts", "error")
        return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    user_data = current_user if current_user.is_authenticated else None
    return render_template("errors/404.html", user=user_data), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    user_data = current_user if current_user.is_authenticated else None
    return render_template("errors/500.html", user=user_data), 500


# Health check for Render
@app.route("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Check if API is reachable
        api_health = api_client.health_check()
        return jsonify(
            {
                "status": "healthy",
                "service": "gigfusion-frontend",
                "api_status": api_health,
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "service": "gigfusion-frontend",
                    "error": str(e),
                }
            ),
            500,
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
