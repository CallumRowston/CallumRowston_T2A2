from flask import Blueprint, request
from controllers.auth_controller import authorize_user
from init import db
from datetime import date
from sqlalchemy import and_
from models.canyon import Canyon, CanyonSchema
from models.user import User, UserSchema
from models.comment import Comment, CommentSchema
from models.user_canyon_todo import UserCanyonToDo, UserCanyonToDoSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

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
    return {'Error': f'Canyon not found with id: {id}'}, 404

@canyons_bp.route('/', methods=['POST'])
@jwt_required()
def create_canyon():
    authorize_user()
    data = CanyonSchema().load(request.json)

    stmt = db.select(User).filter_by(id=get_jwt_identity)
    user = db.session.scalar(stmt)

    if user:
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
            user_id = get_jwt_identity()
        )

        db.session.add(canyon)
        db.session.commit()
        return {
                'Message': 'Canyon added successfully',
                'Canyon': CanyonSchema().dump(canyon)
        }
    return {'Error': 'You must be logged in to add a canyon'}, 404

@canyons_bp.route('/<int:id>/update', methods=['PUT', 'PATCH'])
@jwt_required()
def update_canyon(id):
    authorize_user()
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    data = CanyonSchema().load(request.json, partial=True)
    if canyon:
        canyon.name = data.get('name') or canyon.name
        canyon.area = data.get('area') or canyon.area
        canyon.description = data.get('description') or canyon.description
        canyon.estimated_time_hrs = data.get('estimated_time_hrs') or canyon.estimated_time_hrs
        canyon.number_abseils = data.get('number_abseils') or canyon.number_abseils
        canyon.longest_abseil = data.get('longest_abseil') or canyon.longest_abseil
        canyon.difficulty = data.get('difficulty') or canyon.difficulty
        canyon.wetsuits_recommended = data.get('wetsuits_recommended') or canyon.wetsuits_recommended
        canyon.last_updated = date.today()
        db.session.commit()
        return {
            "Message": f"{canyon.name} Canyon successfully updated",
            "Canyon": CanyonSchema().dump(canyon)
        }
    return {'Error': f'Canyon not found with id: {id}'}, 404

@canyons_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_canyon(id):
    authorize_user()
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'Canyon with id: {id} successfully deleted.'}
    return {'Error': f'Canyon not found with id: {id}'}, 404

# -------------------------
# ~~~~~~~ COMMENTS ~~~~~~~~
# -------------------------

@canyons_bp.route('/<int:id>/comments/')
def get_all_comments_from_canyon(id):
    stmt = db.select(Comment).filter_by(canyon_id=id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)

@canyons_bp.route('/<int:id>/comments/int:comment_id')
def get_one_comment_from_canyon(id, comment_id):
    stmt = db.select(Comment).filter_by(canyon_id=id)
    comment = db.session.scalar(stmt)
    stmt = db.select(Canyon).filter_by(canyon_id=id)
    comment = db.session.scalar(stmt)
    return CommentSchema().dump(comment)


@canyons_bp.route('/<int:id>/comment/', methods=['POST'])
@jwt_required()
def create_comment(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        comment = Comment(
                message = request.json['message'],
                date_posted = date.today(),
                canyon_id = id,
                user_id = get_jwt_identity()
        )
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment)
    return {'error': f'canyon not found with id {id}'}, 404

@canyons_bp.route('/<int:id>/comment/<int:comment_id>/', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_comment(id, comment_id):
    stmt = db.select(Comment).filter_by(id=id)
    comment = db.session.scalar(stmt)

    stmt = db.select(Comment).where(and_(
        Comment.id == comment_id,
        Comment.user_id == get_jwt_identity()
    ))
    comment = db.session.scalar(stmt)
    data = CommentSchema().load(request.json)
    if comment:
        comment.messgae = data['message'] or comment.message
        db.session.commit() 
        return CommentSchema().dump(comment)
    return {'error': f'Comment not found with id {id}'}, 404

# --------------------------------------------
# ~~~~~~~ To Do and Completed Canyons ~~~~~~~~
# --------------------------------------------

@users_bp.route('/<int:id>/add_to_do', methods=['POST'])
@jwt_required()
def add_canyon_todo(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    stmt = db.select(User).filter_by(id=get_jwt_identity)
    user = db.session.scalar(stmt)

    data = UserCanyonToDoSchema().load(request.json)

def add_canyon_completed():
    pass