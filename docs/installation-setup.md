# Installation and Setup Guide

## Prerequisites

1. Installation Python3 and pip
2. Installation of PostgreSQL
3. A PostgreSQL Database titled ```canyon_app_db```
4. A PostgreSQL User titled ```canyon_dev``` with full access to the database

## .env and .flaskenv

1. Rename the file ```.env.sample``` to ```.env```
2. Ensure this file contains the DATABASE_URL and JWT_SECRET_KEY
3. Ensure the .flaskenv file contains the following lines:

```
FLASK_APP=main
FLASK_DEBUG=True
FLASK_RUN_PORT=8080
```

If port 8080 is in use, the ```FLASK_RUN_PORT``` variable can be changed to another port.

## Python Virtual Environment

While in the /src directory, execute the following commands to start the virtual environment and install required packages.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database Setup and Seeding

To add the relevant tables and data to the database, from the /src directory enter the following command:

```flask db drop && flask db create && flask db seed```

## Run the server

To run the server, from the /src directory enter the following command:

```flask run```
