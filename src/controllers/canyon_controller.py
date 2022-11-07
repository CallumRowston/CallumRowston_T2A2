from flask import Blueprint, request
from init import db
from datetime import date
from models.canyon import Canyon, CanyonSchema

canyons_bp = Blueprint('canyons', __name__, url_prefix='/canyons')

@canyons_bp.route('/')
def get_all_canyons():
    stmt = db.select(Canyon).order_by(Canyon.id)
    canyons = db.session.scalars(stmt)
    return CanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/<int:id>/')
def get_one_canyon(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        return CanyonSchema().dump(canyon)
    return {'error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/', methods=['POST'])
# @jwt_required()
def create_canyon():
    data = CanyonSchema().load(request.json)

    canyon = Canyon(
        name = data['name'],
        area = data['area'],
        description = data['description'],
        estimated_time_hrs = data['estimated_time_hrs'],
        number_abseils = data['number_abseils'],
        longest_abseil = data['longest_abseil'],
        difficulty = data['difficulty'],
        wetsuits_recommended = data['wetsuits_recommended'],
        last_updated = date.today(),
        # user_id = get_jwt_identity()
    )

    db.session.add(canyon)
    db.session.commit()
    return {
            'message': f'You have added {canyon.name} Canyon successfully',
            'canyon': CanyonSchema().dump(canyon)
    }
    # return CanyonSchema().dump(canyon), 201

@canyons_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_one_canyon(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        canyon.name = request.json.get('name') or canyon.name
        canyon.area = request.json.get('area') or canyon.area
        canyon.description = request.json.get('description') or canyon.description
        canyon.estimated_time_hrs = request.json.get('estimated_time_hrs') or canyon.estimated_time_hrs
        canyon.number_abseils = request.json.get('number_abseils') or canyon.number_abseils
        canyon.longest_abseil = request.json.get('longest_abseil') or canyon.longest_abseil
        canyon.difficulty = request.json.get('difficulty') or canyon.difficulty
        canyon.wetsuits_recommended = request.json.get('wetsuits_recommended') or canyon.wetsuits_recommended
        canyon.last_updated = date.today(),
        db.session.commit()
        return CanyonSchema().dump(canyon)
    return {'error': f'Canyon not found with id: {id}'}, 404

@canyons_bp.route('/<int:id>/', methods=['DELETE'])
# @jwt_required()
def delete_one_canyon(id):
    # authorize()
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'message': f'{canyon.name} Canyon with id: {canyon.id} deleted.'}
    return {'error': f'Canyon not found with id: {id}'}, 404
