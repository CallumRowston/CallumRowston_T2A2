from flask import Blueprint
from init import db
from models.user import User, UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/users/')
def get_all_users():
    stmt = db.select(User).order_by(User.id)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    pass

@auth_bp.route('/login/', methods=['POST'])
def login_user():
    pass

def authorize_user():
    # user_id = get_jwt_identity()
    # stmt = db.select(User).filter_by(id=user_id)
    # user = db.session.scalar(stmt)
    # if not user.is_admin:
    #     abort(401)