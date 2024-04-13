# Qentelli Internship Projects: Password Authentication Prototype

This repository contains the first task from my internship at Qentelli: a prototype of user signup and login written in Python. It stores accounts in MongoDB, hashes passwords with bcrypt, and issues a JSON Web Token (JWT) when an account is created. The prototype runs as a command-line program. The folder name, dependencies, and Dockerfile point to a planned FastAPI service, but that API layer has not been built.

> [!IMPORTANT]
> For security and privacy reasons, Qentelli allowed me to publish only the code in this repository. It is a small part of my internship work.

## Contents

1. [Aim](#aim)
2. [Design](#design)
3. [Implementation](#implementation)
4. [Limitations](#limitations)
5. [Repository structure](#repository-structure)
6. [Running the prototype](#running-the-prototype)

## Aim

The prototype covers two parts of an authentication service: storing passwords so that a leaked database does not reveal them, and issuing a signed token that a server can check later without keeping session state.

## Design

| Concern | Choice | Reason |
| :--- | :--- | :--- |
| Password storage | bcrypt with a random salt per password (`bcrypt.gensalt()`) | Salting defeats precomputed rainbow-table attacks, and bcrypt is deliberately slow, which raises the cost of guessing passwords |
| Session token | JWT signed with HMAC-SHA256 (HS256), expiring after 24 hours | A server can verify the token from its signature alone, without a session table |
| User store | MongoDB, database `users`, collection `users` | One document per user, looked up by username |

Each stored user document has this shape:

```json
{
  "username": "alice",
  "password": "<bcrypt hash, as bytes>",
  "token": "<JWT issued at signup>"
}
```

## Implementation

`app.py` shows a menu with three options: signup, login, and exit.

### Signup

1. Read a username and password from the terminal.
2. Hash the password with bcrypt.
3. Stop if the username already exists.
4. Create a JWT whose payload holds the username and an expiry time 24 hours ahead.
5. Insert the username, hash, and token into MongoDB.

### Login

1. Read a username and password.
2. Look up the user by username.
3. Check the password against the stored hash with `bcrypt.checkpw` and report the result.

The program prints the same message whether the username or the password is wrong, so a failed login does not reveal which usernames exist.

## Limitations

- There is no FastAPI application yet. The Dockerfile starts `uvicorn app:app`, but `app.py` defines no `app` object, so the container exits on start-up. The program runs only as a command-line script.
- A token is created at signup and stored in the database, but it is never shown to the user, and login does not issue one. Nothing in the program verifies a token, so the JWT is not yet used for authentication.
- The signing key is the placeholder string `"your_secret_key"` in the source code. A real deployment would read it from an environment variable or a secrets store.
- `requirements.txt` lists `passlib`, but the code imports `bcrypt` directly, and `passlib` does not install it. Install `bcrypt` as well (see below). `fastapi` and `uvicorn` are listed but not used yet.
- Passwords are read with `input()`, so they appear on screen as the user types. `getpass.getpass()` would hide them.
- `Database/database.sql` defines a PostgreSQL `users` table with first name, last name, email, and password columns. The program does not use it.
- There is no password-strength check, no limit on repeated login attempts, and no automated test.

## Repository structure

| Path | Contents |
| :--- | :--- |
| `app.py` | Signup, login, and JWT generation, with the command-line menu |
| `docker-compose.yml` | Runs MongoDB on port 27017 |
| `dockerfile` | Container image intended for the future FastAPI service |
| `requirements.txt` | Python dependencies |
| `Database/database.sql` | Unused PostgreSQL schema for a `users` table |

## Running the prototype

The program needs Python 3.9 or later and a MongoDB instance on `localhost:27017`.

```bash
# Start MongoDB in Docker
docker-compose up -d

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt bcrypt

# Run the program
python app.py
```

Choose 1 to sign up, 2 to log in, or 3 to exit.
