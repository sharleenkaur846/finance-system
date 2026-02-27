from flask import Blueprint, request, jsonify
from app import mysql
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
                (name,email,hashed))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s",(email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        token = create_access_token(identity=user[0])
        return jsonify({"token":token})

    return jsonify({"error":"Invalid credentials"}),401