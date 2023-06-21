#!/usr/bin/python3
"""creates new engine DBStorage"""
import os
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """class for database storage engine"""
    __engine = None
    __engine = None

    def __init__(self):
        """Initializes an instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(os.environ.get('HBNB_MYSQL_USER'),
                                          os.environ.get('HBNB_MYSQL_PWD'),
                                          os.environ.get('HBNB_MYSQL_HOST'),
                                          os.environ.get('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        if cls:
            result = self.__session.query(eval(cls)).all()
        else:
            results = self.__session.query(State).all()
            results.extend(self.__session.query(City).all())
        return {f"{type(obj).__name__}.{obj.id}".obj for obj in results}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit(obj)

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)
