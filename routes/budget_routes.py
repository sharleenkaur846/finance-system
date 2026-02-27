from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import get_db_connection

budget_bp = Blueprint("budgets", __name__)


@budget_bp.route("/budgets", methods=["POST"])
@jwt_required()
def set_budget():
    user_id = get_jwt_identity()
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO budgets (user_id, category, amount) VALUES (%s, %s, %s)",
        (user_id, data["category"], data["amount"]),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Budget set successfully"}), 201


@budget_bp.route("/budgets", methods=["GET"])
@jwt_required()
def get_budgets():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM budgets WHERE user_id = %s", (user_id,)
    )
    budgets = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(budgets)