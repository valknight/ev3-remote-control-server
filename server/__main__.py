from server.blueprints.command import command
from server.blueprints.robot import robot
from flask import render_template, Flask, session, redirect, request, url_for, flash, g
import json
import logging

from config import secret_key, logname
from server.util.checks import get_code

logging.basicConfig(filename=logname, level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
app.secret_key = secret_key

# Attach blueprints
app.register_blueprint(robot)
logging.info("Registered robot blueprint")
app.register_blueprint(command)
logging.info("Registered command blueprint")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form.get('code'):
        session['joinCode'] = request.form.get('code')
    if session.get('joinCode') == get_code():
        return redirect(url_for('command.selection'))
    if session.get('joinCode') is not None:
        # this means we have an invalid code, and one is set here
        session['joinCode'] = None
        flash('PIN invalid', 'danger')
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('code_entry.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)