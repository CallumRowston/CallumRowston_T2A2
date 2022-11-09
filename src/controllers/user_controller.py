from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import date, timedelta
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@users_bp.route('/<int:id>/')
#jwt_required()
def get_one_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)
    return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/update_account/', methods=['PUT', 'PATCH'])
#jwt_required()
def update_user_self():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)
    return {'error': f'User not found with id {id}'}, 404
