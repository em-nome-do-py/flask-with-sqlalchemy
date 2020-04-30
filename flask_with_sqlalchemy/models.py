from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


database = SQLAlchemy()


class User(database.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Todo(database.Model):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', backref='todos')

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'user': self.user.to_dict()
        }
