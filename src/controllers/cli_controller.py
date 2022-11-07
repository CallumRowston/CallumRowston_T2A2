from flask import Blueprint
from init import db, bcrypt
from datetime import date, datetime
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
            name='Callum_Rowston',
            email='callum_r@canyon.com',
            password=bcrypt.generate_password_hash('callum123').decode('utf-8')
        ),
        User(
            name='John_Smith',
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
            last_updated=datetime.now()
        ),
        Canyon(
            name='Firefly',
            area='Newnes',
            description='A good canyon to the north of the Wolgan Valley with many short abseils and swims.',
            estimated_time_hrs=8,
            number_abseils=7,
            longest_abseil='20m',
            difficulty='Medium',
            wetsuits_recommended=True,
            last_updated=datetime.now()
        ),
        Canyon(
            name='Rocky Creek',
            area='South Wolgan',
            description='A long, dark and spectacular canyon in the South Wolgan. A great beginner canyon as there is no abseiling required and be easily linked up with Twister Canyon to make up a full day',
            estimated_time_hrs=4,
            number_abseils=0,
            longest_abseil='N/A',
            difficulty='Easy',
            wetsuits_recommended=True,
            last_updated=datetime.now()
        ),
        Canyon(
            name='Twister',
            area='South Wolgan',
            description='A short canyon that runs off Rocky Creek canyon. Features many jumps and slides and no abseils, making it ideal for beginners',
            estimated_time_hrs=3,
            number_abseils=0,
            longest_abseil='N/A',
            difficulty='Easy',
            wetsuits_recommended=True,
            last_updated=datetime.now()
        ),
        Canyon(
            name='Tiger Snake',
            area='South Wolgan',
            description='A narrow twisting canyon with an upper and lower constriction. A usually dry canyon that makes it ideal to do in winter',
            estimated_time_hrs=7,
            number_abseils=5,
            longest_abseil='25m',
            difficulty='Easy-Medium',
            wetsuits_recommended=False,
            last_updated=datetime.now()
        ),
        Canyon(
            name='Whungee Wheengee',
            area='Wollangambe',
            description='An excellent, sustained but difficult canyon with tight constrictions, many short abseils, swims, jumps and possible duck unders in high water.',
            estimated_time_hrs=10,
            number_abseils=6,
            longest_abseil='15m',
            difficulty='Medium-Hard',
            wetsuits_recommended=True,
            last_updated=datetime.now()
        ),
        Canyon(
            name='Claustral',
            area='Carmarthen Labyrinth',
            description='Likely the most impressive canyon in NSW. Three back-to-back abseils lead to a long, sustained moss-covered canyon section lasting up to 1km. A long, difficult day with lots of bouldering, abseiling, swims and a veyr long hike out',
            estimated_time_hrs=10,
            number_abseils=5,
            longest_abseil='20m',
            difficulty='Medium',
            wetsuits_recommended=True,
            last_updated=datetime.now()
        )
    ]

    print("Tables seeded")
    db.session.add_all(users)
    db.session.add_all(canyons)
    db.session.commit()
