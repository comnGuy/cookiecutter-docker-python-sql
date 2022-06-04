# app.py
import uvicorn
from fastapi import FastAPI
from os import getenv
from fastapi.middleware.cors import CORSMiddleware

# from routes import tracker, bandit
from models.db import initialize_db

# Database
TRACKING_DB = getenv('TRACKING_DB', '127.0.0.1:{{cookiecutter.port_db}}/')
USER_DB = getenv('USER_DB', '{{cookiecutter.user_db}}')
PASSWORD_DB = getenv('PASSWORD_DB', '{{cookiecutter.password_db}}')
DATABASE_DB = getenv('DATABASE_DB', '{{cookiecutter.database_name_db}}')

initialize_db(db_url=TRACKING_DB, database_name=DATABASE_DB,
              user_db=USER_DB, password_db=PASSWORD_DB)

app = FastAPI()
# app.include_router(tracker.router)
# app.include_router(bandit.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Host
HOST = getenv('HOST', '0.0.0.0')
PORT = int(getenv('PORT', {{cookiecutter.port_db}}))
DEBUG = int(getenv('DEBUG', 1))
RELOAD = int(getenv('RELOAD', 1))
NUM_WORKERS = int(getenv('NUM_WORKERS', 4))

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=HOST,
        port=PORT,
        access_log=True,
        reload=RELOAD,
        debug=DEBUG,
        workers=NUM_WORKERS
    )
