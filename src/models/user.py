from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    canyons = db.relationship('Canyon', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')
    # to_do = db.relationship('UserCanyonToDo', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    # Validation - name, password, email
    name = fields.String(validate=And(
        Length(min=2, max=50, error='Username must be between 2 and 50 characters long'),
        Regexp('^[a-zA-Z0-9]+$', error='Username can only contain letters and numbers')
    ))

    password = fields.String(validate=(
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',
        error='Password must contain at least eight characters, at least one uppercase letter, one lowercase letter and one number:')
    ))

    # Exclude user from canyon field
    canyons = fields.List(fields.Nested('CanyonSchema', exclude=['user']))
    # Exclude user form comment field
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')
        ordered = True
