import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_engine = create_engine('postgresql://admin:password@localhost:5432/clew_medical')
Session = sessionmaker(bind=db_engine)
Base = declarative_base()

_connection = None
_patient_med_table_name = "patients_meds"


def get_connection():
    global _connection
    if not _connection:
        try:
            # connect to the PostgreSQL server
            _connection = psycopg2.connect(
                host="localhost",
                database="clew_medical",
                user="admin",
                password="password"
            )

        except(Exception, psycopg2.DatabaseError ) as error:
            print(error)
    return _connection


def is_table_exist():
    global _connection
    if _connection is None:
        _connection = get_connection()
        if _connection is None:
            print("Error establishing DB connection...")
            exit(-1)

    command = '''SELECT * FROM information_schema.tables 
               WHERE table_name='patients_meds' '''
    cur = _connection.cursor()

    cur.execute(command)
    is_exist = bool(cur.rowcount)
    if is_exist:
        print('truncating \'patient_meds\' table...')
        cur.execute('truncate table patients_meds')
        _connection.commit()
        print('all data has been truncated from table: \'patient_meds\'')
    return is_exist


def create_tables():
    global _connection
    global _patient_med_table_name
    if _connection is None:
        _connection = get_connection()

    commands = ('''CREATE TABLE IF NOT EXISTS patients_meds (
                p_id INTEGER NOT NULL, medication_name VARCHAR(255) NOT NULL, 
                medication_period_start TIMESTAMP NOT NULL, medication_period_end TIMESTAMP, 
                PRIMARY KEY (p_id,medication_name,medication_period_start))''',

                '''CREATE INDEX patient_med_open_period_check 
                ON patients_meds (medication_period_start,medication_period_end)'''
                )

    # create a cursor
    cur = _connection.cursor()
    # create table one by one
    for command in commands:
        # execute statement
        cur.execute(command)
    _connection.commit()
