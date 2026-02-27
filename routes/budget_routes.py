from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import mysql

budget_bp = Blueprint("budget", __name__)

# ➜ Add / Set Monthly Budget
@budget_bp.route("/set", methods=["POST"])
@jwt_required()
def set_budget():
    user_id = get_jwt_identity()
    data = request.get_json()

    month = data["month"]
    amount = data["amount"]

    cur = mysql.connection.cursor()

    # Check if budget already exists for this month
    cur.execute("SELECT id FROM budgets WHERE user_id=%s AND month=%s",
                (user_id, month))
    existing = cur.fetchone()

    if existing:
        # Update existing budget
        cur.execute("UPDATE budgets SET amount=%s WHERE id=%s",
                    (amount, existing[0]))
    else:
        # Insert new budget
        cur.execute("INSERT INTO budgets (user_id, month, amount) VALUES (%s,%s,%s)",
                    (user_id, month, amount))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Budget saved successfully"})


# ➜ Get User Budgets
@budget_bp.route("/", methods=["GET"])
@jwt_required()
def get_budgets():
    user_id = get_jwt_identity()

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, month, amount FROM budgets WHERE user_id=%s", (user_id,))
    budgets = cur.fetchall()
    cur.close()

    budget_list = []
    for b in budgets:
        budget_list.append({
            "id": b[0],
            "month": b[1],
            "amount": float(b[2])
        })

    return jsonify(budget_list)