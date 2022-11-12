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

# ~~~~~~~~~~~~~~~~~~~ CANYONS ~~~~~~~~~~~~~~~~~~~~
# GET, POST, PUT, PATCH, DELETE routes for canyons

# Do not need to be a user to use canyon GET routes - Anyone can see a canyon's details
@canyons_bp.route('/')
def get_all_canyons():
    # Returns all canyons and their attributes

    # Query to get all canyons from canyon table and order by id
    stmt = db.select(Canyon).order_by(Canyon.id)
    canyons = db.session.scalars(stmt)
    
    return CanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/<int:id>/')
def get_one_canyon(id):
    # Returns one selected canyon and its attributes

    # Query to get one canyon from canyon table whose id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    if canyon:
        return CanyonSchema().dump(canyon)

    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/<string:difficulty>/')
def get_canyons_difficulty(difficulty):
    # Returns canyons according to difficulty (Easy, Medium, Hard)

    # Query to get all canyons from canyon table whose difficulty attribute matches the string entered in the route
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
    # Allows an admin to create new canyons in the database
    authorize_user()

    data = CanyonSchema().load(request.json, partial=True)

    # Query to return user whose id will be associated with the created canyon
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    # If a user was found by the query, create a new canyon object and commit it to the database
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

@canyons_bp.route('/<int:id>/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_canyon(id):
    # Allows an admin to update canyon details in the database
    authorize_user()

    # Query to return one canyon in canyon table where the canyon id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    data = CanyonSchema().load(request.json, partial=True)

    # If a canyon was found by the query, update any fields given in request and commit changes to the database
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
    # Allows an admin to delete a canyon from the database and its associated comments
    authorize_user()

    # Query to return one canyon in canyon table where the canyon id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    # If a canyon was found by the query, delete it
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'Canyon with id: {id} successfully deleted.'}

    return {'Error': f'Canyon not found with id: {id}'}, 404

# ~~~~~~~~~~~~~~~~~~~ COMMENTS ~~~~~~~~~~~~~~~~~~~~
# GET, POST, PUT, PATCH, DELETE routes for comments

# Do not need to be a user to use comment GET routes - Anyone can see a canyon's comments, but must be logged in to make comments
@canyons_bp.route('/<int:id>/comments/')
def get_all_comments_from_canyon(id):
    # Returns all comments on a selected canyon

    # Query to get all comments from comments table associated with the canyon whose id matches the id entered in the route
    stmt = db.select(Comment).filter_by(canyon_id=id)
    comments = db.session.scalars(stmt)

    # If any comments were found by the query, return them
    if comments:
        return CommentSchema(many=True, exclude=['canyon']).dump(comments)

    return {'Error': f'No comments found for canyon with id: {id}'}, 404

@canyons_bp.route('/comments/<int:comment_id>/')
def get_one_comment(comment_id):
    # Returns a selected comment from a selected canyon

    # Query to get one comment from comment table where the comment_id matches the id entered in the route
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    # If a comment was found by the query, return it
    if comment:
        return CommentSchema(exclude=['canyon']).dump(comment)

    return {'Error': f'Comment not found with id {comment_id}'}, 404

@canyons_bp.route('/comments/user/<int:user_id>/')
def get_all_comments_from_user(user_id):
    # Returns all comments from a selected user

    # Query to get all comments from comments table where the user_id matches the id entered in the route
    stmt = db.select(Comment).filter_by(user_id=user_id)
    comments = db.session.scalars(stmt)

    # If any comments were found by the query, return them
    if comments:
        return CommentSchema(many=True, exclude=['canyon']).dump(comments)

    return {'Error': f'No comments found for user with id {user_id}'}, 404

@canyons_bp.route('/<int:id>/comments/', methods=['POST'])
@jwt_required()
def create_comment_on_canyon(id):
    # Adds a comment to a selected canyon
    data = CommentSchema().load(request.json)

    # Query to get one canyon from canyon table where the id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    # If a canyon was found by the query, create a new comment object with that canyon_id and commit it to the database
    if canyon:
        comment = Comment(
                message = data['message'],
                date_posted = date.today(),
                canyon_id = id,
                user_id = get_jwt_identity()
        )
        db.session.add(comment)
        db.session.commit()
        return {
            "Message": "Comment posted successfully",
            "Comment": CommentSchema(exclude=['canyon']).dump(comment)
        }

    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/comments/<int:comment_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(comment_id):
    # Allows a user to update their own comment

    # Query to get one comment from comment table where the comment_id matches the id entered in the route and user_id matches the id of the logged in user
    stmt = db.select(Comment).where(and_(
        Comment.id == comment_id,
        Comment.user_id == get_jwt_identity()
    ))
    comment = db.session.scalar(stmt)

    data = CommentSchema().load(request.json, partial=True)

    # If a comment was found by the query, update any fields given in request and commit changes to the database
    if comment:
        comment.message = data.get('message') or comment.message
        db.session.commit()
        return {
            "Message": "Comment updated successfully",
            "Comment": CommentSchema(exclude=['canyon']).dump(comment)
        }

    return {'Error': f'Comment not found with id {comment_id}'}, 404

@canyons_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    # Allows a user to delte their own comment

    # Query to get one comment from comment table where the comment_id matches the id entered in the route and user_id matches the id of the logged in user
    stmt = db.select(Comment).where(and_(
        Comment.id == comment_id,
        Comment.user_id == get_jwt_identity()
    ))
    comment = db.session.scalar(stmt)

    # If a comment was found by the query, delete it
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'Message': f'Comment with id: {comment_id} successfully deleted'}

    return {'Error': f'Comment not found with id {comment_id}'}, 404

