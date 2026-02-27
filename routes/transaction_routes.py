from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import get_db_connection

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/transactions", methods=["POST"])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO transactions 
        (user_id, type, amount, category, description, date)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            user_id,
            data["type"],
            data["amount"],
            data["category"],
            data["description"],
            data["date"],
        ),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Transaction added successfully"}), 201


@transaction_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM transactions WHERE user_id = %s", (user_id,)
    )
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(transactions)