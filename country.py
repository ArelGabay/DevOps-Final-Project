import sqlite3
import logging


class Country:
    def __init__(self):
        self.countries = []
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT * FROM Countries')
        data = data.fetchall()
        for row in data:
            d = {'code_AI': row[0], 'name': row[1]}
            self.countries.append(d)
        logging.info(f'List of countries created.')
        conn.close()
        logging.info(f'Database closed.')

    def get_name(self, code_ai):
        return self.countries[int(code_ai) - 1]['name']
