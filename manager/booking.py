from flask import Blueprint, request, redirect, flash, g, render_template, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from .db import get_db
from .auth import require_login

bp = Blueprint("booking", __name__, url_prefix="/booking")

@bp.route('/index')
def index():
    db = get_db()
    db.execute('''SELECT BookingID, RoomNumber, CheckInDate, CheckOutDate, TeamName, 
               TotalPrice, Username FROM (Booking NATURAL JOIN Guest)
               LEFT JOIN Caterer on Booking.CatererID = Caterer.CatererID''')
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

        err, roomNo, checkIn, checkOut, catererID = validateAndTransform(
            roomNo, checkIn, checkOut, catererID)
        
        if err is None:
            db = get_db()

            db.execute("SELECT * FROM Room WHERE RoomNumber = %s", (roomNo,))

            if db.fetchone() is None:
                err = "Room number invalid"
            else:
                db.execute("SELECT CheckInDate, CheckOutDate FROM Booking WHERE RoomNumber = %s", 
                           (roomNo,))

                for dateRange in db:
                    if (dateRange['CheckInDate'] > checkIn and dateRange['CheckInDate'] < checkOut) or (
                        dateRange['CheckOutDate'] > checkIn and dateRange['CheckOutDate'] < checkOut):
                        err = "Time overlap with already booked bookings"
                        break
            
            if err is None and catererID:
                db.execute("SELECT * FROM Caterer WHERE CatererID = %s", (catererID,))
                if db.fetchone() is None:
                    err = "Caterer ID invalid"

        if err is None:
            db.execute("SELECT GuestID FROM Guest WHERE Username = %s", (g.user['Username'],))
            guestId = db.fetchone()['GuestID']

            db.execute("SELECT PricePerNight FROM Room NATURAL JOIN RoomType WHERE RoomNumber = %s", 
                       (roomNo,))
            dayAmount = checkOut - checkIn
            price = dayAmount.days * db.fetchone()['PricePerNight']
    
            query = '''
                    INSERT INTO Booking 
                    (GuestID, RoomNumber, CatererID, CheckInDate, CheckOutDate, TotalPrice)
                    VALUES (%(gid)s, %(room)s, %(cid)s, %(cin)s, %(cout)s, %(price)s)
                    '''
            
            values = {
                'gid': guestId,
                'room': roomNo,
                'cid': catererID,
                'cin': checkIn,
                'cout': checkOut,
                'price': price
            }
    
            db.execute(query, values)

            return redirect(url_for('booking.index'))

        flash(err)

    return render_template('booking/create.html')


def get_booking(id):
    db = get_db()
    db.execute("SELECT * FROM Booking WHERE BookingID = %s", (id,))

    booking = db.fetchone()

    db.execute("SELECT GuestID FROM Guest WHERE Username = %s", (g.user['Username'],))
    gid = db.fetchone()['GuestID']

    if booking is None:
        abort(404, "Booking does not exist")
    elif booking['GuestID'] != gid:
        abort(403)
    
    return booking


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@require_login
def edit(id):
    booking = get_booking(id)

    if request.method == "POST":
        roomNo = request.form['roomNo']
        checkIn = request.form['checkIn']
        checkOut = request.form['checkOut']
        catererID = request.form['caterer']
        err = None

        err, roomNo, checkIn, checkOut, catererID = validateAndTransform(
            roomNo, checkIn, checkOut, catererID)

        if err is None:
            db = get_db()

            db.execute("SELECT * FROM Room WHERE RoomNumber = %s", (roomNo,))

            if db.fetchone() is None:
                err = "Room number invalid"
            else:
                query = '''
                        SELECT CheckInDate, CheckOutDate FROM Booking
                        WHERE RoomNumber = %(room)s AND BookingID <> %(book)s
                        '''
                
                values = {
                    'room': roomNo,
                    'book': booking['BookingID']
                }

                db.execute(query, values)

                for dateRange in db:
                    if (dateRange['CheckInDate'] > checkIn and dateRange['CheckInDate'] < checkOut) or (
                        dateRange['CheckOutDate'] > checkIn and dateRange['CheckOutDate'] < checkOut):
                        err = "Time overlap with already booked bookings"
                        break

            if err is None and catererID:
                db.execute("SELECT * FROM Caterer WHERE CatererID = %s", (catererID,))
                if db.fetchone() is None:
                    err = "Caterer ID invalid"

        if err is None:
            db.execute("SELECT PricePerNight FROM Room NATURAL JOIN RoomType WHERE RoomNumber = %s", 
                       (roomNo,))
            dayAmount = checkOut - checkIn
            price = dayAmount.days * db.fetchone()['PricePerNight']

            query = '''
                    UPDATE Booking SET RoomNumber = %(room)s, CatererID = %(cid)s,
                    CheckInDate = %(cin)s, CheckOutDate = %(cout)s, TotalPrice = %(price)s
                    WHERE BookingID = %(bin)s
                    '''
            
            values = {
                'room': roomNo,
                'cid': catererID,
                'cin': checkIn,
                'cout': checkOut,
                'price': price,
                'bin': booking['BookingID']
            }
    
            db.execute(query, values)

            return redirect(url_for('booking.index'))

        flash(err)

    return render_template('booking/edit.html', original_booking=booking)


@bp.route('/cancel/<int:id>', methods=('POST',))
@require_login
def cancel(id):
    get_booking(id)

    db = get_db()
    db.execute("DELETE FROM Booking WHERE BookingID = %s", (id,))
    
    return redirect(url_for('booking.index'))


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

    if err is not None:
        return err, roomNo, checkIn, checkOut, catererID

    roomNo = int(roomNo)
    
    if catererID:
        catererID = int(catererID)
    else:
        catererID = None

    try:
        checkIn = datetime.strptime(checkIn, r'%Y-%m-%d').date()
        checkOut = datetime.strptime(checkOut, r'%Y-%m-%d').date()
    except ValueError:
        err = "Date input error; try again"
    else:
        if checkIn > checkOut:
            err = "Check in date is after check out date"
    
    return err, roomNo, checkIn, checkOut, catererID
