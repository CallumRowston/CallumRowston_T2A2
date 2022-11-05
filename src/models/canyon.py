from init import db, ma

class Canyon(db.Model):
    __tablename__ = 'canyons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    area = db.Column(db.String(100))
    description = db.Column(db.String(200))
    estimated_time_hrs = db.Column(db.Integer)
    number_abseils = db.Column(db.Integer)
    longest_abseil = db.Column(db.String(20))
    difficulty = db.Column(db.String(20))
    wetsuits_recommended = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.Date)

class CanyonSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'area', 'description', 'estimated_time', 'number_abseils', 'longest_abseil', 'difficulty', 'wetsuits_recommended', 'last_updated')
        ordered = True