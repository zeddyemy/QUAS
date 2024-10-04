'''
This module defines the User model for the database.

It includes fields for the user's email, password, and other necessary information,
as well as methods for password hashing and verification.

@author Emmanuel Olowu
@link: https://github.com/zeddyemy
'''

from enum import Enum
from flask import current_app
from slugify import slugify
from sqlalchemy.orm import backref
from sqlalchemy import inspect, or_
from ..utils.date_time import DateTimeUtils
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..extensions import db
from .media import Media
from .role import Role, RoleNames
from ..utils.helpers.loggers import console_log
from config import Config

class TempUser(db.Model):
    ''' temporary user '''
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=DateTimeUtils.aware_utcnow)
    
    def __repr__(self) -> str:
        return f'<ID: {self.id}, email: {self.email}>'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'date_joined': self.date_joined,
        }

class AppUser(db.Model, UserMixin):
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    password_hash = db.Column(db.String(255), nullable=True)
    two_fa_secret = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime(timezone=True), nullable=False, default=DateTimeUtils.aware_utcnow)
    
    # Relationships
    profile = db.relationship('Profile', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('app_users', lazy='dynamic'), cascade="save-update, merge", single_parent=True)
    
    
    @property
    def password(self) -> AttributeError:
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        '''
        #This returns True if the password is same as hashed password in the database.
        '''
        return check_password_hash(self.password_hash, password)
    
    @property
    def role_names(self) -> list[str]:
        """Returns a list of role names for the user."""
        return [str(role.name.value) for role in self.roles]
    
    def __str__(self) -> str:
        return self.name.capitalize()
    
    @staticmethod
    def add_search_filters(query, search_term):
        """
        Adds search filters to a SQLAlchemy query.
        """
        if search_term:
            search_term = f"%{search_term}%"
            query = query.filter(
                    or_(
                        AppUser.username.ilike(search_term),
                        AppUser.email.ilike(search_term)
                    )
                )
        return query
    
    
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


def create_default_super_admin(clear: bool = False) -> None:
    if inspect(db.engine).has_table('role'):
        super_admin_role = Role.query.filter_by(name=RoleNames.SUPER_ADMIN).first()
        
        if not super_admin_role:
            super_admin_role = Role(
                name=RoleNames.SUPER_ADMIN,
                slug=slugify(RoleNames.SUPER_ADMIN.value)
            )
            db.session.add(super_admin_role)
            db.session.commit()
        
    if inspect(db.engine).has_table('app_user'):
        super_admin = AppUser.query.join(AppUser.roles).filter(Role.name == RoleNames.SUPER_ADMIN).first()
        
        if clear and super_admin:
            # Clear existing super admin before creating new ones
            super_admin.delete()
            db.session.close()
            console_log(data="Super Admin deleted successfully")
            return
        
        if not super_admin:
            super_admin = AppUser(
                username=current_app.config['DEFAULT_SUPER_ADMIN_USERNAME'],
                email='admin@admin.com'
            )
            super_admin.password = current_app.config['DEFAULT_SUPER_ADMIN_PASSWORD']
            super_admin.roles.append(super_admin_role)
            
            db.session.add(super_admin)
            db.session.commit()
            console_log(data="Admin user created with default credentials")
        else:
            console_log(data="Admin user already exists")