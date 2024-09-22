import os
from sqlalchemy import create_engine # Crear conexiones con BC
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# CREAMOS CONEXIÓN
sqliteName = 'movies.sqlite' # Nombre bd
base_dir = os.path.dirname(os.path.realpath(__file__)) # Path de la base de datos
databaseUrl = f'sqlite:///{os.path.join(base_dir,sqliteName)}'

engine = create_engine(databaseUrl,echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
