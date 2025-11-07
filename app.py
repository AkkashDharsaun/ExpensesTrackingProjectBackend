from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from routes.expense_routes import expense_bp

app = Flask(__name__)

CORS(
    app,
    resources={r"/expense_bp/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
)

app.register_blueprint(expense_bp, url_prefix="/expense_bp")

if __name__ == "__main__":
    app.run(debug=True)
