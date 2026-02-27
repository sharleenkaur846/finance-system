from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import get_db_connection

goal_bp = Blueprint("goals", __name__)


@goal_bp.route("/goals", methods=["POST"])
@jwt_required()
def add_goal():
    user_id = get_jwt_identity()
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO goals 
        (user_id, goal_name, target_amount, saved_amount)
        VALUES (%s, %s, %s, %s)""",
        (user_id, data["goal_name"], data["target_amount"], 0),
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Goal added successfully"}), 201


@goal_bp.route("/goals", methods=["GET"])
@jwt_required()
def get_goals():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM goals WHERE user_id = %s", (user_id,)
    )
    goals = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(goals)