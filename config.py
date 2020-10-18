import json

robot_register_key = "susxrobogals"
secret_key = '4]ds;3]xd;":.s£sideDC"a'
# this is in ms
button_timeout = 300
# this is in ms
robot_timeout = 2000
logname = "logs/log.txt"
try:
    with open('commands.json', 'r') as f:
        default_commands = json.loads(f.read())
except json.decoder.JSONDecodeError:
    default_commands = []