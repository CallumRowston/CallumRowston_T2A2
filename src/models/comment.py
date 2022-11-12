from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.Date)

    # Foreign Keys
    canyon_id = db.Column(db.Integer, db.ForeignKey('canyons.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    canyon = db.relationship('Canyon', back_populates='comments')
    user = db.relationship('User', back_populates='comments')
    
class CommentSchema(ma.Schema):

    # Only display username in user field
    user = fields.Nested('UserSchema', only=['name'])
    # Display entire canyon field
    canyon = fields.Nested('CanyonSchema')

    class Meta:
        fields = ('id', 'message', 'date_posted', 'canyon', 'user')
        ordered = True
