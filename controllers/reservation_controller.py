from flask import Blueprint, request, jsonify
from models.reservation import ReservationModel

reservation_bp = Blueprint('reservation', __name__)
reservation_model = ReservationModel()

@reservation_bp.route('/reserve', methods=['POST'])
def reserve():
    data = request.form
    required_fields = ['pickupDate', 'returnDate', 'numOfTravellers', 'carId', 'userEmail']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400


    response, status = reservation_model.reserve(data,data,data)
    return jsonify(response), status

@reservation_bp.route('/cancel/<booking_id>', methods=['DELETE'])
def cancel_reservation(booking_id):

    response, status = reservation_model.cancel_reservation(booking_id)
    return jsonify(response), status

@reservation_bp.route('/allBookings', methods=['GET'])
def get_bookings():
    data = request.form
    print("received data", dict(data))
    if 'userEmail' not in data:
        return jsonify({'status': 'error', 'message': 'userEmail is required'}), 400
    response, status = reservation_model.get_bookings(data)
    return jsonify(response), status