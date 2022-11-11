from flask import Blueprint
from init import db
from models.user import User, UserSchema
from models.comment import Comment
from controllers.auth_controller import authorize_user
from flask_jwt_extended import get_jwt_identity, jwt_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/grant_admin/<int:user_id>/', methods=['PATCH'])
@jwt_required()
def grant_admin_access(user_id):
    # Allows an admin to give admin privileges to another user
    authorize_user()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user and user.is_admin is True:
        return {'Message': 'User is already an admin'}
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
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user and user.is_admin is False:
        return {'Message': 'User does not have admin privileges'}
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
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'Message': f'Comment with id: {comment_id} successfully deleted'}

    return {'Error': f'Comment not found with id {comment_id}'}, 404
