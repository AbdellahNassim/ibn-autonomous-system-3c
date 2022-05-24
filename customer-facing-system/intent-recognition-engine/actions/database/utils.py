import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base, User, Service, ServiceType

def create_session(logger):
    """
        This function will try to connect to the intent store database 
        It gets environment variables and create a connection
    """
     # check database user 
    if 'DATABASE_USER' not in os.environ:
        logger.error("DATABASE_USER variable wasn't set")
    database_user = os.environ.get('DATABASE_USER')

    # check database name 
    if 'DATABASE_NAME' not in os.environ:
        logger.error("DATABASE_NAME variable wasn't set")
    database_name = os.environ.get('DATABASE_NAME')

     # check database user password
    if 'DATABASE_PASSWORD' not in os.environ:
        logger.error("DATABASE_PASSWORD variable wasn't set")
    database_password = os.environ.get('DATABASE_PASSWORD')

     # check database port
    if 'DATABASE_PORT' not in os.environ:
        logger.error("DATABASE_USER variable wasn't set")
    database_port = os.environ.get('DATABASE_PORT')

     # check database host
    if 'DATABASE_HOST' not in os.environ:
        logger.error("DATABASE_HOST variable wasn't set")
    database_host = os.environ.get('DATABASE_HOST')

    connectionUrl = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"
    logger.info(f"Connecting to database using {connectionUrl}")
    # create connection
    engine = create_engine(connectionUrl)
    # create scoped session 
    # this is very important to have a unique session for each user
    db = scoped_session(sessionmaker(bind=engine))
    # check if tables exists already 
    if not inspect(engine).has_table("service"):
        logger.info("The Intent store database was found empty So we will create tables")
        # If not then 
        # initialize db 
        initiate_db(logger, engine)
        logger.info("Database empty seeding with data ")
        # And seed it with initial data 
        seed_db(logger, db)    
    return db


def initiate_db(logger, engine):
    """
        Creation of datababase tables from models 
    """
    logger.info("Creating database tables")
    # create the tables based on the models 
    Base.metadata.create_all(engine)

def seed_db(logger, session):
    """
        Seeding database with an initial user and a service type
        #todo Just for testing 
    """
    # Creating user 
    user = User(username="akram09", password="c8fed00eb2e87f1cee8e90ebbe870c190ac3848c")
    # Creating Service Type
    service_type = ServiceType(name="video", provider_name="Netflix", provider_url="https://netflix.com")

    # persisting 
    session.add(user)
    session.add(service_type)
    
    # commit the transaction 
    session.commit()



