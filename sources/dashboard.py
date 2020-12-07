from flask import Blueprint, render_template
import socket

def get_blueprint(hardware_class):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]

    dashboard_bp = Blueprint('dashboard_bp', __name__)

    @dashboard_bp.route('/')
    def index():
        return render_template('index.html', x_window=100, ip_address=local_ip_address)

    @dashboard_bp.route('/solenoid_1_on')
    def solenoid_one_control_on():
        hardware_class.control_valve(0, 'open')
        return ("nothing")

    @dashboard_bp.route('/solenoid_1_off')
    def solenoid_one_control_off():
        hardware_class.control_valve(0, 'close')
        return ("nothing")

    @dashboard_bp.route('/solenoid_2_on')
    def solenoid_2_control_on():
        hardware_class.control_valve(1, 'open')
        return ("nothing")

    @dashboard_bp.route('/solenoid_2_off')
    def solenoid_2_control_off():
        hardware_class.control_valve(1, 'close')
        return ("nothing")

    # @dashboard_bp.route("/getPlotCSV")
    # def plot_csv():
    #     return send_file('outputs/Adjacency.csv',
    #                      mimetype='text/csv',
    #                      attachment_filename='Adjacency.csv',
    #                      as_attachment=True)
    #
    #
    # @dashboard_bp.route("/record")
    # def record():
    #     hardware_class.record

    return dashboard_bp
