from flask import Blueprint, jsonify, request
from models.car import CarModel

car_bp = Blueprint('car', __name__)
car_model = CarModel()

@car_bp.route('/getPackages', methods=['GET'])
def get_packages():
    return car_model.get_all_cars()

@car_bp.route('/addCar', methods=['POST'])
def add_car():
    return car_model.add_car(request.form)