import os

from flask import Flask
from flask_cors import CORS

from app.routes.bridge import bridge_bp
from app.routes.light import light_bp
from app.routes.motion import motion_bp
from app.routes.voice import voice_bp
from app.services.automation_service import configure
from app.state_store import init_state
from app.utils.response import error_response, success_response


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config["AUTO_OFF_SECONDS"] = int(os.getenv("AUTO_OFF_SECONDS", "10"))
    app.config["DEFAULT_MODE"] = os.getenv("DEFAULT_MODE", "auto")
    app.config["MANUAL_OVERRIDE_SECONDS"] = int(os.getenv("MANUAL_OVERRIDE_SECONDS", "30"))

    init_state(default_mode=app.config["DEFAULT_MODE"])
    configure(
        auto_off_seconds=app.config["AUTO_OFF_SECONDS"],
        manual_override_seconds=app.config["MANUAL_OVERRIDE_SECONDS"],
    )

    @app.get("/")
    def healthcheck():
        return success_response("Smart Light API is running", {"service": "SmartSimLight"})

    app.register_blueprint(light_bp)
    app.register_blueprint(motion_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(bridge_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("Route not found", 404)

    @app.errorhandler(500)
    def internal_error(_error):
        return error_response("Internal server error", 500)

    return app
