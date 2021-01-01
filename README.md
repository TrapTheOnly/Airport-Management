# Airport Management App

## Table Of Contents

1. [About](https://github.com/TrapTheOnly/Airport-Management#about-app)
2. [Installation](https://github.com/TrapTheOnly/Airport-Management#installation)
3. [Usage Guide](https://github.com/TrapTheOnly/Airport-Management#usage-guide)

## About App

This is a simple client-server flask-based application on Python that helps to maintain the working process of an imaginary airport system. You can check available flights in the database, or, if you have an access to an admin account, you can edit the database by adding new flights, as well as updating and deleting them.

## Installation

In terminal window enter:

```
git clone https://github.com/TrapTheOnly/Airport-Management.git
```

To install requirements in terminal window enter:

```
pip install -r requirements.txt
```

## Usage Guide

You need at least 2 seperate terminals being open:

Server Terminal

```C++
python3 server.py
```

Client Terminal

```C++
python3 client.py
```

All other steps are intuitively explained in the client side of the application. You can add admin accounts if you wish. To do so, head to `admin.json` file and add your account as the already existing ones. Currently available admin accounts by default are:

```
______________________
| Logins | Passwords |
|________|___________|
| ismail | 123       |
| GICO   | 0808      |
| admin  | admin     |
|________|___________|
```

To stop server, head to Server Terminal and press `Ctrl+C` in terminal.
