from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from flask_login import login_user, logout_user, login_required
from ..email import mail_message

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        user.save_user()
        mail_message("Welcome to one minute pitch","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

