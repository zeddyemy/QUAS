'''
This module defines the User model for the database.

It includes fields for the user's email, password, and other necessary information,
as well as methods for password hashing and verification.

@author Emmanuel Olowu
@link: https://github.com/zeddyemy
@package QUAS
'''

from enum import Enum
from sqlalchemy.orm import backref
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .media import Media
from config import Config

class TempUser(db.Model):
    ''' temporary user '''
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'<ID: {self.id}, email: {self.email}>'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'date_joined': self.date_joined,
        }

class AppUser(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    password_hash = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    two_fa_secret = db.Column(db.String(255), nullable=True)
    
    # Relationships
    profile = db.relationship('Profile', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('app_users', lazy='dynamic'), cascade="all, delete-orphan", single_parent=True)
    
    
    @property
    def password(self) -> AttributeError:
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password) -> bool:
        '''
        #This returns True if the password is same as hashed password in the database.
        '''
        return check_password_hash(self.password_hash, password)
    
    @property
    def role_names(self) -> list[str]:
        """Returns a list of role names for the user."""
        return [str(role.name.value) for role in self.roles]
    
    
    def __repr__(self) -> str:
        return f'<ID: {self.id}, username: {self.username}, email: {self.email}>'
    
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined,
            'roles': self.role_names,
        }


class Profile(db.Model):
    __tablename__ = "profile"
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(200), nullable=True)
    lastname = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    
    profile_picture_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=True)
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False,)
    
    app_user = db.relationship('AppUser', back_populates="profile")
    profile_picture = db.relationship('Media', backref='profile_picture')
    
    def __repr__(self):
        return f'<profile ID: {self.id}, name: {self.firstname}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    @property
    def profile_pic(self) -> str:
        if self.profile_picture_id:
            theImage = Media.query.get(self.profile_picture_id)
            return theImage.get_path() if theImage else ""
        else:
            return ''
    
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'phone': self.phone,
            'birthday': self.birthday,
            'profile_picture': self.profile_pic,
        }


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    currency_code = db.Column(db.String(50), nullable=True)
    
    app_user_id = db.Column(db.Integer, db.ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False,)
    app_user = db.relationship('AppUser', back_populates="address")
    
    def __repr__(self):
        return f'<address ID: {self.id}, country: {self.country}, LGA: {self.city}, user ID: {self.app_user_id}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'country': self.country,
            'state': self.state,
            'city': self.city,
        }