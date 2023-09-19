#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        if kwargs:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        cls_name = self.__class__.__name__
        return f'[{cls_name}] ({self.id}) {self.__dict__}'

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        dictionary = self.__dict__.copy()
        if "created_at" in dictionary:
            ca = dictionary["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
            dictionary["created_at"] = ca
        if "updated_at" in dictionary:
            ua = dictionary["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
            dictionary["updated_at"] = ua
        dictionary["__class__"] = self.__class__.__name__
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        models.storage.delete(self)
