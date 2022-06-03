from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_engine = None
SessionLocal = None 
Base = declarative_base() 

""" 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
"""

def initialize_db(db_url, database_name, user_db, password_db):
    global db_engine
    global Base
    global SessionLocal

    database_uri = f'mysql+mysqlconnector://{user_db}:{password_db}@{db_url}{database_name}'
    db_engine = create_engine(database_uri)

    Base.metadata.create_all(bind=db_engine)

def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)() # SessionLocal()
    #db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_db(app):
    db.init_app(app)
    db.create_all() # Create sql tables for our data models 
"""