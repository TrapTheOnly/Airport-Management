from datetime import datetime
import json
from flask_restful import Api, Resource, marshal_with, fields
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
from os import system, name

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def clearTheConsole():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


clearTheConsole()


class Admin(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(100))


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departure_city = db.Column(db.String(50))
    arrival_city = db.Column(db.String(50))
    departure_time = db.Column(db.DateTime)
    arrival_time = db.Column(db.DateTime)
    airplane = db.Column(db.String(50))
    passenger_count = db.Column(db.Integer)


db.create_all()
db.session.query(Admin).delete()

f = open("admin.json")
admins = json.loads(f.read())
for i in range(len(admins)):
    username = admins[i]["username"]
    password = hash(admins[i]["password"])
    user = Admin(username=username, password=password)
    db.session.add(user)
    db.session.commit()
f.close()

tokens = {}


def checkToken(token):
    if token in tokens.values():
        return True


flightResourceFields = {
    'departure_city': fields.String,
    'arrival_city': fields.String,
    'departure_time': fields.DateTime(dt_format='rfc822'),
    'arrival_time': fields.DateTime(dt_format='rfc822'),
    'airplane': fields.String,
    'passenger_count': fields.Integer
}


class Flights(Resource):
    @marshal_with(flightResourceFields)
    def get(self, from_addr, to):
        if from_addr == 'null' and to == 'null':
            flights = Flight.query.all()
            return flights

        elif from_addr == 'null' and to != 'null':
            flights = Flight.query.filter_by(arrival_city=to).all()
            return flights

        elif from_addr != 'null' and to == 'null':
            flights = Flight.query.filter_by(
                departure_city=from_addr).all()
            return flights

        else:
            flights = Flight.query.filter_by(
                departure_city=from_addr, arrival_city=to).all()
            return flights


class ChangeFlights(Resource):
    def post(self, mode, token):
        if checkToken(token):
            if mode == "add":
                try:
                    json_data = request.json
                    flight = Flight(
                        departure_city=json_data['departure_city'],
                        arrival_city=json_data['arrival_city'],
                        departure_time=datetime.strptime(
                            json_data['departure_time'], '%b %d %Y %I:%M%p'),
                        arrival_time=datetime.strptime(
                            json_data['arrival_time'], '%b %d %Y %I:%M%p'),
                        airplane=json_data['airplane'],
                        passenger_count=int(json_data['passenger_count'])
                    )
                    db.session.add(flight)
                    db.session.commit()
                    return f"Added a flight from {json_data['departure_city']} to {json_data['arrival_city']} on {json_data['departure_time']}", 200
                except:
                    return f"Unable to add this flight!"

            elif mode == 'update':
                try:
                    json_data = request.json
                    flight = Flight.query.filter_by(
                        departure_city=json_data['departure_city'],
                        arrival_city=json_data['arrival_city'],
                        airplane=json_data['airplane'],
                        passenger_count=int(json_data['passenger_count'])
                    ).first()
                    change_param = json_data['change']
                    change_value = json_data['change_to']
                    if change_param == 'departure_city':
                        flight.departure_city = change_value
                    elif change_param == 'arrival_city':
                        flight.arrival_city = change_value
                    elif change_param == 'departure_time':
                        flight.departure_time = datetime.strptime(
                            change_value, '%b %d %Y %I:%M%p')
                    elif change_param == 'arrival_time':
                        flight.arrival_time = datetime.strptime(
                            change_value, '%b %d %Y %I:%M%p')
                    elif change_param == 'airplane':
                        flight.airplane = change_value
                    elif change_param == 'passenger_count':
                        flight.passenger_count = int(change_value)
                    db.session.commit()
                    return "Changed!"

                except Exception as e:
                    return "Error! " + str(e)

            elif mode == 'delete':
                try:
                    json_data = request.json
                    flight = Flight.query.filter_by(
                        departure_city=json_data['departure_city'],
                        arrival_city=json_data['arrival_city'],
                        airplane=json_data['airplane'],
                        passenger_count=int(json_data['passenger_count'])
                    ).first()
                    db.session.delete(flight)
                    db.session.commit()
                    return "Deleted!"

                except Exception as e:
                    return "Error! " + str(e)


class Login(Resource):
    def get(self, login, password):
        try:
            admin = Admin.query.filter_by(username=login).first()
            if int(admin.password) == int(hash(str(password))):
                if login in tokens:
                    return tokens[login]
                token = randint(1000, 2000)
                tokens[login] = token
                return token
            else:
                return 0
        except:
            return 0


class End(Resource):
    def get(self, token):
        for key in tokens.keys():
            if tokens[key] == token:
                del tokens[key]
                return "Logged out!"


api.add_resource(
    Flights, "/flights/<string:from_addr>/<string:to>", endpoint='flights')

api.add_resource(
    ChangeFlights, "/flights/<int:token>/<string:mode>", endpoint='changeflights')

api.add_resource(
    Login, "/authentication_authorization/<string:login>/<string:password>", endpoint='login')

api.add_resource(
    End, "/end_session/<int:token>", endpoint='end')

if __name__ == "__main__":
    app.run(debug=True)
