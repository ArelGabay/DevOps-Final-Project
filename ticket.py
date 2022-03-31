import sqlite3
import logging


class Ticket:
    def __init__(self):
        self.tickets = []
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT * FROM Tickets')
        data = data.fetchall()
        for row in data:
            d = {'ticket_id': row[0], 'user_id': row[1], 'flight_id': row[2]}
            self.tickets.append(d)
        logging.info(f'List of tickets created.')
        conn.close()
        logging.info(f'Database closed.')

    def get_all(self):
        return self.tickets

    def get_by_id(self, ticket_id):
        ticket_by_id = [ticket for ticket in self.tickets if ticket["ticket_id"] == ticket_id][0]
        return ticket_by_id

    def add(self, user_id, flight_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO Tickets ("user_id", "flight_id") VALUES ({user_id}, {flight_id})')
        conn.commit()
        logging.info(f'New ticket for user: {user_id} added to the database.')
        last_id = cursor.execute(f'SELECT last_insert_rowid()')
        last_id = last_id.fetchone()[0]
        conn.close()
        logging.info(f'Database closed.')
        new_ticket = {'ticket_id': last_id, 'user_id': user_id,
                      'flight_id': flight_id}
        self.tickets.append(new_ticket)
        logging.info(f'New ticket for user: {user_id} added to the list of tickets.')

    def delete(self, ticket_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM Tickets WHERE ticket_id = {ticket_id}')
        conn.commit()
        logging.info(f'ticket id: {ticket_id} deleted from database.')
        conn.close()
        logging.info(f'Database closed.')
        self.tickets = [ticket for ticket in self.tickets if ticket['user_id'] != ticket_id]
        logging.info(f'ticket id: {ticket_id} deleted from list of tickets.')
