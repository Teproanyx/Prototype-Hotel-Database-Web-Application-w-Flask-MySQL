from flask import Blueprint, request, redirect, flash, g, render_template, url_for

from .db import get_db
from .auth import require_login

bp = Blueprint("booking", __name__, url_prefix="/booking")