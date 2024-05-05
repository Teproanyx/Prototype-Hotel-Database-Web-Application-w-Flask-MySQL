from flask import Blueprint, request, redirect, flash, g, render_template, url_for
from werkzeug.exceptions import abort

from .db import get_db
from .auth import require_login

bp = Blueprint("booking", __name__, url_prefix="/booking")

@bp.route('/index')
def index():
    db = get_db()
    db.execute("SELECT BookingID, RoomNumber, CheckInDate, CheckOutDate, GuestID FROM Booking")
    all_bookings = db.fetchall()

    return render_template('booking/index', bookings=all_bookings)
