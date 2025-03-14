from flask import Blueprint, request, jsonify
from models.user import UserModel

user_bp = Blueprint('user', __name__)
user_model = UserModel()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    required_fields = ['userName', 'userEmail', 'userPassword', 'proofId']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    return user_model.register(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.form
    required_fields = ['userEmail', 'userPassword']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    return user_model.login(data)
