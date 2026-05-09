from flask import request
import time

def log_requests(app):
    @app.before_request
    def before_request():
        print(f"\n{'='*60}")
        print(f"📡 [{time.strftime('%H:%M:%S')}] {request.method} {request.path}")
        print(f"📥 Headers: {dict(request.headers)}")
        if request.method in ['POST', 'PUT', 'PATCH']:
            print(f"📦 Body: {request.get_json(silent=True)}")
        print(f"{'='*60}")
    
    @app.after_request
    def after_request(response):
        print(f"📤 Response Status: {response.status_code}")
        return response