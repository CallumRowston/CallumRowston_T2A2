from init import db, ma

class Canyon(db.Model):
    __tablename__ = 'canyons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    area = db.Column(db.String(100))
    description = db.Column(db.String(500))
    estimated_time_hrs = db.Column(db.Integer)
    number_abseils = db.Column(db.Integer, default=0)
    longest_abseil = db.Column(db.String(20), default='N/A')
    difficulty = db.Column(db.String(20))
    wetsuits_recommended = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.Date)

    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # user = db.relationship('User', back_populates='canyons')
    # comments = db.relationship('Comment', back_populates='canyon', cascade='all, delete')

class CanyonSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'area', 'description', 'estimated_time_hrs', 'number_abseils', 'longest_abseil', 'difficulty', 'wetsuits_recommended', 'last_updated')
        ordered = True
