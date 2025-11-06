from flask import Flask
from flask_cors import CORS
from routes.expense_routes import expense_bp

app = Flask(__name__)

# ✅ Allow requests from your React app (localhost:5173)
CORS(app, resources={r"/expense_bp/*": {"origins": "https://expenses-tracking-project-j22y.vercel.app"}}, supports_credentials=True)

# Register blueprint
app.register_blueprint(expense_bp, url_prefix='/expense_bp')

if __name__ == '__main__':
    app.run(debug=True)
