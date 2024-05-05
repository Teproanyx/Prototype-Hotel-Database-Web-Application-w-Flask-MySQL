from flask import Blueprint, redirect, render_template, url_for

from .db import get_db

bp = Blueprint("viewing", __name__)

@bp.route('/')
def book():
    pass


@bp.route('/staff')
def staff():
    pass