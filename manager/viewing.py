from flask import Blueprint, redirect, render_template, url_for

from .db import get_db

bp = Blueprint("viewing", __name__)

@bp.route('/')
def room():
    db = get_db()
    info_header = ("RoomNumber", "RoomName", r"Price/Night" ,"Detail", "Cleaning Staff")
    
    db.execute(f'''
               SELECT RoomNumber, RoomName, PricePerNight, Detail, FirstName
               FROM Room NATURAL JOIN RoomType NATURAL JOIN Staff
               ''')
    
    return render_template("viewing/viewtable.html", title="Rooms", headers=info_header, 
                           table=db.fetchall())


@bp.route('/staff')
def staff():
    pass