## Getting started 
These instructions will get you a copy of the project up and running in your local machine for development and testing purposes.

## Prerequisites
- [Git](https://git-scm.com/download/)
- [Python 3.6 and above](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)


## Installation and running the server

### Setting up and Activating a Virtual Environment
- Navigate to the project directory
- Create a virtual environment `python3 -m venv name_of_your_virtual_environment`
- Create a .env file and put these key=values in it:
```
export ALLOWED_HOST="Allowed hosts for CORS"
export PORT="port number"
```
- Alternatively rename the `.env.sample` to `.env` 
- Load the environment variable `source .env`
- Install dependencies to your virtual environment `pip install -r requirements.txt`
- Start the server by running the command `uvicorn app.main:app --reload`
- Navigate to `localhost:$PORT` to test the endpoints

### Setting up using Docker
- Navigate to the project directory
- Create a .env file and put these key=values in it:
```
export ALLOWED_HOST="Allowed hosts for CORS"
export PORT="port number"
```
- Alternatively rename the `.env.sample` to `.env` 
- In the root folder build the docker image using the command `docker build -t fast-api .`
- To run the application run the command `docker run -p 8000:8000 fast-api`
- Navigate to `localhost:$PORT` to test the endpoints

## Run Tests
-Run the tests and get test coverage using the command `coverage run --source=app -m pytest && coverage report -m`
