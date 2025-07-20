import os
import uuid
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class SupabaseServices:
    def __init__(self):
        self.user = os.getenv('SUPABASE_USER')
        self.password = os.getenv('SUPABASE_PASSWORD')
        self.host = os.getenv('SUPABASE_HOST')
        self.port = os.getenv('SUPABASE_PORT')
        self.dbname = os.getenv('SUPABASE_DBNAME')
        self.connection = None

    def initialise_supabase(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname
            )
            print(f"Connection initialised successfully.")
        except Exception as e:
            raise Exception(f"Could not initialise supabase client: {e}")

    def save_access_token(self, **kwargs):
        '''Uploads user data into Supabase'''
        if not self.connection:
            self.initialise_supabase()
        try:
            user_uuid = str(uuid.uuid4())
            first_name = kwargs.get('first_name')
            last_name = kwargs.get('last_name')
            access_token = kwargs.get('access_token')

            if not (first_name and last_name and access_token):
                return {'message': 'error', 'status_code': 400}

            query = '''
                INSERT INTO users (user_id, first_name, last_name, access_token)
                VALUES (%s, %s, %s, %s)
            '''

            cursor = self.connection.cursor()
            cursor.execute(query, (user_uuid, first_name, last_name, access_token))
            self.connection.commit()
            cursor.close()
            print("User saved.")

            return {'message': 'success', 'status_code': 201}
        except Exception as e:
            return {'message': f'failed: {e}', 'status_code': 500}

    def get_user_by_id(self, user_id):
        if not self.connection:
            self.initialise_supabase()
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()

            return {
            	'user_id': result[0],
            	'serial_id': result[1],
            	'name': f'{result[2]} {result[3]}',
            	'access_token': result[4]
            }
            
        except Exception as e:
            raise Exception(f"Something went wrong: {e}")

if __name__ == '__main__':
    supabase = SupabaseServices()
    # result = supabase.save_access_token(
    #     first_name='John',
    #     last_name='Doe',
    #     access_token='token123abc456xyz'
    # )
    result = supabase.get_user_by_id('4567123e-e89b-12d3-a456-426614174000')
    print(result)
