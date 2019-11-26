from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from auth.database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError
from datetime import datetime

auth = SwaggerBlueprint('auth', 'auth', swagger_spec='./auth/auth-specs.yaml')
schema= auth.spec['definitions']
login_schema=schema['Login']
signup_schema=schema['Signup']
id_schema=schema['Id']

"""
This route is used to display the form to let the user login.
"""
@auth.operation('login')
def login():
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    if general_validator('login', request):
        json_data= request.get_json()
        email = json_data['email']
        password = json_data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            return jsonify({'user_id': user.id, 'firstname': user.firstname})
        else:
            return abort(401, description= "Wrong username or password")
    else:
         return abort(400)

"""
This route is used to let a new user signup.
"""
@auth.operation('signup')
def create_user():
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    if general_validator('signup', request):
        json_data= request.get_json()
        firstname = json_data['firstname']
        lastname = json_data['lastname']
        dateofbirth = json_data['dateofbirth']
        email = json_data['email']
        password = json_data['password']
        new_user = User()
        new_user.firstname = firstname
        new_user.lastname = lastname
        new_user.email = email
        new_user.dateofbirth = datetime.strptime(dateofbirth, '%m/%d/%Y')
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'user_id': new_user.id, 'firstname': new_user.firstname})
        except IntegrityError:
            db.session.rollback()
            return abort(409)
    else:
         return abort(400)

def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

def int_validator(string):
    try:
        value= int(string)
    except (ValueError, TypeError):
        return None
    return value

@auth.operation('user_exists')
def user_exists(user_id):
    if int_validator(user_id) == None:
        return "Not Found!", 404 
    q = db.session.query(User).filter(User.user_id == user_id)
    user = q.first()
    if user is None:
        abort(404)
    else:
        return "", 200

def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

def general_validator(op_id, request):
    schema= auth.spec['paths']
    for endpoint in schema.keys():
        for method in schema[endpoint].keys():
            if schema[endpoint][method]['operationId']==op_id:
                op_schema= schema[endpoint][method]['parameters'][0]
                if 'schema' in op_schema:
                    definition= op_schema['schema']['$ref'].split("/")[2]
                    schema= auth.spec['definitions'][definition]
                    try:
                        validate(request.get_json(), schema=schema)
                        return True
                    except ValidationError as error:
                        return False
                else:
                     return True
                     