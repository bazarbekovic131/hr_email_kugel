import psycopg2
import pandas as pd

class WADatabase():
    #### create tables users and surveys for now ###

    def __init__(self, db_config):
        self.conn = self.create_connection(db_config)
        self.create_tables()

    def create_connection(self, db_config):
        try:
            conn = psycopg2.connect(**db_config)
            return conn
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
        
    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(32) UNIQUE NOT NULL,
                        current_step INTEGER DEFAULT 0,
                        survey_mode BOOLEAN DEFAULT FALSE,
                        has_completed_survey BOOLEAN DEFAULT FALSE,
                        wants_notifications BOOLEAN DEFAULT TRUE
                        );""")
            
            cur.execute("""CREATE TABLE IF NOT EXISTS surveys (
                        id SERIAL PRIMARY KEY,
                        phone VARCHAR(16) UNIQUE NOT NULL REFERENCES users(phone),
                        age VARCHAR(32),
                        production_experience VARCHAR(32),
                        completed_survey BOOLEAN DEFAULT FALSE,
                        name VARCHAR(50),
                        vacancy VARCHAR(32),
                        sent BOOLEAN DEFAULT FALSE,
                        resume VARCHAR(32) DEFAULT 'Не указан'
                        );""")

            create_table_query = '''
                        CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        requirements TEXT,
                        details TEXT,
                        tasks TEXT,
                        salary VARCHAR(32) DEFAULT 'Не указано'
                        );'''
            cur.execute(create_table_query)

            self.conn.commit()

    # new ones. untested
    def get_incomplete_surveys(self):
        with self.conn.cursor() as cur:
            query = "SELECT * FROM surveys WHERE sent = FALSE AND vacancy != '';"
            cur.execute(query)
            df = cur.fetchall()
        self.conn.commit()
        return pd.DataFrame(df, columns=['id', 'phone', 'age','production_experience', 'completed_survey', 'name', 'vacancy', 'sent', 'resume'])

    def update_sent_status(self, survey_id):
        query = "UPDATE surveys SET sent = TRUE WHERE id = %s;"
        self.conn.cursor().execute(query, (survey_id,))
        self.conn.commit()