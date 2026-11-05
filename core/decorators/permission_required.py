from functools import wraps
from flask import flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from core.models.user import User

def permission_level_required(level: int):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            print(level)
            if current_user.permissions < level:
                flash(f"You need <code>Level: {level}</code> permission to view that page. Current: <code>Level: {current_user.permissions}</code>.")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# =====================================================================
# ItemDatabase Mod REST Authentication
# Checks the HTTP Authorization header ('Bearer <token>') instead of
# session cookies so the Fabric client mod can perform admin actions.
# =====================================================================
def api_permission_level_required(level: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({
                    "success": False,
                    "error": "Missing or malformed Authorization header. Expected 'Bearer <token>'"
                }), 401

            token = auth_header.split(" ", 1)[1].strip()
            user = User.query.filter_by(api_token=token).first()
            if not user:
                return jsonify({
                    "success": False,
                    "error": "Invalid API token."
                }), 401

            if user.permissions is None or user.permissions < level:
                return jsonify({
                    "success": False,
                    "error": "Forbidden",
                    "required_level": level,
                    "current_level": user.permissions
                }), 403

            # Passes the authenticated staff user instance to the endpoint
            return f(authenticated_user=user, *args, **kwargs)
        return decorated_function
    return decorator