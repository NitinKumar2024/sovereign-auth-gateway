from flask import Flask
from pymongo import MongoClient
from config import Config
from app.routes.auth_routes import auth_bp
from app.routes.gateway_routes import gateway_bp

# Initialize variables but don't connect them yet
mongo_client = None
db = None

def create_app(config_class=Config):
    """
    The Application Factory.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Connect to Local MongoDB
    global mongo_client, db
    mongo_client = MongoClient(app.config['MONGO_URI'])
    
    # Extract the database name from the URI (e.g., 'beehive_auth')
    db_name = app.config['MONGO_URI'].split('/')[-1]
    db = mongo_client[db_name]

    # 2. Register Blueprints (We will uncomment this in the next step)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Register the Gateway Blueprint
    app.register_blueprint(gateway_bp, url_prefix='/api/gateway')

    # 3. A simple health check route to prove the server is alive
    @app.route('/health')
    def health_check():
        db_status = False
        try:
            # Send a lightweight 'ping' command to the admin database
            mongo_client.admin.command('ping')
            db_status = True
        except Exception as e:
            db_status = False

        return {
            "status": "healthy", 
            "service": "sovereign-auth-gateway",
            "database_connected": db_status
        }, 200

    return app