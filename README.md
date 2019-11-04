# Mobile Catalogue

AngularJS Single Page App to store and retrieve Mobile Catalogue Information. Flask is used to provide Back-end support for app with JSON endpoins. Users can create accounts using their Google accounts (Uses OAuth2 User Authentication).

## Tech Stack

1.  Python
1.  Flask
1.  AngularJS
1.  Bootstrap3
1.  SQLAlchemy

## How To Run

1. Clone this repository
1. Install the required modules using the following command
    
    ```
    $ pip install -r requirements.txt
    ```
1. change working directory to be the folder that contains app.py
1. run this to use flask cli commands
    
    ```
    $ export FLASK_APP=app.py
    ```
1. Initialise database and its tables using
    
    ```
    $ flask initdb
    ```
1. start the application server by
    
    ```
    $ python app.py
    ```

## JSON API Endpoints

1.  To get all categories and their items
    `http://localhost:5000/?json=all`
2.  To get only items under a category
    `http://localhost:5000/?json=category&category={category_name}`

## Features:

1.  Using OAuth2 based user syste to manage site contents
1.  Secured cookie usage
1.  Single Page app using AngualrJS

## ScreenShots:

![Home](./screenshots/after_login.png?raw=true)
![Categories](./screenshots/category_items.png?raw=true)

## Notes while deploying:

- Any database engine can be used for the apllication backend if they are supported by SQLAlchemy and the respective db engine driver is installed. 
- Update the SQLALCHEMY_DATABASE_URI variable in the app.py to use correct connection URI to the database.
- Update the authorised URI section in the Google Credentials and then update the client_secrets.json file.
