from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_TAGS = ('To Do', 'Completed')

class UserCanyon(db.Model):
    __tablename__ = 'user_canyons'

    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date)
    tag = db.Column(db.String, nullable=False)

    # Foreign Keys
    canyon_id = db.Column(db.Integer, db.ForeignKey('canyons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    canyon = db.relationship('Canyon', back_populates='user_canyons')
    user = db.relationship('User', back_populates='user_canyons')

class UserCanyonSchema(ma.Schema):
    # Validation - canyon must be tagged as 'To Do' or 'Completed' otherwise it has no reason to exist in the table
    tag = fields.String(validate=OneOf(VALID_TAGS, error=f'Canyon must be tagged as one of: {VALID_TAGS}'))

    # Only return user id in user field
    user = fields.Nested('UserSchema', only=['id'])
    # Exclude user and comments from canyon field
    canyon = fields.Nested('CanyonSchema', exclude=['user', 'comments'])

    class Meta:
        fields = ('id', 'date_added', 'tag', 'canyon', 'user')
        ordered = True
