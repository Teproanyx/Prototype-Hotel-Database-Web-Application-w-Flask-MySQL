from flask import Blueprint, render_template

from .db import get_db

bp = Blueprint("viewing", __name__)

@bp.route('/room')
def room():
    db = get_db()
    info_header = ("Room Number", "Room Type", r"Price/Night", "Capacity", "Details", "Cleaning Staff")
    
    db.execute('''
               SELECT RoomNumber, RoomName, PricePerNight, Capacity, Details, FirstName
               FROM Room NATURAL JOIN RoomType NATURAL JOIN Staff
               ORDER BY RoomNumber
               ''')
    
    return render_template("viewing/viewtable.html", title="Rooms", headers=info_header, 
                           table=db.fetchall())


@bp.route('/staff')
def staff():
    db = get_db()
    info_header = ("Staff ID", "First Name", "Last Name", "Phone Number", "Email")
    
    db.execute("SELECT StaffID, FirstName, LastName, Phone, Email FROM Staff")
    
    return render_template("viewing/viewtable.html", title="Staffs", headers=info_header, 
                           table=db.fetchall())

@bp.route('/caterer')
def caterer():
    db = get_db()
    info_header = ("Caterer ID", "Team Name", "Phone Number", "Email")

    db.execute("SELECT CatererID, TeamName, Phone, Email FROM Caterer")

    return render_template("viewing/viewtable.html", title="Caterer Teams", headers=info_header,
                           table=db.fetchall())
