from enum import Enum
from flask import current_app
from slugify import slugify
from sqlalchemy.orm import backref
from sqlalchemy import inspect, or_
from ..utils.date_time import DateTimeUtils, datetime

from ..extensions import db
from ..utils.helpers.loggers import console_log
from config import Config


class Project(db.Model):
    __tablename__ = "project"
    
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    description: str = db.Column(db.Text)
    created_at: datetime = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow)
    
    def __repr__(self) -> str:
        return f'<ID: {self.id}, name: {self.name}>'
    
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
                        Project.name.ilike(search_term),
                        Project.description.ilike(search_term)
                    )
                )
        return query
    
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
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
        }
    
    def to_excel_data(self) -> dict:
        return {
            "Name": self.name,
            'Description': self.description,
            'Date Created': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

