import os
from flask import Flask
from app.routes import routes

def create_app():
    """Factory function to initialize and configure the Flask app."""
    app = Flask(__name__, template_folder='../templates')  # Explicitly set templates folder

    # Application Configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Use environment variable for the secret key
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')  # Use environment variable for uploads directory
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # Max upload size (default: 16 MB)

    # Register the blueprint
    app.register_blueprint(routes)

    return app
