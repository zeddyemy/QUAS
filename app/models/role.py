from enum import Enum
from slugify import slugify
from sqlalchemy import inspect

from ..extensions import db

class RoleNames(Enum):
    """ENUMS for the name filed in Role Model"""
    SUPER_ADMIN = 'Super Admin'
    ADMIN = 'Admin'
    ANNOTATOR = 'Annotator'

# Association table for the many-to-many relationship
user_roles = db.Table('user_roles',
    db.Column('app_user_id', db.Integer, db.ForeignKey('app_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model):
    """ Role data model """
    id: int = db.Column(db.Integer, primary_key=True)
    name: RoleNames = db.Column(db.Enum(RoleNames), unique=True, nullable=False)
    slug: str = db.Column(db.String(100), unique=True, nullable=False)
    description: str = db.Column(db.String(100), nullable=True)
    
    def __str__(self) -> str:
        return self.name.value.capitalize()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name.value,
            'slug': self.slug,
            'description': self.description,
        }



def create_roles(clear: bool = False) -> None:
    """Creates default roles if the 'role' table doesn't exist.

    Args:
        clear (bool, optional): If True, clears all existing roles before creating new ones. Defaults to False.
    """
    if inspect(db.engine).has_table('role'):
        if clear:
            # Clear existing roles before creating new ones
            Role.query.delete()
            db.session.commit()
        
        for role_name in RoleNames:
            if not Role.query.filter_by(slug=slugify(role_name.value)).first():
                new_role = Role(name=role_name, slug=slugify(role_name.value))
                db.session.add(new_role)
        db.session.commit()
    