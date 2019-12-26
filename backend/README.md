# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
        - Login Page URL: https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
        - Manager Access Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5USkZOVU01TnpkR09EVTFRVUU0UlRJMU1VWXhPRGMzT0RZeE1rTTRNREJDTmtVd01qQTJNZyJ9.eyJpc3MiOiJodHRwczovL215ZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRlOGZlNjY2YjFhNDAwZWFmOGNmZTQyIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTc3MTA3NzYwLCJleHAiOjE1NzcxMTQ5NjAsImF6cCI6ImoxM3lpd1RuOE12VkZMQWxQWVFBUXdZMExDZVJxTUdWIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.v7uLAYWmuVrtOqvQ-uL0TltQjEy8AmTkqZGbmEpFzdkMWXnF5qfzHNhHLImKrUglwexriY59D-QtMI-dFL7RTWykGZ3uJUi3J6VNVu2aGLsFP-vJWUcC9B158FuHpNyZL-TvU5FK4BbDGMoJGHVZmSLBlbS2m9Kmtl0nQyfvAT9Uj1guTgN-mqdOaFkg1zLd6ZHXQq1Qyrh4h9_Y26Ul-Pb2oijKoCy1hCWj-7ITFA7lR4NJgCTDOr5s5EMIPtV8xkO6T1_M4Ow5h1VNYB8C4s1r4PzBQ6RsWqonycDehPAYFZygTt2Vzjfh-imFPVJNO7-1H2z3isO8cbKb4nB34g
        - Barista Access Token: 
        eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik5USkZOVU01TnpkR09EVTFRVUU0UlRJMU1VWXhPRGMzT0RZeE1rTTRNREJDTmtVd01qQTJNZyJ9.eyJpc3MiOiJodHRwczovL215ZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGI4NjlmZmQ5NmUwZTdmNjI0MjQzIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTc3MzY1ODk1LCJleHAiOjE1NzczNzMwOTUsImF6cCI6ImoxM3lpd1RuOE12VkZMQWxQWVFBUXdZMExDZVJxTUdWIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.ZI09yGVr-f8bg5Obac8TaKoi1-RG5J9NzjvfnZzyQuIvBIKvgZ8eVHyG5OoO4vK2ndH_b9MPPzaB9-he9PevblbqyIo8ke0tmwKk30rdJiUbWJK4kCN3c_3qvN2KfTbtyfdqAU1Wz5iCJKtF5vg2gTe1VfbSefVLQJyqDZ50lz3IZ5Q8t7N3bGjE0gKt1jPCDNeKomtrx0eMYcu6VXOC4vuX3wZ9F8k8WnKm0CMmQSajdr4nBX-z4VifJw3PnvYuCIcHMQ6l3_nMUrFbxMD6eg1-4F7e3BqnvsCxhiAWx-pqtWjWZRUyfCz5jyNhj3ac46SLWfv_6Y5eYneLEQXPOQ
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
