#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Permission, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.fake import users, posts

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.option('-n', '--number', help='the number of fake users')
def generate_fake_users(number):
    users(number)

@manager.option('-n', '--number', help='the number of fake posts')
def generate_fake_posts(number):
    posts(int(number))

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()

