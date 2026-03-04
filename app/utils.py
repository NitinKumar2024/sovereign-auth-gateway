from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    """
    A decorator to protect Flask routes. 
    It checks for a valid JWT in the 'Authorization' header.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 1. Look for the token in the headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Enterprise standard: Tokens are sent as "Bearer <token_string>"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]

        # 2. If no token is found, bounce them
        if not token:
            return jsonify({"error": "Token is missing! Access denied."}), 401

        # 3. Verify the token's cryptograpic signature and expiration
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            # If successful, we pass the payload (user info) into the route
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired! Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token! Security breach attempt logged."}), 401

        # 4. Open the door and run the actual route
        return f(current_user=payload, *args, **kwargs)

    return decorated