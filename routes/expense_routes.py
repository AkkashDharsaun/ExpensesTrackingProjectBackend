# routes/expense_routes.py
from flask import Blueprint, jsonify, request
from models.expense_model import get_all_expenses, add_expense, delete_expense

ALLOWED_ORIGINS = {"http://localhost:5173", "http://127.0.0.1:5173"}

expense_bp = Blueprint("expense_bp", __name__)

@expense_bp.after_request
def add_cors_headers(resp):
    # Echo back origin only if allowed (handles browsers checking exact origin)
    origin = request.headers.get("Origin", "")
    if origin in ALLOWED_ORIGINS:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Vary"] = "Origin"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    return resp

# ---------- Preflight handlers ----------
@expense_bp.route("/expenses", methods=["OPTIONS"])
def expenses_preflight():
    return ("", 204)

@expense_bp.route("/expenses/<int:_expense_id>", methods=["OPTIONS"])
def expenses_id_preflight(_expense_id):
    return ("", 204)

# ---------- API ----------
# 🔹 GET all expenses
@expense_bp.route("/expenses", methods=["GET"])
def get_expenses():
    items = get_all_expenses()
    return jsonify(items), 200

# 🔹 POST new expense
@expense_bp.route("/expenses", methods=["POST"])
def create_expense():
    try:
        data = request.get_json(silent=True) or {}
        category = (data.get("category") or "").strip()
        amount_raw = data.get("amount")
        note = data.get("note") or ""
        date = (data.get("date") or "").strip()

        if not category or not date or amount_raw in ("", None):
            return jsonify({"error": "Missing required fields: category, amount, date"}), 400

        try:
            amount_val = float(str(amount_raw).replace(",", "").strip())
        except ValueError:
            return jsonify({"error": "Amount must be a number"}), 400

        print("🔥 DEBUG DATA:", data)
        key = add_expense(category, amount_val, note, date)
        print("✅ Firebase push key:", key)
        return jsonify({"message": "Expense added successfully"}), 201

    except Exception as e:
        import traceback
        print("❌ FULL ERROR TRACEBACK:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# 🔹 DELETE expense by ID
# 🔹 DELETE expense by ID
@expense_bp.route("/expenses/<string:expense_id>", methods=["DELETE"])
def remove_expense(expense_id):
    try:
        delete_expense(expense_id)
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        print("Delete expense error:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

