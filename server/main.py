from flask import render_template, Flask, jsonify, session, redirect, request, url_for, flash
from functools import wraps
from random import randint
from classes.robot import Robot, get_robot
import json
from config import robot_register_key, secret_key
app = Flask(__name__)
app.secret_key = secret_key
robots = []


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


def load_commands():
    with open('commands.json', 'r') as f:
        app.config['commands'] = json.loads(f.read())


load_commands()




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
    r = get_robot(robots, robotId)
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
    r = get_robot(robots, robotId)
    if r is None:
        return jsonify({'success': False, 'msg': 'No such robot with ID'}), 400
    commands = request.json
    command_log.append(request.json)
    with open('commands.log.json', 'w') as f:
        f.write(json.dumps(command_log))
    for command in commands:
        if not r.pushButton(command):
            return jsonify('{} cannot be pressed for robot {}'.format(command, robotId)), 400
    print("{}:{}".format(robotId, command))
    return jsonify({
        'robot': robotId,
        'command': command,
        'sent_to_client': True})


@app.route('/get_robots')
def get_robots():
    while True:
        robotDicts = []
        deleted_robot = False
        for i in range(0, len(robots)):
            robot = robots[i]
            if robot.isAlive():
                robotDicts.append(robot.toDict())
            else:
                # This is done so if a robot reconnects with a different command set, it should have been removed by then
                del robots[i]
                deleted_robot = True
                break
        if not deleted_robot:
            break
    return jsonify(robotDicts)


@app.route('/robot', methods=['POST'])
def add_robot():
    data = json.loads(request.json)
    if data.get('robotKey') != robot_register_key:
        print(data.get('robotKey'))
        return jsonify({
            'success': False,
            'msg': 'Invalid robot registration key'
        })
    try:
        robotId = int(data.get('robotId', 'noId'))
    except ValueError:
        return jsonify({
            'success': False,
            'msg': 'robotId must be int'
        })
    if not data.get('robotName'):
        return jsonify({
            'success': False,
            'msg': 'robotName must be included'
        })
    #TODO: Add check if the command data isn't formatted right, and return an error if so
    r = get_robot(robots, robotId)
    #NOTE: In future, commands will be required from robots - this shim is just to allow for older testing scripts to still function
    commands = data.get('commands', app.config['commands'])
    if not r:
        
        r = Robot(data.get('robotName'), robotId, commands=commands)
        robots.append(r)
    else:
        if r.getCommands() != commands:
            r.setCommands(commands)
    r.alive()
    return jsonify(r.toDict())
