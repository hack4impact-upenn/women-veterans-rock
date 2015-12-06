#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, ZIPCode, Address, Resource, \
    ResourceReview, Tag, AffiliationTag, ResourceCategoryTag
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

# Import settings from .env file. Must define FLASK_CONFIG
if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, ZIPCode=ZIPCode,
                Address=Address, Tag=Tag,
                ResourceCategoryTag=ResourceCategoryTag,
                AffiliationTag=AffiliationTag)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.option('-n',
                '--fake-count',
                default=10,
                type=int,
                help='Number of each model type to create',
                dest='count')
def add_fake_data(count):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=count)
    ZIPCode.generate_fake()
    Resource.generate_fake()
    ResourceReview.generate_fake(count=count)
    Address.generate_fake()
    AffiliationTag.generate_default()

    # Set a random zip for each user without one.
    User.set_random_zip_codes(User.query.filter_by(zip_code=None).all(),
                              ZIPCode.query.all())
    # Set a random affiliation tag for each user.
    User.set_random_affiliation_tags(User.query.all(),
                                     AffiliationTag.query.all())


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()

    admin_email = 'wvr@gmail.com'
    if User.query.filter_by(email=admin_email).first() is None:
        User.create_confirmed_admin('Default',
                                    'Admin',
                                    admin_email,
                                    'password',
                                    ZIPCode.create_zip_code('19104'))


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production."""
    Role.insert_roles()

if __name__ == '__main__':
    manager.run()
