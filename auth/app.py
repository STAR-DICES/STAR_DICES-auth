import datetime
import json
import os
from auth.views import blueprints
from auth.database import db, User

from flakon import create_app

def start(test = False):
    app=create_app(blueprints=blueprints)
    db.init_app(app)
    db.create_all(app=app)

    with app.app_context():
        # Create first admin user.
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = start()
    app.run()
