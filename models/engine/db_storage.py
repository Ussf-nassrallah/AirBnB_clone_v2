#!/usr/bin/python3
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import union_all, select


class DBStorage:
    """New  database engine"""
    __engine = None
    __session = None

    def __init__(self):
        """instance methods"""
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        dbName = getenv('HBNB_MYSQL_DB')
        base_url = "mysql+mysqldb://{}:{}@{}:3306/{}"
        self.__engine = create_engine(
            base_url.format(username, password, host, dbName),
            pool_pre_ping=True
        )

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all : get all data from Database """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Review).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objects = self.__session.query(cls)
        return {"{}.{}".format(type(obj).__name__, obj.id): obj
                for obj in objects}

    def new(self, obj):
        """"""
        self.__session.add(obj)

    def save(self):
        """"""
        self.__session.commit()

    def delete(self, obj=None):
        """"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        # Session = scoped_session(session)
        self.__session = scoped_session(session)
