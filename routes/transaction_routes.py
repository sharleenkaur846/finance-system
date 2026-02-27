from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mysql

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.route("/", methods=["POST"])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO transactions 
        (user_id, category_id, amount, type, description, date)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        user_id,
        data["category_id"],
        data["amount"],
        data["type"],
        data["description"],
        data["date"]
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Transaction added"})