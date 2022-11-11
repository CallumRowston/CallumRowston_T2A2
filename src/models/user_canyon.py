from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

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
    # canyon = db.relationship('Canyon', back_populates='user_canyons')
    # user = db.relationship('User', back_populates='user_canyons')
    
class UserCanyonSchema(ma.Schema):

    tag = fields.String(validate=OneOf(VALID_TAGS, error=f'Difficulty must be one of: {VALID_TAGS}'))

    user = fields.Nested('UserSchema', only=['id'])
    canyon = fields.Nested('CanyonSchema', only=['id'])

    class Meta:
        fields = ('id', 'date_added', 'tag', 'canyon_id', 'user_id')
        ordered = True