# ~~~~~~~~~~~~~~~~~~~~~~~~ TO DO AND COMPLETED CANYONS ~~~~~~~~~~~~~~~~~~~~~~~~~
# GET, POST, and DELETE routes for users to tag canyons as 'To Do' or 'Completed'
# Logged in users can see other users 'To Do' and 'Completed' canyons but a user can only add or delete from their own list

@canyons_bp.route('/to_do/<int:user_id>/')
@jwt_required()
def get_user_canyons_to_do(user_id):
    # Returns all canyons that the specified user has tagged 'To Do'

    # Query to get all canyons tagged as 'To Do' from UserCanyon table where the user_id matches the id entered in the route
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.user_id == user_id,
        UserCanyon.tag == 'To Do'
    ))
    canyons = db.session.scalars(stmt)

    return UserCanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/completed/<int:user_id>/')
@jwt_required()
def get_user_canyons_completed(user_id):
    # Returns all canyons that the specified user has tagged 'Completed'

    # Query to get all canyons tagged as 'Completed' from UserCanyon table where the user_id matches the id entered in the route
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.user_id == user_id,
        UserCanyon.tag == 'Completed'
    ))
    canyons = db.session.scalars(stmt)

    return UserCanyonSchema(many=True).dump(canyons)

@canyons_bp.route('/to_do/<int:id>/', methods=['POST'])
@jwt_required()
def add_canyon_to_do(id):
    # Allows a user to add a canyon to their 'To Do' list

    # Query to return one canyon in canyon table where the canyon id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    # If a canyon was found by the query, add it to the UserCanyon table with the tag 'To Do' and the logged in users' id
    if canyon:
        to_do = UserCanyon(
            date_added = date.today(),
            tag = 'To Do',
            canyon_id = id,
            user_id = get_jwt_identity()
        )
        db.session.add(to_do)
        db.session.commit()
        return {
            "Message": "Canyon successfully added to To Do list",
            "Entry": UserCanyonSchema().dump(to_do)
        }

    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/completed/<int:id>/', methods=['POST'])
@jwt_required()
def add_canyon_completed(id):
    # Allows a user to add a canyon to their 'Completed' list

    # Query to return one canyon in canyon table where the canyon id matches the id entered in the route
    stmt = db.select(Canyon).filter_by(id=id)
    canyon = db.session.scalar(stmt)

    # If a canyon was found by the query, add it to the UserCanyon table with the tag 'Completed' and the logged in users' id
    if canyon:
        completed = UserCanyon(
            date_added = date.today(),
            tag = 'Completed',
            canyon_id = id,
            user_id = get_jwt_identity()
        )
        db.session.add(completed)
        db.session.commit()
        return {
            "Message": "Canyon successfully added to Completed list",
            "Entry": UserCanyonSchema().dump(completed)
        }

    return {'Error': f'Canyon not found with id {id}'}, 404

@canyons_bp.route('/to_do/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_canyon_to_do(id):
    # Allows a user to remove a canyon from their 'To Do' list

    # Query to return one UserCanyon entry in UserCanyon table where the:
    # canyon id matches the id entered in the route,
    # user_id matches the logged in user
    # and the user has tagged the canyon as 'To Do'
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.user_id == get_jwt_identity(),
        UserCanyon.tag == 'To Do'
    ))
    canyon = db.session.scalar(stmt)

    # Query to check if the logged in user is not the owner of the UserCanyon entry, but the entry does exist
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.tag == 'To Do'
    ))
    not_owner = db.session.scalar(stmt)

    # Query to check if the entry is not tagged as 'To Do', but the entry does exist and belongs to the user
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.user_id == get_jwt_identity(),
    ))
    not_to_do = db.session.scalar(stmt)

    # If a matching entry was found in UserCanyon table, delete it from the database
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'To Do Canyon with id: {id} successfully removed from To Do list.'}
    
    elif not_owner:
        return {'Message': 'You are not the owner of this entry'}

    elif not_to_do:
        return {'Message': f"Canyon with id {id} not tagged as 'Completed'"}

    else:
        return {'Error': f'Canyon not found with id {id} in To Do list'}, 404

@canyons_bp.route('/completed/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_canyon_completed(id):
    # Allows a user to remove a canyon from their 'Completed' list

    # Query to return one UserCanyon entry in UserCanyon table where the:
    # canyon id matches the id entered in the route,
    # user_id matches the logged in user
    # and the user has tagged the canyon as 'Completed'
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.user_id == get_jwt_identity(),
        UserCanyon.tag == 'Completed'
    ))
    canyon = db.session.scalar(stmt)

    # Query to check if the logged in user is not the owner of the UserCanyon entry, but the entry does exist
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.tag == 'Completed'
    ))
    not_owner = db.session.scalar(stmt)

    # Query to check if the entry is not tagged as 'Completed', but the entry does exist and belongs to the user
    stmt = db.select(UserCanyon).where(and_(
        UserCanyon.canyon_id == id,
        UserCanyon.user_id == get_jwt_identity(),
    ))
    not_completed = db.session.scalar(stmt)

    # If a matching entry was found in UserCanyon table, delete it from the database
    if canyon:
        db.session.delete(canyon)
        db.session.commit()
        return {'Message': f'Completed Canyon with id: {id} successfully removed from Completed list.'}

    elif not_owner:
        return {'Message': 'You are not the owner of this entry'}

    elif not_completed:
        return {'Message': f"Canyon with id {id} not tagged as 'Completed'"}

    else:
        return {'Error': f'Canyon not found with id {id} in Completed list'}, 404
