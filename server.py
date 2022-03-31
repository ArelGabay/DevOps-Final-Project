from flask import *
from flight import Flight
from user import User
from ticket import Ticket
import sqlite3
import logging

logging.basicConfig(filename='main.log', level=0,
                    format='%(asctime)s: - > %(levelname)s - > %(message)s')

app = Flask(__name__)
logging.info(f'Server on.')
DATABASE = 'DB/FinalProject.db'

flight = Flight()
user = User()
ticket = Ticket()


def create_dict_ticket(user_id):
    connection = sqlite3.connect(database='DB/FinalProject.db', check_same_thread=False)
    logging.info(f'Database opened.')
    cursor = connection.cursor()
    data = cursor.execute(f'SELECT t.ticket_id,f.flight_id,f.timestamp,c1.name,c2.name  FROM Tickets t, '
                          f'Flights f, Countries c1, Countries c2 WHERE t.user_id = {user_id} '
                          f'AND c1.code_AI = f.origin_country_id AND c2.code_AI = f.dest_country_id '
                          f'AND t.flight_id = f.flight_id')
    data = data.fetchall()
    tickets = []
    for row in data:
        d = {'ticket_id': row[0], 'flight_id': row[1], 'flight_time': row[2], 'origin': row[3],
             'destination': row[4]}
        tickets.append(d)
    connection.close()
    logging.info(f'Database closed.')
    return tickets


@app.route('/')
def sign_in():
    return render_template('index.html')


@app.route('/check_sign_in', methods=['POST'])
def check_sign_in():
    id = request.form['id']
    password = request.form['psw']
    data = user.get_by_real_id(id)
    if data['password'] == password:
        return redirect(url_for('home_page', user_id=data["user_id"]))
    else:
        return render_template('index.html', login_message='Invalid ID or Password. Please try again.', color='red')


@app.route('/home_page/<user_id>')
def home_page(user_id):
    data = user.get_by_id(user_id)
    return render_template('home_page.html', user_name=data['full_name'], user_id=user_id)


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    if request.form['id'].isdigit():
        id = request.form['id']
    else:
        return render_template('sign_up.html', signup_error='The ID field can only contain numbers. Please try again.')

    if request.form['psw'] == request.form['psw_confirm']:
        password = request.form['psw']
    else:
        return render_template('sign_up.html', signup_error='The password fields do not match. Please try again.')

    if request.form['f_name'].isalpha() and request.form['l_name'].isalpha():
        full_name = request.form['f_name'] + " " + request.form['l_name']
    else:
        return render_template('sign_up.html', signup_error='The Name fields can only contain letters. '
                                                            'Please try again.')
    user.add(full_name, password, id)
    return render_template('index.html', login_message='User created successfully', color='green')


@app.route('/view_tickets/<user_id>')
def view_tickets(user_id):
    tickets = create_dict_ticket(user_id)
    return render_template('view_tickets.html', tickets=tickets, user_id=user_id)


@app.route('/delete_ticket', methods=['POST', 'DELETE'])
def delete_ticket():
    ticketid = request.form['ticketID']
    userid = request.form['userID']
    flightid = request.form['flightID']
    ticket.delete(ticketid)
    flight.update_seats(flightid, 1)
    tickets = create_dict_ticket(userid)
    return render_template('view_tickets.html', tickets=tickets, user_id=userid)


@app.route('/view_flights/<user_id>')
def view_flights(user_id):
    flights = flight.get_all()
    return render_template('buy_ticket.html', flights=flights, user_id=user_id)


@app.route('/buy_ticket', methods=['POST'])
def buy_ticket():
    flightid = request.form['flightID']
    userid = request.form['userID']
    if flight.update_seats(flightid, -1) > 0:
        ticket.add(userid, flightid)
        return redirect(url_for('view_tickets', user_id=userid))
    else:
        return '<h1>Ticket Taken!</h1>'


# -------------------------- Flights APIs ------------------------------- #


@app.route('/flights')
def get_all_flights():
    return jsonify(flight.get_all())


@app.route('/flight/<flightid>')
def get_flight_id(flightid):
    return flight.get_by_id(flightid)


@app.route('/add_flight', methods=['POST', 'GET'])
def add_flight():
    remaining_seats = request.form['seats']
    timestamp = request.form['timestamp']
    origin_country_id = request.form['origin']
    dest_country_id = request.form['dest']
    flight.add(timestamp, remaining_seats, origin_country_id, dest_country_id)
    return jsonify(results={"Status": 200})


@app.route('/delete_flight/<int:flight_id>', methods=['DELETE', 'GET'])
def delete_flight(flight_id):
    flight.delete(flight_id)
    return jsonify(results={"Status": 200})


@app.route('/update_seats', methods=['PUT'])
def update_seats():
    flightid = request.form['flightid']
    seats = request.form['seats']
    flight.update_seats_number(flightid, seats)
    return jsonify(results={"Status": 200})


# -------------------------- Users APIs ------------------------------- #


@app.route('/users')
def get_all_users():
    return jsonify(user.get_all())


@app.route('/user/<userid>')
def get_user_id(userid):
    return user.get_by_id(userid)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    full_name = request.form['full_name']
    password = request.form['password']
    real_id = request.form['real_id']
    user.add(full_name, password, real_id)
    return jsonify(results={"Status": 200})


@app.route('/delete_user/<int:user_id>', methods=['DELETE', 'GET'])
def delete_user(user_id):
    user.delete(user_id)
    return jsonify(results={"Status": 200})


@app.route('/update_password', methods=['PUT'])
def update_password():
    userid = request.form['flightid']
    password = request.form['seats']
    user.update_password(userid, password)
    return jsonify(results={"Status": 200})


# -------------------------- Tickets APIs ------------------------------- #


@app.route('/tickets')
def get_all_tickets():
    return jsonify(ticket.get_all())


@app.route('/ticket/<ticketid>')
def get_ticket_id(ticketid):
    return ticket.get_by_id(ticketid)


@app.route('/add_ticket', methods=['POST', 'GET'])
def add_ticket():
    user_id = request.form['user_id']
    flight_id = request.form['flight_id']
    ticket.add(user_id, flight_id)
    return jsonify(results={"Status": 200})


@app.route('/delete_ticket/<int:ticket_id>', methods=['DELETE', 'GET'])
def delete_ticket_id(ticket_id):
    ticket.delete(ticket_id)
    return jsonify(results={"Status": 200})


app.run(debug=True)
logging.info(f'Server off.')
