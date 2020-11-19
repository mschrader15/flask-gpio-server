from flask import Blueprint, render_template
from flask import send_file


def get_blueprint(hardware_class):

    dashboard_bp = Blueprint('dashboard_bp', __name__)

    @dashboard_bp.route('/')
    def index():
        return render_template('index.html', x_window=100)

    @dashboard_bp.route("/getPlotCSV")
    def plot_csv():
        return send_file('outputs/Adjacency.csv',
                         mimetype='text/csv',
                         attachment_filename='Adjacency.csv',
                         as_attachment=True)

    return dashboard_bp
