from flask import Blueprint, request, jsonify
from app.models import User
import app  # We import the main app module to access our global 'db' variable
import jwt
import datetime
from config import Config
from werkzeug.security import check_password_hash

# Create the Blueprint (This is like a modular room we attach to the main house)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():

    """
    Handles New User Registration.
    Expected JSON payload: {"email": "user@example.com", "password": "securepassword123"}
    """
    # 1. Capture the incoming data
    data = request.get_json()

    # 2. The Door Check: Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    email = data.get('email').lower() # Normalize emails to lowercase
    password = data.get('password')

    # 3. The Background Check: Does this email already exist in MongoDB?
    # We look inside the 'users' collection of our database
    existing_user = app.db.users.find_one({"email": email})
    
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409

    # 4. The Secure Envelope: Create the User object (this automatically hashes the password)
    new_user = User(email=email, password=password)

    # 5. The Vault Deposit: Save to MongoDB
    # We convert the Python object to a dictionary using our to_dict() method
    app.db.users.insert_one(new_user.to_dict())

    # 6. The Receipt: Send success message
    return jsonify({
        "message": "User registered successfully",
        "email": new_user.email,
        "role": new_user.role
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and issues a JWT.
    Expected JSON payload: {"email": "user@example.com", "password": "securepassword123"}
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing email or password"}), 400

    email = data.get('email').lower()
    password = data.get('password')

    # Find user in the database
    user_record = app.db.users.find_one({"email": email})

    if not user_record:
        return jsonify({"error": "Invalid email or password"}), 401

    # Verify the password using the static method from the User model or check_password_hash directly
    # Since we are retrieving a dict from Mongo, we extract the hash
    stored_hash = user_record.get("password_hash")
    
    if not User.verify_password(stored_hash, password):
         return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT Tokens
    # 1. Access Token (Short-lived, e.g., 1 hour)
    access_payload = {
        "sub": str(user_record['_id']),  # Subject (User ID)
        "email": user_record['email'],
        "role": user_record['role'],
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    
    access_token = jwt.encode(access_payload, Config.SECRET_KEY, algorithm="HS256")

    # 2. Refresh Token (Longer-lived, e.g., 7 days - we'll implement the refresh route later)
    refresh_payload = {
         "sub": str(user_record['_id']),
         "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    
    refresh_token = jwt.encode(refresh_payload, Config.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200