from flask import Blueprint, request, redirect, flash, g, render_template, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from .db import get_db
from .auth import require_login

bp = Blueprint("booking", __name__, url_prefix="/booking")

@bp.route('/index')
def index():
    db = get_db()
    db.execute("SELECT BookingID, RoomNumber, CheckInDate, CheckOutDate, GuestID FROM Booking")
    all_bookings = db.fetchall()

    return render_template('booking/index.html', bookings=all_bookings)

@bp.route('/create', methods=('GET', 'POST'))
@require_login
def create():
    if request.method == "POST":
        roomNo = request.form['roomNo']
        checkIn = request.form['checkIn']
        checkOut = request.form['checkOut']
        guestId = g.user[0]
        err = None

        if not roomNo or not roomNo.isnumeric():
            err = "Room must be selected"
        elif not checkIn:
            err = "Check in date required"
        elif not checkOut:
            err = "Check out date required"

        roomNo = int(roomNo)

        try:
            checkIn = datetime.strptime(checkIn, r'%Y-%m-%d').date()
            checkOut = datetime.strptime(checkOut, r'%Y-%m-%d').date()
        except ValueError:
            err = "Date input error; try again"
        
        db = get_db()

        db.execute(f"SELECT * FROM Room WHERE RoomNumber = {roomNo}")
        if db.fetchone() is None:
            err = "Room number invalid"
        else:
            db.execute(f"SELECT CheckInDate, CheckOutDate FROM Booking WHERE RoomNumber = {roomNo}")

            for dateRange in db:
                if (dateRange[0] > checkIn and dateRange[0] < checkOut) or (
                    dateRange[1] > checkIn and dateRange[1] < checkOut):
                    err = "Time overlap with already booked bookings"
                    break
        

        if err is None:
            db.execute(f'''
                       SELECT PricePerNight FROM Room NATURAL JOIN RoomType 
                       WHERE RoomNumber = {roomNo}
                       ''')
            dayAmount = checkOut - checkIn
            price = dayAmount.days() * db.fetchone()[0]

            db.execute(f'''
                       INSERT INTO Booking 
                       (GuestID, RoomNumber, CheckInDate, CheckOutDate, TotalPrice)
                       VALUES
                       ({guestId}, {roomNo}, {checkIn}, {checkOut}, {price})
                       ''')

            return redirect('booking/index.html')

        flash(err)

    return render_template('booking/create.html')
            