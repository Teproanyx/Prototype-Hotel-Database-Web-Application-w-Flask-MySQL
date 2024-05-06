from flask import Blueprint, request, redirect, flash, g, render_template, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from .db import get_db
from .auth import require_login

bp = Blueprint("booking", __name__, url_prefix="/booking")

@bp.route('/index')
def index():
    db = get_db()
    db.execute('''SELECT BookingID, RoomNumber, CheckInDate, CheckOutDate, Username 
               FROM Booking NATURAL JOIN Guest''')
    all_bookings = db.fetchall()

    return render_template('booking/index.html', bookings=all_bookings)

@bp.route('/create', methods=('GET', 'POST'))
@require_login
def create():
    if request.method == "POST":
        roomNo = request.form['roomNo']
        checkIn = request.form['checkIn']
        checkOut = request.form['checkOut']
        catererID = request.form['caterer']
        err = None

        err, roomNo, checkIn, checkOut, catererID = validateAndTransform(roomNo, checkIn, checkOut, catererID)
        
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
        
        if catererID:
            db.execute(f"SELECT * FROM Caterer WHERE CatererID = {catererID}")
            if db.fetchone() is None:
                err = "Caterer ID invalid"

        if err is None:
            db.execute(f"SELECT GuestID FROM Guest WHERE Username = {g.user[0]}")
            guestId = db.fetchone()[0]

            db.execute(f'''
                       SELECT PricePerNight FROM Room NATURAL JOIN RoomType 
                       WHERE RoomNumber = {roomNo}
                       ''')
            dayAmount = checkOut - checkIn
            price = dayAmount.days() * db.fetchone()[0]

            db.execute(f'''
                       INSERT INTO Booking 
                       (GuestID, RoomNumber, CatererID, CheckInDate, CheckOutDate, TotalPrice)
                       VALUES
                       ({guestId}, {roomNo}, {catererID}, {checkIn}, {checkOut}, {price})
                       ''')

            return redirect(url_for('booking/index.html'))

        flash(err)

    return render_template('booking/create.html')


def get_booking(id):
    db = get_db()
    db.execute(f"SELECT * FROM Booking WHERE BookingID = {id}")

    booking = db.fetchone()

    db.execute(f"SELECT GuestID FROM Guest WHERE USERNAME = {g.user[0]}")
    gid = db.fetchone()[0]

    if booking is None:
        abort(404, "Booking does not exist")
    elif booking[1] != gid:
        abort(403)
    
    return booking


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@require_login
def update(id):
    booking = get_booking(id)

    if request.method == "POST":
        roomNo = request.form['roomNo']
        checkIn = request.form['checkIn']
        checkOut = request.form['checkOut']
        catererID = request.form['caterer']
        err = None

        err, roomNo, checkIn, checkOut, catererID = validateAndTransform(roomNo, checkIn, checkOut, catererID)
        
        db = get_db()

        db.execute(f"SELECT * FROM Room WHERE RoomNumber = {roomNo}")

        if db.fetchone() is None:
            err = "Room number invalid"
        else:
            db.execute(f'''
                       SELECT CheckInDate, CheckOutDate FROM Booking
                       WHERE RoomNumber = {roomNo} AND BookingID <> {booking[0]}
                       ''')

            for dateRange in db:
                if (dateRange[0] > checkIn and dateRange[0] < checkOut) or (
                    dateRange[1] > checkIn and dateRange[1] < checkOut):
                    err = "Time overlap with already booked bookings"
                    break

        if catererID:
            db.execute(f"SELECT * FROM Caterer WHERE CatererID = {catererID}")
            if db.fetchone() is None:
                err = "Caterer ID invalid"

        if err is None:
            db.execute(f'''
                       SELECT PricePerNight FROM Room NATURAL JOIN RoomType 
                       WHERE RoomNumber = {roomNo}
                       ''')
            dayAmount = checkOut - checkIn
            price = dayAmount.days() * db.fetchone()[0]

            db.execute(f'''
                       UPDATE Booking SET RoomNumber = {roomNo}, CatererID = {catererID},
                       CheckInDate = {checkIn}, CheckOutDate = {checkOut}, TotalPrice = {price}
                       WHERE BookingID = {booking[0]}
                       ''')

            return redirect(url_for('booking/index.html'))

        flash(err)

    return render_template('booking/update.html', original_booking=booking)


def validateAndTransform(roomNo, checkIn, checkOut, catererID):
    err = None

    if not roomNo or not roomNo.isnumeric():
        err = "Room must be selected"
    elif not checkIn:
        err = "Check in date required"
    elif not checkOut:
        err = "Check out date required"
    elif catererID and not catererID.isnumeric():
        err = "Caterer ID must be numeric"

    roomNo = int(roomNo)
    
    if catererID:
        catererID = int(catererID)

    try:
        checkIn = datetime.strptime(checkIn, r'%Y-%m-%d').date()
        checkOut = datetime.strptime(checkOut, r'%Y-%m-%d').date()
    except ValueError:
        err = "Date input error; try again"
    
    return err,roomNo,checkIn,checkOut, catererID


@bp.route('/cancel/<int:id>', methods=('POST',))
@require_login
def cancel(id):
    get_booking(id)

    db = get_db()
    db.execute(f"DELETE FROM Booking WHERE BookingID = {id}")
    
    return redirect(url_for('booking/index.html'))
