from flask import Blueprint, request
from controllers.auth_controller import authorize_user
from init import db
from datetime import date
from sqlalchemy import and_
from models.canyon import Canyon, CanyonSchema
from models.user import User
from models.comment import Comment, CommentSchema
from models.user_canyon import UserCanyon, UserCanyonSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

canyons_bp = Blueprint('canyons', __name__, url_prefix='/canyons')

# ~~~~~~~ CANYONS ~~~~~~~~
# GET, POST, PUT, PATCH, DELETE routes for canyons

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
    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/<string:difficulty>/')
def get_canyons_difficulty(difficulty):
    # Returns canyons according to difficulty (Easy, Medium, Hard)
    stmt = db.select(Canyon).filter_by(difficulty=difficulty)
    canyons = db.session.scalars(stmt)
    if canyons:
        return {
                    'Message': f'All {difficulty} canyons successfully found',
                    'Canyon': CanyonSchema(many=True).dump(canyons)
            }
    return {'Error': f'No canyons found with difficulty: {difficulty}'}, 404

@canyons_bp.route('/', methods=['POST'])
@jwt_required()
def create_canyon():
    authorize_user()
    data = CanyonSchema().load(request.json, partial=True)

    stmt = db.select(User).filter_by(id=get_jwt_identity())
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
            "Message": "Canyon updated successfully",
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

# ~~~~~~~ COMMENTS ~~~~~~~~
# GET, POST, PUT, PATCH, DELETE routes for comments

@canyons_bp.route('/<int:id>/comments/')
def get_all_comments_from_canyon(id):
    stmt = db.select(Comment).filter_by(canyon_id=id)
    comments = db.session.scalars(stmt)
    if comments:
        return CommentSchema(many=True).dump(comments)
    return {'Error': f'No comments found for canyon with id: {id}'}, 404

@canyons_bp.route('/<int:id>/comments/<int:comment_id>')
def get_one_comment_from_canyon(id, comment_id):
    stmt = db.select(Comment).where(and_(
        Canyon.id == id,
        Comment.id == comment_id
    ))
    comment = db.session.scalar(stmt)
    if comment:
        return CommentSchema().dump(comment)
    return {'Error': f'Comment not found with id {comment_id}'}, 404

@canyons_bp.route('/comments/<int:user_id>/')
def get_all_comments_from_user(user_id):
    stmt = db.select(Comment).filter_by(user_id=user_id)
    comments = db.session.scalars(stmt)
    if comments:
        return CommentSchema().dump(comments)
    return {'Error': f'No comments found for user with id {user_id}'}, 404

@canyons_bp.route('/<int:id>/comments/', methods=['POST'])
@jwt_required()
def create_comment_on_canyon(id):
    data = CommentSchema().load(request.json)
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        comment = Comment(
                message = data['message'],
                date_posted = date.today(),
                canyon_id = id,
                user_id = get_jwt_identity()
        )
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment)
    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/comments/<int:comment_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(comment_id):
    stmt = db.select(Comment).where(and_(
        Comment.id == comment_id,
        Comment.user_id == get_jwt_identity()
    ))
    comment = db.session.scalar(stmt)
    data = CommentSchema().load(request.json, partial=True)
    if comment:
        comment.message = data.get('message') or comment.message
        db.session.commit()
        return CommentSchema().dump(comment)
    return {'Error': f'Comment not found with id {comment_id}'}, 404

@canyons_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    stmt = db.select(Comment).where(and_(
        Comment.id == comment_id,
        Comment.user_id == get_jwt_identity()
    ))
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'Message': f'Comment with id: {comment_id} successfully deleted'}
    return {'Error': f'Comment not found with id {comment_id}'}, 404

# ~~~~~~~ To Do and Completed Canyons ~~~~~~~~
# GET, POST, and DELETE routes for users to tag canyons as 'To Do' or 'Completed'

@canyons_bp.route('/to_do/<int:id>/')
@jwt_required()
def get_user_canyons_to_do(id):
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.user_id == id,
        UserCanyon.tag == 'To Do'
    ))
    canyons = db.session.scalars(stmt)
    return UserCanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/completed/<int:id>/')
@jwt_required()
def get_user_canyons_completed(id):
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.user_id == id,
        UserCanyon.tag == 'Completed'
    ))
    canyons = db.session.scalars(stmt)
    return UserCanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/to_do/add/<int:id>/', methods=['POST'])
@jwt_required()
def add_canyon_to_do(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        to_do = UserCanyon(
            date_added = date.today(),
            tag = 'To Do',
            canyon_id = id,
            user_id = get_jwt_identity()
        )
        db.session.add(to_do)
        db.session.commit()
        return UserCanyonSchema().dump(to_do)
    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/completed/add/<int:id>/', methods=['POST'])
@jwt_required()
def add_canyon_completed(id):
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        to_do = UserCanyon(
            date_completed = date.today(),
            tag = 'Completed',
            canyon_id = id,
            user_id = get_jwt_identity()
        )
        db.session.add(to_do)
        db.session.commit()
        return UserCanyonSchema().dump(to_do)
    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/to_do/delete/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_canyon_to_do(id):
    stmt = db.select(UserCanyon).filter_by(canyon_id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'To Do Canyon with id: {id} successfully removed from To Do table.'}
    return {'Error': f'Canyon not found with id {id} in To Do list'}, 404

@canyons_bp.route('/completed/delete/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_canyon_completed(id):
    stmt = db.select(UserCanyon).filter_by(canyon_id=id)
    canyon = db.session.scalar(stmt)
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'Completed Canyon with id: {id} successfully removed from Completed table.'}
    return {'Error': f'Canyon not found with id {id} in Completed list'}, 404