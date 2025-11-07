# models/expense_model.py
from firebase_client import rtdb

# RTDB path (simple global collection). Later: /users/{uid}/expenses
BASE_PATH = "/expenses"

# ✅ Fetch all expenses
def get_all_expenses():
    ref = rtdb().reference(BASE_PATH)
    data = ref.get() or {}   # {pushId: { ... }, ... }
    items = []
    for key, val in data.items():
        item = {**val, "id": key}
        items.append(item)
    # Sort by (date, createdAt) descending; missing fields go last
    def _sort_key(x):
        return (
            x.get("date") or "",
            x.get("createdAt") or 0
        )
    items.sort(key=_sort_key, reverse=True)
    return items

# ✅ Add new expense
def add_expense(category, amount, note, date):
    ref = rtdb().reference(BASE_PATH).push({
        "category": category,
        "amount": float(amount),     # amount already validated as float-compatible
        "note": note,
        "date": date,                # "YYYY-MM-DD"
        "createdAt": {".sv": "timestamp"}  # server time
    })
    return ref.key

# ✅ Delete expense
def delete_expense(expense_id):
    rtdb().reference(f"{BASE_PATH}/{expense_id}").delete()
    return True
