import sqlite3
import logging


class User:
    def __init__(self):
        self.users = []
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT * FROM Users')
        data = data.fetchall()
        for row in data:
            d = {'user_id': row[0], 'full_name': row[1], 'password': row[2], 'real_id': row[3]}
            self.users.append(d)
        logging.info(f'List of users created.')
        conn.close()
        logging.info(f'Database closed.')

    def get_all(self):
        return self.users

    def get_by_id(self, user_id):
        user_by_id = [user for user in self.users if user['user_id'] == int(user_id)][0]
        return user_by_id

    def get_by_real_id(self, user_real_id):
        user_by_real_id = [user for user in self.users if user["real_id"] == user_real_id][0]
        return user_by_real_id

    def add(self, full_name, password, real_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO Users ("full_name", "password", "real_id")'
                       f'VALUES ("{full_name}", "{password}", "{real_id}")')
        conn.commit()
        logging.info(f'New user (ID: {real_id}) added to database.')
        last_id = cursor.execute(f'SELECT last_insert_rowid()')
        last_id = last_id.fetchone()[0]
        conn.close()
        logging.info(f'Database closed.')
        new_user = {'user_id': last_id, 'full_name': full_name,
                    'password': password, 'real_id': real_id}
        self.users.append(new_user)
        logging.info(f'New user (ID: {real_id}) added to list of users.')

    def update_password(self, user_id, new_password):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE Users SET password = {new_password} '
                       f'WHERE user_id = {user_id}')
        conn.commit()
        logging.info(f'Password for user id: {user_id} updated in the database.')
        conn.close()
        logging.info(f'Database closed.')
        for user in self.users:
            if user['user_id'] == user_id:
                position = self.users.index(user)
                self.users[position]['password'] = new_password
        logging.info(f'Password for user id: {user_id} updated in list of users.')

    def delete(self, user_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.debug(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM Users WHERE user_id = {user_id}')
        conn.commit()
        logging.info(f'User id: {user_id} deleted from database')
        conn.close()
        logging.debug(f'Database closed.')
        self.users = [user for user in self.users if user['user_id'] != user_id]
        logging.info(f'User id: {user_id} deleted from list of users')
