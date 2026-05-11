from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# En production, ces utilisateurs viennent de la base de données
USERS = {
    "yasmine@bank.com": generate_password_hash("1234")
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    email    = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    if email in USERS and check_password_hash(USERS[email], password):
        token = create_access_token(identity=email)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "role": "banquier"
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401
