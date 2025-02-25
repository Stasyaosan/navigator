from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
import json


class DB:
    def __init__(self):
        load_dotenv()
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'database': os.getenv('DB_NAME'),
            'password': os.getenv('DB_PASSWORD'),
        }

        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                print('MySQL подключена')
                self.cursor = self.connection.cursor()
                self.cursor.execute('''
                                    create table if not exists schedule(
                                    id int auto_increment primary key,
                                    time text,
                                    format text,
                                    class text,
                                    students text,
                                    subject text,
                                    teacher text,
                                    cabinet text,
                                    link text,
                                    teacher_z text,
                                    link_z text
                                    )
                                ''')
                self.connection.commit()
        except Error as e:
            print(f'Ошибка подключения к MySQL: {e}')

    def get_from_json(self):
        str_json = open('json/data.json', 'r').read()
        return json.loads(str_json)

    def save(self):
        for time, data in self.get_from_json().items():
            print(time, data)


db = DB()
db.connect()
