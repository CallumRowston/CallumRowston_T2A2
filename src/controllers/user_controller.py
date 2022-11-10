from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import date, timedelta
from models.user import User, UserSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@users_bp.route('/<int:id>/')
@jwt_required()
def get_one_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)
    return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    data =  UserSchema().load(request.json, partial=True)
    if user:
        user.name = data.get('name') or user.name
        user.email = data.get('email') or user.email
        if data.get('password'):
            user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
        db.session.commit()
        return {
            "Message": f"User successfully updated",
            "User": UserSchema(exclude=['password']).dump(user)
        }
    return {'error': f'User not found with id {id}'}, 404

def get_user_todo_canyons():
    pass

def get_user_completed_canyons():
    pass
