from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from mysql.connector import IntegrityError
from werkzeug.security import  generate_password_hash, check_password_hash
import functools

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
                db.execute(f'''
                           INSERT INTO Guest 
                           (FirstName, LastName, Phone, Email, Username, GuestPassword) 
                           VALUES 
                           ({firstname}, {lastname}, {phone}, {email}, {username}, 
                           {generate_password_hash(password)})
                           ''')
            except IntegrityError:
                err = f"{username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(err)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        error = None

        db.execute(f"SELECT Username, GuestPassword FROM Guest WHERE Username = {username}")
        user = db.fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user[1], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['u_id'] = user[0]
            return redirect(url_for('room'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def cached_login_user():
    u_id = session.get('u_id')

    if u_id is None:
        g.user = None
    else:
        cursor = get_db()
        cursor.execute(f"SELECT Username, GuestPassword FROM Guest WHERE Username = {u_id}")
        g.user = cursor.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('room'))


def require_login(view):
    @functools.wraps(view)
    def decorated_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return decorated_view


@bp.route('/edit', methods=('GET', 'POST'))
@require_login
def edit():
    db = get_db()
    username = g.user[0]
    db.execute(f"SELECT FirstName, LastName, Phone, Email FROM Guest WHERE Username = {username}")
    original = db.fetchone()

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phoneno']
        email = request.form['email']
        

        err = None

        if not firstname:
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
            db.execute(f'''
                        UPDATE Guest SET FirstName = {firstname},
                        LastName = {lastname}, Phone = {phone}, Email = {email}
                        WHERE Username = {username}
                        ''')
            return redirect(url_for('booking.index'))

        flash(err)

    return render_template('auth/edit.html', orig=original)
