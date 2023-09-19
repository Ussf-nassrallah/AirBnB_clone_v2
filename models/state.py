#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        @property
        def cities(self):
            """ getter attribute cities that
            returns the list of City instances with state_id """
            from models import storage
            from models.city import City
            cities_list = []
            all_cities_list = storage.all(City)
            for city in all_cities_list.values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
