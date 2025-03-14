from flask import Flask
from controllers.user_controller import user_bp
from controllers.car_controller import car_bp
from controllers.reservation_controller import reservation_bp
from models.car import CarModel

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(car_bp)
app.register_blueprint(reservation_bp)

if __name__ == '__main__':
    # # Add some sample cars if none exist
    # car_model = CarModel()
    # cars = car_model.get_all_cars()
    # if not cars:
    #     sample_cars = [
    #         {
    #             'carID': 'C101',
    #             'carModel': 'E220',
    #             'registrationNumber': 'MH-01-AB-1234',
    #             'carAvailability': 'AVAILABLE',
    #             'brand': 'Mercedes',
    #             'pricePerHour': 200,
    #             'thumbnail': '/car-3.jpg'
    #         },
    #         {
    #             'carID': 'C102',
    #             'carModel': 'A4',
    #             'registrationNumber': 'MH-01-AB-1235',
    #             'carAvailability': 'AVAILABLE',
    #             'brand': 'Audi',
    #             'pricePerHour': 180,
    #             'thumbnail': '/car-4.jpg'
    #         }
    #     ]
    #     for car in sample_cars:
    #         car_model.add_car(car)

    app.run(debug=True, port=4000)
