from flask import Blueprint
from init import db
from datetime import date
from models.canyon import Canyon, CanyonSchema

canyon_bp = Blueprint('canyons', __name__, url_prefix='/canyons')

@canyon_bp.route('/')
def get_all_canyons():
    stmt = db.select(Canyon).order_by(Canyon.area)
    canyons = db.session.scalars(stmt)
    return CanyonSchema(many=True).dump(canyons)

@canyon_bp.route('/<int:id>/')
def get_one_canyon(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        return CanyonSchema().dump(canyon)
    return {'error': f'canyon not found with id {id}'}, 404

@canyon_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_canyon(id):
    # authorize()
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'message': f'Canyon {canyon.name} deleted successfully'}
    return {'error': f'Canyon not found with id {id}'}, 404
