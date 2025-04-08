import mysql.connector
from mysql.connector import Error
from app.core.config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.connection = self._connect()
        self.cursor = self.connection.cursor(dictionary=True) if self.connection else None

    def _connect(self):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def _fetch_one(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def _execute_query(self, query, values):
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def save_appointment(self, data):
        try:
            print(data['conversation_id'])
            existing_record = self._fetch_one(
                "select id from appoinments where conversation_id = %s",
                (data['conversation_id'],)
            )

            if existing_record:
                query = """
                update appoinments set
                    transcript = %s, audio_file = %s, name = %s, phone = %s, email = %s,
                    reason = %s, gender = %s, age = %s, city = %s, zip = %s, history = %s,
                    app_date = %s, app_time = %s, referral = %s, appointment_status = %s, summary = %s
                where conversation_id = %s
                """
                values = (
                    data['transcript'], data['audio_file'], data['name'], data['phone'],
                    data['email'], data['reason'], data['gender'], data['age'], data['city'],
                    data['zip'], data['history'], data['date'], data['time'], data['referral'],
                    data['appointment_status'], data.get('summary', ''), data['conversation_id']
                )
                self._execute_query(query, values)
                record_id = existing_record['id']
            else:
                # Insert new record
                query = """
                Insert into appoinments (
                    conversation_id, transcript, audio_file, name, phone, email,
                    reason, gender, age, city, zip, history, app_date, app_time,
                    referral, appointment_status, summary
                ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = tuple(data.values())
                record_id = self._execute_query(query, values)

            return self._fetch_one("select * from appoinments where id = %s", (record_id,))

        except Exception as e:
            self.connection.rollback()
            print(f"Database error: {str(e)}")
            raise

    def save_multiple_appointments(self, data_list):
        return [self.save_appointment(data) for data in data_list]


def save_to_database(data_list):
    db_manager = DatabaseManager()
    try:
        return db_manager.save_multiple_appointments(data_list)
    finally:
        db_manager.close()
