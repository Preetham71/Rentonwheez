from models.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def register(self, user_data):
        try:
            # Check if user already exists
            query_check = "SELECT * FROM users WHERE userEmail = %s OR userName = %s OR proofId = %s"
            self.db.execute(query_check, (user_data['userEmail'], user_data['userName'], user_data['proofId']))
            if self.db.fetchone():
                return {'status': 'error', 'message': 'User already exists'}, 400

            # Insert new user
            query_insert = """
                INSERT INTO users (userName, userEmail, userPassword, proofId, numOfTravellers, status, car, img, total)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                user_data['userName'],
                user_data['userEmail'],
                user_data['userPassword'],
                user_data['proofId'],
                1,  # Default numOfTravellers
                'INACTIVE',  # Default status
                '',  # Default car
                '',  # Default img
                0.0  # Default total
            )
            self.db.execute(query_insert, params)
            self.db.commit()
            return {'status': 'success', 'message': 'User registered successfully'}, 201
        except Exception as e:
            self.db.rollback()
            return {'status': 'error', 'message': str(e)}, 500


    def login(self, login_data):
        try:
            query = "SELECT userName, userEmail, proofId FROM users WHERE userEmail = %s AND userPassword = %s"
            self.db.execute(query, (login_data['userEmail'], login_data['userPassword']))
            user = self.db.fetchall()

            if user:
                query = "UPDATE users SET status='INACTIVE' where status='ACTIVE' "
                self.db.execute(query)
                query1 = "UPDATE users SET status= 'ACTIVE' where userEmail= %s"
                self.db.execute(query1, (login_data['userEmail'],))
                return {
                    'status': 'success',
                    'message': 'Login successful',
                    'data': user
                }, 200
            else:
                return {'status': 'error', 'message': 'Invalid credentials'}, 401
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

