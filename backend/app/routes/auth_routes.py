from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from ..models import User

auth_bp=Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data=request.get_json(silent=True) or {}
    user=User.query.filter_by(username=data.get("username")).first()
    if not user or not check_password_hash(user.password_hash, data.get("password", "")):
        return jsonify({"error":"Invalid username or password."}), 401
    return jsonify({"access_token":create_access_token(identity=str(user.id)), "user":user.to_dict()}), 200
