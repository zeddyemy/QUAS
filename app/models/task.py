from enum import Enum
from flask import current_app
from slugify import slugify
from sqlalchemy.orm import backref
from sqlalchemy import inspect, or_
from ..utils.date_time import DateTimeUtils, datetime

from ..extensions import db
from .media import Media
from .role import Role, RoleNames
from ..utils.helpers.loggers import console_log
from config import Config


class Task(db.Model):
    __tablename__ = "task"
    
    id: int = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=True)
    project_id: int = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at: datetime = db.Column(db.DateTime(timezone=True), default=DateTimeUtils.aware_utcnow)
    

    media = db.relationship('Media', backref='task_media')
    annotation = db.relationship('Annotation', backref='task', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Task {self.id} in Project {self.project_id}>'
    
    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def get_task_media(self):
        if self.media_id:
            the_media = Media.query.get(self.media_id)
            if the_media:
                return the_media.get_path()
            else:
                return None
        else:
            return None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'image_url': self.get_task_media(),
            'created_at': self.created_at,
            'annotation': self.annotation.to_dict() if self.annotation else None
        }
    
    def to_excel_data(self) -> dict:
        return {
            'Image URL': self.image_url,
            'Date Created': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

