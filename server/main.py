from flask import render_template, Flask, jsonify, session, redirect, request, url_for, flash
from functools import wraps
from random import randint
from classes.robot import Robot
import json
from config import robot_register_key, secret_key, logname
import logging
logging.basicConfig(filename=logname, level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
# Attach blueprints
from server.blueprints.robot import robot
app.register_blueprint(robot)
logging.info("Registered robot blueprint")
app.secret_key = secret_key


def code_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('joinCode') != app.config['joinCode']:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def generate_code(n=6):
    join_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
    app.config['joinCode'] = join_code
    print("Join code: {}".format(join_code))
    with open('joinCode', 'w') as f:
        f.write(app.config['joinCode'])
    return join_code


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form.get('code'):
        session['joinCode'] = request.form.get('code')
    if session.get('joinCode') == app.config['joinCode']:
        return redirect(url_for('robot_selection'))
    if session.get('joinCode') is not None:
        # this means we have an invalid code, and one is set here
        session['joinCode'] = None
        flash('PIN invalid', 'danger')
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('code_entry.html')


@app.route('/command')
@code_required
def robot_selection():
    return render_template('robot_selection.html')


@app.route('/command/<robotId>')
@code_required
def commander(robotId):
    try:
        robotId = int(robotId)
    except ValueError:
        return jsonify({'success': False, 'msg': 'robotId must be int'})
    r = Robot.get_robot(robotId)
    if not r:
        flash('Robot with ID {} is not connected'.format(robotId), 'warning')
        return redirect(url_for('robot_selection'))
    return render_template('controller.html', robotId=robotId, robotName=r.robotName, commands=r.getCommands(), commandsJ=json.dumps(r.getCommands()))

# TODO: rework this to be a endpoint to press a button, and an endpoint to release it\
# Store the time the button was last held, and what button was held
# If a button has been held for over a second without another request from the web controller, we forcefully release the button.
# This allows us to build an endpoint for a robot-bluetooth bridge to get the currently held buttons of a robot


command_log = []


@app.route('/command/<robotId>', methods=['POST'])
@code_required
def handle_command(robotId):
    try:
        robotId = int(robotId)
    except ValueError:
        return jsonify({'success': False, 'msg': 'robotId must be int'}), 400
    r = Robot.get_robot(robotId)
    if r is None:
        return jsonify({'success': False, 'msg': 'No such robot with ID'}), 400
    # TODO: Add lock checks for robots!
    commands = request.json
    command_log.append(request.json)
    with open('commands.log.json', 'w') as f:
        f.write(json.dumps(command_log))
    r.heldButtons = [] # We do this, so that in case we are changing direction, we immediately invalidate the previous input
    for command in commands:
        if not r.pushButton(command):
            return jsonify('{} cannot be pressed for robot {}'.format(command, robotId)), 400
    return jsonify({
        'robot': robotId,
        'command': command,
        'sent_to_client': True})

