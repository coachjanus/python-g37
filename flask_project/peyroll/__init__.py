import logging
import os
from flask import Flask
from . import pages, database, staff, auth


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration suitable for development; can be overridden by env or instance config
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", None),
        DATABASE=os.path.join(app.instance_path, "payroll.db"),
        # Secure cookie defaults (override as needed in app.cfg or environment)
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        # Only enable in production behind HTTPS
        SESSION_COOKIE_SECURE=os.environ.get("FLASK_SESSION_COOKIE_SECURE", "false").lower() == "true",
    )

    # Ensure instance folder exists; only ignore already-exists case
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except PermissionError as e:
        # Fail fast on permission issues which would break DB and config handling
        raise RuntimeError(f"Cannot create instance path '{app.instance_path}': {e}") from e

    # Load instance-specific config if present; this should define a SECRET_KEY for non-dev
    app.config.from_pyfile("app.cfg", silent=True)

    # If still no SECRET_KEY, generate a temporary one for dev and warn (do not print secret)
    if not app.config.get("SECRET_KEY"):
        logging.warning("SECRET_KEY not set; generating a temporary development key. Do not use in production.")
        # Use a random key only for local dev sessions
        import secrets

        app.config["SECRET_KEY"] = secrets.token_hex(16)

    # Log non-sensitive config details
    logging.getLogger(__name__).info("Using database at %s", app.config.get("DATABASE"))

    database.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(staff.bp)
    app.register_blueprint(auth.bp)
    return app
    
    

