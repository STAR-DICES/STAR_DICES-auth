from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from auth.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = SwaggerBlueprint('auth', __name__, swagger_spec='./auth/views/auth-specs.yaml')

"""
This route is used to display the form to let the user login.
"""
@auth.operation('login')
def login(body):
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    print(body)
    q = db.session.query(User).filter(User.email == body.email)
    user = q.first()
    if user is not None and user.authenticate(body.password):
        return jsonify({'id': user.id})
    else:
        return abort(403)

def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

"""
This route is used to let the user logout.
#This route should be directly handled from API gateway#
"""
#@auth.route("/logout")
#@login_required
#def logout():
#    logout_user()
#    return redirect('/')

"""
This route is used to let a new user signup.

@quizzes.operation('signup')
def create_user(firstname, lastname, email, dateofbirth, password):
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    form = UserForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            return login()
        except IntegrityError:
            db.session.rollback()
            form.message="Seems like this email is already used"
            
    return render_template('create_user.html', form=form, notlogged=True)

"""
