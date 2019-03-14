import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
            }


class University(Base):
    __tablename__ = 'university'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable formate"""
        return {
            'name': self.name,
            'id': self.id
            }


class College(Base):
    __tablename__ = 'college'

    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    address = Column(String(250))
    founded = Column(Integer)
    phone = Column(String(100))
    place = Column(String(250))
    college_id = Column(Integer, ForeignKey('university.id'))
    university = relationship(University)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable formate"""
        return{
            'name': self.name,
            'id': self.id,
            'address': self.address,
            'founded': self.founded,
            'phone': self.phone,
            'place': self.place,
            'college_id': self.college_id
            }
engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(engine)
