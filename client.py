from time import sleep
from pyfiglet import Figlet
import requests
from PyInquirer import prompt
from termcolor import colored
from os import system, name

BASE = "http://127.0.0.1:5000/"


def clearTheConsole():
    input('Press any key to continue...')
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def getFlightInfo():
    questions = [
        {
            'type': 'input',
            'name': 'from',
            'message': f'Where from the plane departures?'
        },
        {
            'type': 'input',
            'name': 'to',
            'message': f'Where to the plane arrives?'
        }
    ]
    answers = prompt(questions)
    fromAddr = answers['from']
    toAddr = answers['to']
    flights = requests.get(BASE + 'flights/' +
                           fromAddr + '/' + toAddr).json()
    if len(flights) > 0:
        counter = 1
        for i in flights:
            print(f"""
{counter} | {i['departure_city']} -> {i['arrival_city']}
{i['departure_time']} UTC -> {i['arrival_time']} UTC
Plane: {i['airplane']} |---| Passengers: {i['passenger_count']}
--------------------------------------------------------------------------
        """)
            counter += 1
        return flights
    else:
        print(colored('No such flight available right now!', 'yellow'))


def main():
    clearTheConsole()
    f = Figlet(font='small', width=100)
    print(f.renderText("Airport Management"))
    questions = [
        {
            'type': 'list',
            'name': 'mode',
            'message': 'Enter the mode you want:',
            'choices': ['Login', 'Check Flight', 'Exit']
        }
    ]
    answers = prompt(questions)

