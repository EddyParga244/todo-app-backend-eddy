# TODO APP BACKEND

## Description

This project is a backend for the Todo App, using Python and Flask library and MySQL for database, with features such as
authentication, JWT, and data persistence

## Tech Stack

- Python
- Flask 
- Bcrypt
- SQLalchemy
- Marshmallow
- MySQL
- JWT (flask-jwt-extended)
- python-dotenv

## Endpoints

### auth routes

- (POST) /api/auth/register - Register User
- (POST) /api/auth/login - Login User
- (POST) /api/auth/refresh - Refresh token

### todo routes

- (POST) /api/todos - Add todo 
- (GET) /api/todos - Get todos
- (PUT) /api/todos/reorder - Reorder todo
- (DELETE) /api/todos/:todo_id - Delete todo
- (PATCH) /api/todos/:todo_id - Update todo

## Installation

1. Clone repository or download app
2. Create virtual environment with `python -m venv venv`
3. Activate it with `venv\Scripts\activate`
4. Install dependencies with `pip install -r requirements.txt`
5. Create .env file using `.env_template` as template
6. Create database in MySQL
7. Run server with `python app.py`

## Tech decisions

- Flask: Small project, no need for all the advantages of Django
- HTTP-only cookies: Protection againsts XSS attacks, no JavaScript access
- UUID: Harder to brute force compared to incremental IDs