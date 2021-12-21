from flask import Blueprint, render_template, flash
from .get_program import current, tonight


now_bp = Blueprint('now', __name__)

@now_bp.route('/maintenant')
def now():
    flash("maintenant")
    flash(current)
    return render_template('time.html')


@now_bp.route("/cesoir")
def csoir():
    flash("ce soir")
    flash(tonight)
    return render_template('time.html')