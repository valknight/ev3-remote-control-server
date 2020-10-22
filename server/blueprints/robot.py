from classes.robot import Robot, get_robot
from config import robot_register_key, default_commands
import json
from flask import (
    Blueprint, request, jsonify
)

robot = Blueprint('robot', __name__, url_prefix='/robot')


# TODO: Add robot pairing process, instead of hacky system of having a "key"


@robot.route('', methods=['POST'])
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
    # TODO: Add check if the command data isn't formatted right, and return an error if so
    r = get_robot(robotId)
    # NOTE: In future, commands will be required from robots - this shim is just to allow for older testing scripts to still function
    commands = data.get('commands', default_commands)
    if not r:
        r = Robot(data.get('robotName'), robotId, commands=commands)
        Robot.add_robot(r)
    else:
        if r.getCommands() != commands:
            r.setCommands(commands)
    r.alive()
    return jsonify(r.toDict())


@robot.route('/list')
def get_robots():
    return jsonify(Robot.get_robot_list_as_dict())
