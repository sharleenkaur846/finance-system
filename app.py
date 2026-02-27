from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

mysql = MySQL()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from routes.auth_routes import auth_bp
    from routes.transaction_routes import transaction_bp
    from routes.budget_routes import budget_bp
    from routes.goal_routes import goal_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
    app.register_blueprint(budget_bp, url_prefix="/api/budget")
    app.register_blueprint(goal_bp, url_prefix="/api/goals")

    return app
    
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)