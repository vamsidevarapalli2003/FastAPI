from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://deploy_database_mbi7_user:UwRyH78pCa1GP5gZuASrwItGa2wIpkPU@dpg-da6iotn10e5c73bs816g-a.singapore-postgres.render.com/deploy_database_mbi7'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
