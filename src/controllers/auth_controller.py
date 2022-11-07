from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/users/')
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    data = UserSchema().load(request.json)
    try:
        user = User(
            name = data['name'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'error': F'User with {user.email} already exists'}, 409

@auth_bp.route('/login/', methods=['POST'])
def login_user():
    pass

def authorize_user():
    # user_id = get_jwt_identity()
    # stmt = db.select(User).filter_by(id=user_id)
    # user = db.session.scalar(stmt)
    # if not user.is_admin:
    #     abort(401)