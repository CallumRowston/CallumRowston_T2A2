from flask import Blueprint
from init import db
from datetime import date
from models.canyon import Canyon, CanyonSchema

canyons_bp = Blueprint('canyons', __name__, url_prefix='/canyons')

@canyons_bp.route('/')
def get_all_canyons():
    stmt = db.select(Canyon).order_by(Canyon.area)
    canyons = db.session.scalars(stmt)
    return CanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/<int:id>/')
def get_one_canyon(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        return CanyonSchema().dump(canyon)
    return {'error': f'canyon not found with id {id}'}, 404
