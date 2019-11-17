from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from auth.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError

auth = SwaggerBlueprint('auth', 'auth', swagger_spec='./auth/views/auth-specs.yaml')
schema= auth.spec['definitions']
login_schema=schema['Login']
signup_schema=schema['Signup']
"""
This route is used to display the form to let the user login.
"""
@auth.operation('login')
def login():
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    json_data = request.get_json()
    try:
        validate(json_data, schema=login_schema)
    except ValidationError as error:
        return abort(400)
    
    email = json_data['email']
    password = json_data['password']
    q = db.session.query(User).filter(User.email == email)
    user = q.first()
    if user is not None and user.authenticate(password):
        return jsonify({'id': user.id})
    else:
        return abort(401, description= "Wrong username or password")

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
"""
@auth.operation('signup')
def create_user():
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    
    json_data = request.get_json()
    try:
        validate(json_data, schema=signup_schema)
    except ValidationError as error:
        return abort(400)
    
    firstname = json_data['firstname']
    lastname = json_data['lastname']
    dateofbirth = json_data['dateofbirth']
    email = json_data['email']
    password = json_data['password']
    new_user = User(firstname, lastname, dateofbirth, email)
    new_user.set_password(password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return login()
    except IntegrityError:
        db.session.rollback()
        form.message="Seems like this email is already used"

def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
