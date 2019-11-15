from flask import Blueprint, render_template, redirect, request, url_for
from sqlalchemy.exc import IntegrityError
from auth.database import db, User

auth = Blueprint('auth', __name__)

"""
This route is used to display the form to let the user login.
"""
@auth.route('/login', methods=['GET', 'POST'])
def login(message=''):
    #To be redirect directly from API Gateway
    #if not current_user.is_anonymous:
    #    return redirect("/", code=302)
    form = LoginForm()
    form.message = message
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None:
            #Return user id
            return redirect('/')
        else:
            #return 403
            form.message = "User or Password not correct!"
    return render_template('login.html', form=form, notlogged=True)

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
@auth.route('/signup', methods=['GET', 'POST'])
def create_user():
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
