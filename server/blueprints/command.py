from server.util.checks import code_required
import json
from classes.robot import Robot
from flask import render_template, jsonify, redirect, url_for, request, Blueprint, flash, session
from classes.robot import get_robot
command = Blueprint('command', __name__, url_prefix='/command')
import time

@command.route('')
@code_required
def selection():
    return render_template('robot_selection.html')


@command.route('/<robotId>')
@code_required
def commander(robotId):
    try:
        robotId = int(robotId)
    except ValueError:
        return jsonify({'success': False, 'msg': 'robotId must be int'})
    r = get_robot(robotId)
    if not r:
        flash('Robot with ID {} is not connected'.format(robotId), 'warning')
        return redirect(url_for('command.selection'))
    if r.isRobotInUse():
        print(session.get('robotLockKey'))
        print(r.lock.keys)
        if not r.lock.validateLock(session.get('robotLockKey')):
            flash("Robot already in use by another client", "danger")
            return redirect(url_for("command.selection"))
        key = session['robotLockKey']
    else:
        key = r.markInUse()
        session['robotLockKey'] = key
    return render_template('controller.html', robotId=robotId, robotName=r.robotName, commands=r.getCommands(), commandsJ=json.dumps(r.getCommands()), robotKey = key)

# TODO: rework this to be a endpoint to press a button, and an endpoint to release it\
# Store the time the button was last held, and what button was held
# If a button has been held for over a second without another request from the web controller, we forcefully release the button.
# This allows us to build an endpoint for a robot-bluetooth bridge to get the currently held buttons of a robot


command_log = []


@command.route('/<robotId>', methods=['POST'])
@code_required
def handle_command(robotId):
    try:
        robotId = int(robotId)
    except ValueError:
        return jsonify({'success': False, 'msg': 'robotId must be int'}), 400
    r = get_robot(robotId)
    if r is None:
        return jsonify({'success': False, 'msg': 'No such robot with ID'}), 400
    # we don't need "isRobotInUse" here, as, if it is in use, our key will be here
    # we only need it up above, to ensure that if someone else wants to control the robot, and we are not present, we hand over control
    if not r.lock.validateLock(session.get('robotLockKey')):
        return jsonify({'success': False, 'msg': 'No permission to use robot of ID {} with key {}'.format(robotId, session.get('key', 'null'))}), 400
    # this means, we have *most certainly* verified the key is in the current lock, so there's at least one person in this session
    r.markInUse()
    commands = request.json
    command_log.append(request.json)
    with open('commands.log.json', 'w') as f:
        f.write(json.dumps(command_log))
    r.heldButtons = []  # We do this, so that in case we are changing direction, we immediately invalidate the previous input
    for command in commands:
        if not r.pushButton(command):
            return jsonify('{} cannot be pressed for robot {}'.format(command, robotId)), 400
    return jsonify({
        'robot': r.toDict(),
        'commands': commands,
        'sent_to_client': True})
