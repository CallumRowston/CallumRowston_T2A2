from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.canyon import Canyon

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='CanyonAdministrator',
            email='canyon@admin.com',
            password=bcrypt.generate_password_hash('canyon123').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Smith',
            email='johnsmith@canyon.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8')
        )
    ]

    canyons = [
        Canyon(
            name='Starlight',
            area='Newnes',
            description='Impressive canyon with long dark tunnel with glowworms and a bat colony. A very long boulder field and fire trail to hike out means it can be a very long day, so come prepared.',
            estimated_time_hrs=9,
            number_abseils=3,
            longest_abseil='25m',
            difficulty='Medium',
            wetsuits_recommended=False,
            last_updated=
        ),
        Canyon(
            name=,
            area=,
            description=,
            estimated_time_hrs=,
            number_abseils=,
            longest_abseil=,
            difficulty=,
            wetsuits_recommended=,
            last_updated=
        ),
        Canyon(
            name=,
            area=,
            description=,
            estimated_time_hrs=,
            number_abseils=,
            longest_abseil=,
            difficulty=,
            wetsuits_recommended=,
            last_updated=
        ),
        Canyon(
            name=,
            area=,
            description=,
            estimated_time_hrs=,
            number_abseils=,
            longest_abseil=,
            difficulty=,
            wetsuits_recommended=,
            last_updated=
        )
    ]

    print("Tables seeded")
    db.session.add_all(users)
    db.session.commit()
