from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions (these must exist before create_app)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Create Flask application
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Login settings
    login_manager.login_view = "auth.login"   # if route is /auth/login
    login_manager.login_message_category = "info"

    # Import and register blueprints
    from .auth import auth_bp
    from .main import main_bp
    from .payments import payments_bp
    from .admin_ui import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(admin_bp)  # URL prefix is inside admin_bp

    # Inject global template variables
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {
            "current_year": datetime.now().year
        }

    return app
