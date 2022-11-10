from init import db, ma
from marshmallow import fields

class UserCanyonToDo(db.Model):
    __tablename__ = 'user_canyons_todo'

    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.Date)

    # Foreign Keys
    canyon_id = db.Column(db.Integer, db.ForeignKey('canyons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    canyon = db.relationship('Canyon', back_populates='user_canyons_todo')
    user = db.relationship('User', back_populates='user_canyons_todo')
    
class UserCanyonToDoSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=['name', 'email'])
    canyon = fields.Nested('CanyonSchema')

    class Meta:
        fields = ('id', 'date_added', 'canyon', 'user')
        ordered = True