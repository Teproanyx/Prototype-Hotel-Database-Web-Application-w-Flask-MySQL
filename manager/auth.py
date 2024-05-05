from flask import Blueprint, request, redirect, url_for, flash, render_template
from mysql.connector import IntegrityError

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phoneno']
        email = request.form['email']

        db = get_db()
        err = None

        if not username:
            err = "Username is required"
        elif not password:
            err = "Password is required"
        elif not firstname:
            err = "First Name is required"
        elif not lastname:
            err = "Last Name is required"
        elif not phone:
            err = "Phone number is required"
        elif not email:
            err = "Email is required"
        elif not phone.isnumeric():
            err = "Phone number needs to be a number"
        
        if err is not None:
            try:
                db.execute(f'''INSERT INTO Guest 
                           (FirstName, LastName, Phone, Email, Username, GuestPassword) 
                           VALUES 
                           ({firstname}, {lastname}, {phone}, {email}, {username}, {password})''')
            except IntegrityError:
                err = f"{username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(err)

    return render_template('auth/register.html')
