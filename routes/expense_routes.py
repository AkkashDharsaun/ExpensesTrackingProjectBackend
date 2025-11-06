from flask import Blueprint, jsonify, request
from models.expense_model import get_all_expenses, add_expense, delete_expense

expense_bp = Blueprint('expense_bp', __name__)

# 🔹 GET all expenses
@expense_bp.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = get_all_expenses()
    return jsonify(expenses), 200

# 🔹 POST new expense
@expense_bp.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()
    category = data.get('category')
    amount = data.get('amount')
    note = data.get('note')
    date = data.get('date')

    if not all([category, amount, date]):
        return jsonify({"error": "Missing required fields"}), 400

    add_expense(category, amount, note, date)
    return jsonify({"message": "Expense added successfully"}), 201

# 🔹 DELETE expense by ID
@expense_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def remove_expense(expense_id):
    delete_expense(expense_id)
    return jsonify({"message": "Expense deleted successfully"}), 200
