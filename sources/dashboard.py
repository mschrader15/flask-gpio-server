from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/')
def index():
    return render_template('index.html', x_window=100)
