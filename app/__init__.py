import os
import time

from flask import Flask, request
from flask_cors import CORS

from app.routes.bridge import bridge_bp
from app.routes.advanced_controls import advanced_controls_bp
from app.routes.light import light_bp
from app.routes.motion import motion_bp
from app.routes.voice import voice_bp
from app.services.automation_service import configure
from app.state_store import init_state
from app.utils.response import error_response, success_response


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # Configuration
    app.config["AUTO_OFF_SECONDS"] = int(os.getenv("AUTO_OFF_SECONDS", "10"))
    app.config["DEFAULT_MODE"] = os.getenv("DEFAULT_MODE", "auto")
    app.config["MANUAL_OVERRIDE_SECONDS"] = int(os.getenv("MANUAL_OVERRIDE_SECONDS", "30"))

    # Initialize state and automation
    init_state(
        default_mode=app.config["DEFAULT_MODE"],
        auto_off_seconds=app.config["AUTO_OFF_SECONDS"],
    )
    configure(
        auto_off_seconds=app.config["AUTO_OFF_SECONDS"],
        manual_override_seconds=app.config["MANUAL_OVERRIDE_SECONDS"],
    )

    # ========== Request Logging Middleware ==========
    @app.before_request
    def log_request():
        print(f"\n{'='*60}")
        print(f"📡 [{time.strftime('%H:%M:%S')}] {request.method} {request.path}")
        print(f"📥 Headers: {dict(request.headers)}")
        
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                payload = request.get_json(silent=True)
                if payload:
                    print(f"📦 Body: {payload}")
                else:
                    print(f"📦 Body: {request.get_data(as_text=True)}")
            except:
                print(f"📦 Body: {request.get_data(as_text=True)}")
        print(f"{'='*60}")

    @app.after_request
    def log_response(response):
        print(f"📤 Response Status: {response.status_code}")
        return response

    # ========== Routes ==========
    @app.get("/")
    def healthcheck():
        print("🔵 [ROOT] GET / - Health check requested")
        return success_response("Smart Light API is running", {"service": "SmartSimLight"})

    # Register blueprints
    app.register_blueprint(light_bp)
    app.register_blueprint(motion_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(bridge_bp)
    app.register_blueprint(advanced_controls_bp)

    # ========== Error Handlers ==========
    @app.errorhandler(404)
    def not_found(_error):
        print("❌ [ERROR] 404 - Route not found")
        return error_response("Route not found", 404)

    @app.errorhandler(500)
    def internal_error(_error):
        print("❌ [ERROR] 500 - Internal server error")
        return error_response("Internal server error", 500)

    return app