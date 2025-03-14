from models.database import Database
from flask import make_response

class CarModel:
    def __init__(self):
        self.db = Database()

    def get_all_cars(self):
        try:
            query = "SELECT carID AS id, carModel AS models, brand, carAvailability AS status, registrationNumber, pricePerHour, thumbnail FROM cars"
            self.db.execute(query)
            cars = self.db.fetchall()
            print(cars)
            return make_response({"All Cars": cars}, 200)
        except Exception as e:
            return []


    def add_car(self, car_data):
        try:
            query = """
                INSERT INTO cars (carID, carModel, registrationNumber, carAvailability, brand, pricePerHour, thumbnail)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                car_data['carID'],
                car_data['carModel'],
                car_data['registrationNumber'],
                car_data['carAvailability'],
                car_data['brand'],
                car_data['pricePerHour'],
                car_data['thumbnail']
            )
            self.db.execute(query, params)
            self.db.commit()
            return make_response({"message":"car created successfully"},201)
        except Exception as e:
            self.db.rollback()
            raise e


    def get_car_by_id(self, car_id):
        try:
            query = "SELECT * FROM cars WHERE carID = %s"
            self.db.execute(query, car_id)
            car = self.db.fetchone()
            return car
        except Exception as e:
            return None


    def update_car_availability(self, car_id, availability):
        try:
            query = "UPDATE cars SET carAvailability = %s WHERE carID = %s"
            self.db.execute(query, (availability, car_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
