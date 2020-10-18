from server.util.checks import code_required
import json
from classes.robot import Robot
from flask import render_template, jsonify, redirect, url_for, request, Blueprint, flash

command = Blueprint('command', __name__, url_prefix='/command')


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
    r = Robot.get_robot(robotId)
    if not r:
        flash('Robot with ID {} is not connected'.format(robotId), 'warning')
        return redirect(url_for('command.selection'))
    return render_template('controller.html', robotId=robotId, robotName=r.robotName, commands=r.getCommands(), commandsJ=json.dumps(r.getCommands()))

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
    r = Robot.get_robot(robotId)
    if r is None:
        return jsonify({'success': False, 'msg': 'No such robot with ID'}), 400
    # TODO: Add lock checks for robots!
    commands = request.json
    command_log.append(request.json)
    with open('commands.log.json', 'w') as f:
        f.write(json.dumps(command_log))
    r.heldButtons = []  # We do this, so that in case we are changing direction, we immediately invalidate the previous input
    for command in commands:
        if not r.pushButton(command):
            return jsonify('{} cannot be pressed for robot {}'.format(command, robotId)), 400
    return jsonify({
        'robot': robotId,
        'command': command,
        'sent_to_client': True})