#############################LOGIN##################################
    if answers['mode'] == 'Login':
        def check_pass():
            questions = [
                {
                    'type': 'input',
                    'name': 'login',
                    'message': 'Enter your admin username:'
                },
                {
                    'type': 'password',
                    'name': 'pass',
                    'message': 'Enter your admin password:'
                }
            ]
            credentials = prompt(questions)
            login = credentials['login']
            password = credentials['pass']
            token = int(requests.get(
                BASE + 'authentication_authorization/' + f"{login}/" + password).json())
            if token != 0:
                print(colored('LOGGED IN SUCCESSFULLY!', 'green'))
                return (login, token)
            else:
                print(
                    colored('USERNAME OR PASSWORD IS INCORRECT! TRY AGAIN!', 'red', attrs=['bold']))
                return 0

        login = ""
        token = ""
        answer = check_pass()
        if answer != 0:
            login, token = answer

        else:
            main()

        def processAdmin(token, login):
            clearTheConsole()
            f = Figlet(font='small', width=100)
            print(f.renderText("Airport Management"))
            print(
                f'\nHello {colored(str(login), "green")}! Your admin token is {colored(str(token), "blue", attrs=["underline"])}!')
            questions = [
                {
                    'type': 'list',
                    'name': 'nmode',
                    'message': 'What you want to do now?',
                    'choices': [
                        'Get flight info',
                        'Change flights list',
                        'End the session'
                    ]
                }
            ]
            nmode = prompt(questions)['nmode']

            if nmode == 'End the session':
                def tryLeave():
                    questions = [
                        {
                            'type': 'input',
                            'name': 'token',
                            'message': f'To confirm, enter your token: '
                        }
                    ]
                    tryToken = prompt(questions)['token']
                    if int(token) == int(tryToken):
                        print(requests.get(BASE + 'end_session/' +
                                           tryToken).json() + '\n\n')
                        main()
                    else:
                        print(colored('TOKEN IS INCORRECT!',
                                      'red', attrs=['bold']))
                        tryLeave()
                tryLeave()

            elif nmode == 'Get flight info':
                getFlightInfo()
                processAdmin(token, login)

            elif nmode == 'Change flights list':
                def tryChange():
                    questions = [
                        {
                            'type': 'list',
                            'name': 'choice',
                            'message': 'Select what you want to do with the Flights table',
                            'choices': ['Add a flight', 'Update a flight', 'Delete a flight']
                        }
                    ]
                    answer = prompt(questions)['choice']
                    if answer == 'Add a flight':
                        mode = 'add'
                        questions = [
                            {
                                'type': 'input',
                                'name': 'departure_city',
                                'message': 'Enter the departure city:'
                            },
                            {
                                'type': 'input',
                                'name': 'arrival_city',
                                'message': 'Enter the arrival city:'
                            },
                            #############DEPARTURE############
                            {
                                'type': 'input',
                                'name': 'd_day',
                                'message': 'Enter the departure day:',
                            },
                            {
                                'type': 'list',
                                'name': 'd_month',
                                'message': 'Select the departure month:',
                                'choices': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                            },
                            {
                                'type': 'list',
                                'name': 'd_hour',
                                'message': 'Select the departure hour:',
                                'choices': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                            },
                            {
                                'type': 'list',
                                'name': 'd_minute',
                                'message': 'Select the departure minute:',
                                'choices': ['00', '10', '20', '30', '40', '50']
                            },
                            {
                                'type': 'list',
                                'name': 'd_period',
                                'message': 'Select the departure period:',
                                'choices': ['AM', 'PM']
                            },
                            ################ARRIVAL##################
                            {
                                'type': 'input',
                                'name': 'a_day',
                                'message': 'Enter the arrival day:',
                            },
                            {
                                'type': 'list',
                                'name': 'a_month',
                                'message': 'Select the arrival month:',
                                'choices': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                            },
                            {
                                'type': 'list',
                                'name': 'a_hour',
                                'message': 'Select the arrival hour:',
                                'choices': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                            },
                            {
                                'type': 'list',
                                'name': 'a_minute',
                                'message': 'Select the arrival minute:',
                                'choices': ['00', '10', '20', '30', '40', '50']
                            },
                            {
                                'type': 'list',
                                'name': 'a_period',
                                'message': 'Select the arrival period:',
                                'choices': ['AM', 'PM']
                            },
                            ##################OTHER##################
                            {
                                'type': 'list',
                                'name': 'airplane',
                                'message': 'Enter the airplane model:',
                                'choices': ['Airbus A320', 'Airbus A321', 'Boeing 747', 'Boeing 777', 'Boeing 787']
                            },
                            {
                                'type': 'list',
                                'name': 'passenger_count',
                                'message': 'Enter the passenger count:',
                                'choices': ['200', '250', '300', '350', '400']
                            },
                            {
                                'type': 'input',
                                'name': 'token',
                                'message': 'Enter your admin token to confirm:'
                            }
                        ]
                        data = prompt(questions)
                        d_time = f"{data['d_month']} {data['d_day']} 2021 {data['d_hour']}:{data['d_minute']}{data['d_period']}"
                        a_time = f"{data['a_month']} {data['a_day']} 2021 {data['a_hour']}:{data['a_minute']}{data['a_period']}"
                        jsonData = {
                            'departure_city': data['departure_city'],
                            'arrival_city': data['arrival_city'],
                            'departure_time': d_time,
                            'arrival_time': a_time,
                            'airplane': data['airplane'],
                            'passenger_count': data['passenger_count']
                        }
                        tryToken = data['token']
                        if int(tryToken) == int(token):
                            reply = requests.post(
                                BASE + 'flights/' + tryToken + '/' + mode, json=jsonData).json()
                            print(reply)
                            processAdmin(token, login)
                        else:
                            print(colored("TOKEN IS INCORRECT!", 'red'))
                            tryChange()

                    elif answer == 'Update a flight':
                        mode = 'update'
                        flights = getFlightInfo()
                        nums = []
                        for i in range(len(flights)):
                            nums.append(str(i+1))
                        questions = [
                            {
                                'type': 'rawlist',
                                'name': 'choice',
                                'message': 'Which one do you want to edit?',
                                'choices': nums
                            }
                        ]
                        choice = int(prompt(questions)['choice'])
                        flight = flights[choice-1]
                        choices = ['Departure City', 'Arrival City', 'Time Of Departure',
                                   'Time Of Arrival', 'Plane Model', 'Passengers Count']
                        questions = [
                            {
                                'type': 'list',
                                'name': 'parameter',
                                'message': 'Which parameter do you want to edit?',
                                'choices': choices
                            }
                        ]
                        try_parameter = prompt(questions)['parameter']
                        parameters = {
                            'Departure City': 'departure_city',
                            'Arrival City': 'arrival_city',
                            'Time Of Departure': 'departure_time',
                            'Time Of Arrival': 'arrival_time',
                            'Plane Model': 'airplane',
                            'Passengers Count': 'passenger_count'}
                        parameter = parameters[try_parameter]
                        value = ""
                        tryToken = ""
                        if parameter == 'departure_city':
                            questions = [
                                {
                                    'type': 'input',
                                    'name': 'departure_city',
                                    'message': 'Enter the departure city:'
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            values = prompt(questions)
                            value = values['departure_city']
                            tryToken = values['token']
                        elif parameter == 'arrival_city':
                            questions = [
                                {
                                    'type': 'input',
                                    'name': 'arrival_city',
                                    'message': 'Enter the arrival city:'
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            values = prompt(questions)
                            value = values['arrival_city']
                            tryToken = values['token']
                        elif parameter == 'departure_time':
                            questions = [
                                {
                                    'type': 'input',
                                    'name': 'd_day',
                                    'message': 'Enter the departure day:',
                                },
                                {
                                    'type': 'list',
                                    'name': 'd_month',
                                    'message': 'Select the departure month:',
                                    'choices': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                                },
                                {
                                    'type': 'list',
                                    'name': 'd_hour',
                                    'message': 'Select the departure hour:',
                                    'choices': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                                },
                                {
                                    'type': 'list',
                                    'name': 'd_minute',
                                    'message': 'Select the departure minute:',
                                    'choices': ['00', '10', '20', '30', '40', '50']
                                },
                                {
                                    'type': 'list',
                                    'name': 'd_period',
                                    'message': 'Select the departure period:',
                                    'choices': ['AM', 'PM']
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            data = prompt(questions)
                            value = f"{data['d_month']} {data['d_day']} 2021 {data['d_hour']}:{data['d_minute']}{data['d_period']}"
                            tryToken = data['token']
                        elif parameter == 'arrival_time':
                            questions = [
                                {
                                    'type': 'input',
                                    'name': 'a_day',
                                    'message': 'Enter the arrival day:',
                                },
                                {
                                    'type': 'list',
                                    'name': 'a_month',
                                    'message': 'Select the arrival month:',
                                    'choices': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                                },
                                {
                                    'type': 'list',
                                    'name': 'a_hour',
                                    'message': 'Select the arrival hour:',
                                    'choices': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
                                },
                                {
                                    'type': 'list',
                                    'name': 'a_minute',
                                    'message': 'Select the arrival minute:',
                                    'choices': ['00', '10', '20', '30', '40', '50']
                                },
                                {
                                    'type': 'list',
                                    'name': 'a_period',
                                    'message': 'Select the arrival period:',
                                    'choices': ['AM', 'PM']
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            data = prompt(questions)
                            value = f"{data['a_month']} {data['a_day']} 2021 {data['a_hour']}:{data['a_minute']}{data['a_period']}"
                            tryToken = data['token']
                        elif parameter == 'airplane':
                            questions = [
                                {
                                    'type': 'list',
                                    'name': 'airplane',
                                    'message': 'Enter the airplane model:',
                                    'choices': ['Airbus A320', 'Airbus A321', 'Boeing 747', 'Boeing 777', 'Boeing 787']
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            values = prompt(questions)
                            value = values['airplane']
                            tryToken = values['token']
                        elif parameter == 'passenger_count':
                            questions = [
                                {
                                    'type': 'list',
                                    'name': 'passenger_count',
                                    'message': 'Enter the passenger count:',
                                    'choices': ['200', '250', '300', '350', '400']
                                },
                                {
                                    'type': 'input',
                                    'name': 'token',
                                    'message': 'Enter your admin token to confirm:'
                                }
                            ]
                            values = prompt(questions)
                            value = values['passenger_count']
                            tryToken = values['token']

                        if int(tryToken) == int(token):
                            jsonData = {
                                'departure_city': flight['departure_city'],
                                'arrival_city': flight['arrival_city'],
                                'airplane': flight['airplane'],
                                'passenger_count': flight['passenger_count'],
                                'change': f'{parameter}',
                                'change_to': str(value)
                            }
                            status = requests.post(
                                BASE + 'flights/' + tryToken + '/' + mode, json=jsonData).json()
                            print(colored(status, 'green'))
                            processAdmin(token, login)

                        else:
                            print(colored('YOUR TOKEN IS INCORRECT!', 'red'))
                            tryChange()

                    elif answer == 'Delete a flight':
                        mode = 'delete'
                        flights = getFlightInfo()
                        nums = []
                        for i in range(len(flights)):
                            nums.append(str(i+1))
                        questions = [
                            {
                                'type': 'rawlist',
                                'name': 'choice',
                                'message': 'Which one do you want to edit?',
                                'choices': nums
                            }
                        ]
                        choice = int(prompt(questions)['choice'])
                        flight = flights[choice-1]
                        questions = [
                            {
                                'type': 'input',
                                'name': 'token',
                                'message': 'Enter your admin token to confirm:'
                            }
                        ]
                        values = prompt(questions)
                        tryToken = values['token']
                        if int(tryToken) == int(token):
                            jsonData = {
                                'departure_city': flight['departure_city'],
                                'arrival_city': flight['arrival_city'],
                                'airplane': flight['airplane'],
                                'passenger_count': flight['passenger_count'],
                            }
                            status = requests.post(
                                BASE + 'flights/' + tryToken + '/' + mode, json=jsonData).json()
                            print(colored(status, 'green'))
                            processAdmin(token, login)

                        else:
                            print(colored('YOUR TOKEN IS INCORRECT!', 'red'))
                            tryChange()
                tryChange()

        processAdmin(token, login)
#############################CHECK FLIGHT##################################
    elif answers['mode'] == 'Check Flight':
        getFlightInfo()
        main()

    elif answers['mode'] == 'Exit':
        print(colored('Have a good day!', 'green', attrs=['bold']))
        sleep(2)
        exit()


if __name__ == "__main__":
    main()
