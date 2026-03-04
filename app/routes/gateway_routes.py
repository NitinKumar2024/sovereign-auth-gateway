from flask import Blueprint, jsonify
from app.utils import token_required

# Create a new Blueprint just for internal microservice communication
gateway_bp = Blueprint('gateway', __name__)

@gateway_bp.route('/validate', methods=['GET'])
@token_required
def validate_token(current_user):
    """
    The core Gateway endpoint. 
    MediGuide (FastAPI) will hit this route with a user's token.
    If the @token_required decorator passes, this code runs.
    """
    # Because the decorator passed, we know the token is 100% valid.
    # We return the user's ID and Role so FastAPI knows what permissions to give them.
    return jsonify({
        "message": "Token is valid",
        "user_id": current_user['sub'],
        "role": current_user['role']
    }), 200