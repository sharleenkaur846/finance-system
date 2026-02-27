from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mysql

goal_bp = Blueprint("goals", __name__)

# ➜ Add New Goal
@goal_bp.route("/add", methods=["POST"])
@jwt_required()
def add_goal():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data["title"]
    target_amount = data["target_amount"]
    deadline = data["deadline"]

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO goals (user_id, title, target_amount, deadline)
        VALUES (%s,%s,%s,%s)
    """, (user_id, title, target_amount, deadline))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Goal created successfully"})


# ➜ Get User Goals
@goal_bp.route("/", methods=["GET"])
@jwt_required()
def get_goals():
    user_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, title, target_amount, saved_amount, deadline 
        FROM goals WHERE user_id=%s
    """, (user_id,))

    goals = cur.fetchall()
    cur.close()

    goal_list = []
    for g in goals:
        goal_list.append({
            "id": g[0],
            "title": g[1],
            "target_amount": float(g[2]),
            "saved_amount": float(g[3]),
            "deadline": str(g[4])
        })

    return jsonify(goal_list)


# ➜ Update Saved Amount (Track Progress ⭐)
@goal_bp.route("/update/<int:goal_id>", methods=["PUT"])
@jwt_required()
def update_goal(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    added_amount = data["amount"]

    cur = mysql.connection.cursor()

    # Get current saved amount
    cur.execute("SELECT saved_amount FROM goals WHERE id=%s AND user_id=%s",
                (goal_id, user_id))
    goal = cur.fetchone()

    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    new_amount = float(goal[0]) + float(added_amount)

    cur.execute("UPDATE goals SET saved_amount=%s WHERE id=%s",
                (new_amount, goal_id))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Goal updated successfully"})