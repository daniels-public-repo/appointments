from flask import Flask, render_template, request, redirect, jsonify
from att.database import init_db, db_session
from att.models import Appointment
from datetime import datetime, date, time
from json import dumps
app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def hello_world():
    if 'id' in request.form:
        return 'hi'
    return render_template('index.html')


@app.route('/addAppointment', methods=['POST'])
def add_appointment():
    if 'addAppointment' in request.form:
        desc = request.form.get('description')
        appointment_date = request.form.get('date')
        appointment_time = request.form.get('time')
        if appointment_date:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        if appointment_time:
            appointment_time = datetime.strptime(appointment_time, '%H:%M').time()
        new_appointment = Appointment(
            description=desc,
            date=appointment_date,
            time=appointment_time
        )
        db_session.add(new_appointment)
        db_session.commit()
        return redirect('/')


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@app.route('/search', methods=['POST'])
def search():
    query = request.json['params']['search']
    if len(query):
        rows = db_session.query(Appointment).filter(Appointment.description.like("%{}%".format(query))).all()
    else:
        rows = db_session.query(Appointment).all()
    return app.response_class(response=dumps([appt.as_dict() for appt in rows], default=json_serial),
                              status=200,
                              content_type='application/json')


if __name__ == '__main__':
    init_db()
    app.run()
