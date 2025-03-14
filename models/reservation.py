from http.client import responses

from models.database import Database
from datetime import datetime
import mysql.connector
import uuid
from flask import make_response
from models.user import UserModel


class ReservationModel:
    def __init__(self):
        self.db = Database()


    def generate_unique_id(self, prefix):
        return f"{prefix}{str(uuid.uuid4())[:8]}"

    def reserve(self, reservation_data,user_data,car_data):
        try:
            # Check if car exists and is available
            query = "SELECT * FROM cars WHERE carID = %s AND carAvailability = 'Available'"
            self.db.execute(query, (reservation_data['carId'],))
            car = self.db.fetchall()
            if not car:
                return {'status': 'error', 'message': 'Car not available'}, 400

            # getting car details from db
            query = " SELECT brand, carModel, thumbnail, pricePerHour from cars WHERE carID= %s"
            self.db.execute(query, (reservation_data['carId'],))
            details = self.db.fetchall()
            s = details[0]["brand"] + " " + details[0]["carModel"]
            s1 = details[0]["thumbnail"]
            s2 = details[0]["pricePerHour"] * 5


            #updating users table
            query = "UPDATE users SET numOfTravellers = %s, car= %s, img= %s, total= %s WHERE userEmail = %s"
            self.db.execute(query, (user_data['numOfTravellers'],s,s1,s2, reservation_data['userEmail']))
            self.db.commit()




            # Update car availability
            query = "UPDATE cars SET carAvailability = 'BOOKED' WHERE carID = %s"
            self.db.execute(query, (reservation_data['carId'],))

            # Create reservation
            booking_id = self.generate_unique_id('B')
            query = """
                            INSERT INTO reservations (bookingId, userEmail, carID, reservationDate, pickupDate, returnDate)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
            params = (
                booking_id,
                reservation_data['userEmail'],
                reservation_data['carId'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                reservation_data['pickupDate'],
                reservation_data['returnDate']
            )
            self.db.execute(query, params)


            return {
                'status': 'success',
                'message': 'Reservation successful',
                'data': {
                    'bookingId': booking_id,
                    'userEmail': reservation_data['userEmail'],

                }
            }, 201
        except Exception as e:
            self.db.rollback()
            return {'status': 'error', 'message': str(e)}, 500


    def cancel_reservation(self, booking_id):
        try:
            # Check if reservation exists
            query= "SELECT * FROM reservations WHERE bookingId = %s"
            self.db.execute(query, (booking_id,))
            reservation = self.db.fetchone()
            if not reservation:
                return {'status': 'error', 'message': 'Reservation not found'}, 404

            # Update car availability
            query = "UPDATE cars SET carAvailability = 'Available' WHERE carID = %s"
            self.db.execute(query, (reservation['carID'],))

            #update users
            query = "UPDATE users SET numOfTravellers=1, car='', img='',total=0.0 WHERE userEmail= %s "
            self.db.execute(query, (reservation['userEmail'],))

            # Delete reservation
            query = "DELETE FROM reservations WHERE bookingId = %s"
            self.db.execute(query, (booking_id,))
            self.db.commit()
            return {'status': 'success', 'message': 'Reservation cancelled successfully'}, 200
        except Exception as e:
            self.db.rollback()
            return {'status': 'error', 'message': str(e)}, 500

    def get_bookings(self, reservation_data):
        try:

            query = "SELECT * FROM reservations WHERE userEmail = %s"
            self.db.execute(query, (reservation_data['userEmail'],))  # Pass as a tuple
            reservation = self.db.fetchall()
            if not reservation:
                return {'status': 'error', 'message': 'Reservation not found '}, 404

            #getting data for user data
            query= "SELECT userEmail, numOfTravellers, car, img, total from users WHERE status='ACTIVE' "
            self.db.execute(query)
            details= self.db.fetchall()
            userEmail= details[0]['userEmail']
            self.db.commit()

            query1 = "SELECT bookingId, carId, reservationDate, pickupDate, returnDate from reservations where userEmail=%s "
            self.db.execute(query1,(userEmail,))
            details1 = self.db.fetchall()
            self.db.commit()
            print("Hiiiii")

            return {
                'status': 'success',
                'message': 'Reservation successful',
                'data': {
                    'bookingId': details1[0]['bookingId'],
                    'userEmail': reservation_data['userEmail'],
                    'carId': details1[0]['carId'],
                    'reservationDate': details1[0]['reservationDate'],
                    'pickupDate': details1[0]['pickupDate'],
                    'returnDate': details1[0]['returnDate'],
                    'numOfTravellers': details[0]['numOfTravellers'],
                    'status': "Confirmed",
                    'car': details[0]['car'],
                    'img': details[0]['img'],
                    'total': details[0]['total']
                }

            }, 201

        except Exception as e:
            self.db.rollback()
            return {'status': 'error', 'message': str(e)}, 500




