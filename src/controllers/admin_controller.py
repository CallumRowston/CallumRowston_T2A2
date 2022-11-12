from flask import Blueprint
from init import db
from models.user import User, UserSchema
from models.comment import Comment
from controllers.auth_controller import authorize_user
from flask_jwt_extended import jwt_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/grant_admin/<int:user_id>/', methods=['PATCH'])
@jwt_required()
def grant_admin_access(user_id):
    # Allows an admin to give admin privileges to another user
    authorize_user()

    # Query to get one user from user table where the user_id matches the id entered in the route
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the query returns a user and the user is already an admin, return the message
    if user and user.is_admin is True:
        return {'Message': 'User is already an admin'}

    # If the query returns a user who is not an admin, give them admin access and commit changes to the database
    elif user:
        user.is_admin = True
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)

    else:
        return {'Message': f'User with id: {user_id} not found'}

@admin_bp.route('/remove_admin/<int:user_id>/', methods=['PATCH'])
@jwt_required()
def remove_admin_access(user_id):
    # Allows an admin to remove admin privileges from another user
    authorize_user()

    # Query to get one user from user table where the user_id matches the id entered in the route
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the query returns a user but the user is not an admin, return the message
    if user and user.is_admin is False:
        return {'Message': 'User does not have admin privileges'}

    # If the query returns a user who is an admin, remove their admin access and commit changes to the database
    elif user:
        user.is_admin = False
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user)

    else:
        return {'Message': f'User with id: {user_id} not found'}

@admin_bp.route('/delete_comment/<int:comment_id>/', methods=['DELETE'])
@jwt_required()
def admin_delete_comment(comment_id):
    # Allows an admin to delete any comment
    authorize_user()

    # Query to get one comment from comment table where the comment_id matches the id entered in the route
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    # If the comment exists, delete it
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'Message': f'Comment with id: {comment_id} successfully deleted'}

    return {'Error': f'Comment not found with id {comment_id}'}, 404
