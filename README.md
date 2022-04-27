# Tax Payer

#### Homepage
```
The home  page was created in a way that all tax payer are displayed on the page sorted by the day the tax payer accounts were created.

This also show which accountant the tax payer is registerd under.
```

#### Accountant and Admin

``` 
Accountants/Admins roles where created to be able to handle all tax payers in the system. 
They have the right to add, delete and update a tax payer. 
You need to be logged in to your accountant role before any of this can be handle.
They have a relationship with each and every tax payer registered under them.
They can update the amount being owned by the tax payer.
```

#### Tax Payer
```
They have relationship with the accountants they are registered under.
```


#### Programming Language
[Python](https://www.python.org/) and [Flask](https://flask.palletsprojects.com/en/2.1.x/) was used to create the web api.
Plugins needed includes the following:
```
Flask
Flask-Bcrypt
Flask-Login
Flask-SQLAlchemy
gunicorn
PyMySQL
python-dotenv
SQLAlchemy
```

##### Virtual Environment
A virtual environment is a Python environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments, and (by default) any libraries installed in a “system” Python, i.e., one which is installed as part of your operating system.

It is advisable to use a virtual environment so as to be able to migrate your programme easily.

To do this, migrate to the folder where you run your server from and type ```python -m venv <your virtual environment name>``` e.g ```python -m venv venv```.

##### Flask
Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.

You use ```pip install flask``` to install it in your environment.

##### Flask Bcrypt
Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for your application.

Due to the recent increased prevalence of powerful hardware, such as modern GPUs, hashes have become increasingly easy to crack. A proactive solution to this is to use a hash that was designed to be "de-optimized". Bcrypt is such a hashing facility; unlike hashing algorithms such as MD5 and SHA1, which are optimized for speed, bcrypt is intentionally structured to be slow.

For sensitive data that must be protected, such as passwords, bcrypt is an advisable choice.

You use ```pip install flask-bcrypt``` to install it in your environment.

##### Flask Login
Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods of time.

Flask-Login is not bound to any particular database system or permissions model. The only requirement is that your user objects implement a few methods, and that you provide a callback to the extension capable of loading users from their ID.

You use ```pip install flask-login``` to install it in your environment.

##### Flask SQLAlchemy
Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

You use ```pip install flask-sqlalchemy``` to install it in your environment.

##### Gunicorn
Flask is a microweb framework and as such is not really good for production. As that is where gunicorn comes into play.

Gunicorn is a Python WSGI HTTP Server that uses a pre-fork worker model.

You use ```pip install gunicorn``` to install it in your environment.

##### PyMySQL
PyMySQL is an interface for connecting to a MySQL database server from Python. It implements the Python Database API v2. 0 and contains a pure-Python MySQL client library. The goal of PyMySQL is to be a drop-in replacement for MySQLdb.

It is needed for the application to connect to the database.

You use ```pip install pymysql``` to install it in your environment.

##### Python Dotenv
Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. It helps in the development of applications following the 12-factor principles.

If your application takes its configuration from environment variables, like a 12-factor application, launching it in development is not very practical because you have to set those environment variables yourself.

To help you with that, you can add Python-dotenv to your application to make it load the configuration from a .env file when it is present (e.g. in development) while remaining configurable via the environment:

```
from dotenv import load_dotenv

load_dotenv()
```

You can do the above in any part of your program, but it advisable to use in the configuration file.

You use ```pip install python-dotenv``` to install it in your environment.