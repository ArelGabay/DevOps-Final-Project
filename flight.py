from country import *
import sqlite3
import logging


class Flight:
    def __init__(self):
        self.flights = []
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        data = cursor.execute(f'SELECT f.flight_id,f.timestamp,f.remaining_seats,c1.name,c2.name FROM Flights f, '
                              f'Countries c1, '
                              f'Countries c2 WHERE c1.code_AI = f.origin_country_id AND c2.code_AI = f.dest_country_id')
        data = data.fetchall()
        for row in data:
            d = {'flight_id': row[0], 'flight_time': row[1], 'seats': row[2], 'origin': row[3], 'destination': row[4]}
            self.flights.append(d)
        logging.info(f'List of flights created.')
        conn.close()
        logging.info(f'Database closed.')

    def get_all(self):
        return self.flights

    def get_by_id(self, flight_id):
        flight_by_id = [flight for flight in self.flights if flight["flight_id"] == int(flight_id)][0]
        return flight_by_id

    def add(self, timestamp, remaining_seats, origin_country_id, dest_country_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO Flights ("timestamp", "remaining_seats", "origin_country_id", "dest_country_id")'
                       f'VALUES ("{timestamp}", {remaining_seats}, {origin_country_id}, {dest_country_id})')
        conn.commit()

        last_id = cursor.execute(f'SELECT last_insert_rowid()')
        last_id = last_id.fetchone()[0]
        logging.info(f'New flight id: {last_id} added to the database.')
        conn.close()
        logging.info(f'Database closed.')
        country = Country()
        new_flight = {'flight_id': last_id, 'flight_time': timestamp,
                      'seats': remaining_seats, 'origin': country.get_name(origin_country_id),
                      'destination': country.get_name(dest_country_id)}
        self.flights.append(new_flight)
        logging.info(f'New flight id: {last_id} added to list of flights.')

    def update_seats(self, flight_id, number):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        if number == -1:
            cursor.execute(f'UPDATE Flights SET remaining_seats = remaining_seats - 1 '
                           f'WHERE flight_id = {flight_id} AND remaining_seats > 0')
            conn.commit()
            logging.info(f'Number of seats for flight id: {flight_id} updated in the database.')
            conn.close()
            logging.info(f'Database closed.')
            for flight in self.flights:
                if flight['flight_id'] == flight_id:
                    position = self.flights.index(flight)
                    self.flights[position]['seats'] = self.flights[position]['seats'] - 1
            logging.info(f'Number of seats for flight id: {flight_id} updated in list of flights.')

        else:
            cursor.execute(f'UPDATE Flights SET remaining_seats = remaining_seats + 1 '
                           f'WHERE flight_id = {flight_id}')
            conn.commit()
            logging.info(f'Number of seats for flight id: {flight_id} updated in the database.')
            conn.close()
            logging.info(f'Database closed.')
            for flight in self.flights:
                if flight['flight_id'] == flight_id:
                    position = self.flights.index(flight)
                    self.flights[position]['seats'] = self.flights[position]['seats'] + 1
            logging.info(f'Number of seats for flight id: {flight_id} updated in list of flights.')
        if cursor.rowcount > 0:
            return True
        else:
            return False

    def update_seats_number(self, flight_id, seats_number):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'UPDATE Flights SET remaining_seats = {seats_number} WHERE flight_id = {flight_id}')
        conn.commit()
        logging.info(f'Number of seats for flight id: {flight_id} updated in the database.')
        conn.close()
        logging.info(f'Database closed.')
        for flight in self.flights:
            if flight['flight_id'] == flight_id:
                position = self.flights.index(flight)
                self.flights[position]['seats'] = seats_number
        logging.info(f'Number of seats for flight id: {flight_id} updated in list of flights.')

    def delete(self, flight_id):
        conn = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
        logging.info(f'Database opened.')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM Flights WHERE flight_id = {flight_id}')
        conn.commit()
        logging.info(f'flight id: {flight_id} deleted from database.')
        conn.close()
        logging.info(f'Database closed.')
        self.flights = [flight for flight in self.flights if flight['flight_id'] != flight_id]
        logging.info(f'flight id: {flight_id} deleted from list of flights.')
