from db import get_db_connection

# ✅ Fetch all expenses
def get_all_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# ✅ Add new expense
def add_expense(category, amount, note, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (category, amount, note, date) VALUES (%s, %s, %s, %s)",
        (category, amount, note, date)
    )
    conn.commit()
    conn.close()
    return True

# ✅ Delete expense
def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    conn.close()
    return True
