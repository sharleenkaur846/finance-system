from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)


# ✅ Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=int(os.getenv("MYSQL_PORT", 3306))
    )


# ✅ Test Route
@app.route("/")
def home():
    return jsonify({"message": "Finance System Backend Running Successfully 🚀"})


# Import routes
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from routes.budget_routes import budget_bp
from routes.goal_routes import goal_bp

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(transaction_bp, url_prefix="/api")
app.register_blueprint(budget_bp, url_prefix="/api")
app.register_blueprint(goal_bp, url_prefix="/api")

@app.route("/test")
def test():
    return "TEST WORKING"

@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "Backend Live ✅"
    }, 200

if __name__ == "__main__":
    app.run(debug=True)
    
print("APP LOADED")