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


class DBStorage:
    """New  database engine"""
    __engine = None
    __session = None

    def __init__(self):
        """instance methods"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """"""
        if cls:
            cls_list = self.__session.query(cls)
        else:
            cls_list = self.__session.query(City)
            cls_list.extend(self.__session.query(State))
            cls_list.extend(self.__session.query(Review))
            cls_list.extend(self.__session.query(Place))
            cls_list.extend(self.__session.query(User))
            cls_list.extend(self.__session.query(Amenity))

        dictionary = dict()
        for clss in cls_list:
            key = "{}.{}".format(clss.__class__.name, clss.id)
            dictionary[key] = clss
        return dictionary

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

    def close(self):
        """Close scoped session"""
        self.__session.remove()
