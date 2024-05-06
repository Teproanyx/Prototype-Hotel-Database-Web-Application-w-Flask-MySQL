from flask import Blueprint, render_template

from .db import get_db

bp = Blueprint("viewing", __name__)

@bp.route('/')
def room():
    db = get_db()
    info_header = ("RoomNumber", "RoomName", r"Price/Night", "Details", "Cleaning Staff")
    
    db.execute(f'''
               SELECT RoomNumber, RoomName, PricePerNight, Details, FirstName
               FROM Room NATURAL JOIN RoomType NATURAL JOIN Staff
               ''')
    
    return render_template("viewing/viewtable.html", title="Rooms", headers=info_header, 
                           table=db.fetchall())


@bp.route('/staff')
def staff():
    db = get_db()
    info_header = ("Staff ID", "First Name", "Last Name", "Phone Number", "Email")
    
    db.execute(f"SELECT Staff ID, First Name, Last Name, Phone, Email FROM Staff")
    
    return render_template("viewing/viewtable.html", title="Staffs", headers=info_header, 
                           table=db.fetchall())

@bp.route('/caterer')
def caterer():
    db = get_db()
    info_header = ("Caterer ID", "Team Name", "Phone Number", "Email")

    db.execute(f"SELECT CatererID, TeamName, Phone, Email FROM Caterer")

    return render_template("viewing/viewtable.html", title="Caterer Teams", headers=info_header,
                           table=db.fetchall())
