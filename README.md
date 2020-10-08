# EV3 Remote Control Server

## Purpose

This project is to provide a server side application for controls and interaction with EV3 robots or other similar robot.

If you want to check out an example for a project that utilises this server, take a look at [EV3-Brick-Controller](https://github.com/valknight/EV3-brick-controller)

## Credits

This would not be possible, or at least as easily possible without the following projects:

- [ev3dev2-lang-python](https://github.com/ev3dev/ev3dev-lang-python)
- [flask](https://flask.palletsprojects.com/)
- [keydrown]()
- [mustache.js]
- [bulma]

## Requirements
The requirements are based off what has been used in testing. You may have luck running it on older versions of Python or an unsupported OS, but no guarantee!

- Linux or macOS running Python 3.8 or higher
    - The setup guide assumes you also have virtual environment support
- If your commanding robot does not have it's own wifi capabilities, you will also need Bluetooth

## Basic Setup

1. Clone this repository
2. Open config.py and change `robot_register_key` and `secret_key`
3. Setup a virtual environment using `python -m venv venv/`
4. Activate the virtual environment with `source venv/bin/activate`
5. Install the requirements with `pip install -r requirements.txt`
6. Run the development server with `python -m server`
7. Login to the server using the code that will be written to the file `joinCode`

## Configuration

- `robot_register_key`
    - This is used by the server and robots so that a robot can communicate. It should be changed from the default, and changed on a regular basis 
- `secret_key`
    - This is used by flask to secure the session cookie. Do not share this at all! It's again recommended to be changed on a regular basis, and in future releases will be randomly generated unless you are in debug mode
- `button_timeout`
    - This the time in milliseconds to assume a button is being held for past the last communication from a client. Modify if people using your server are typically using lower end internet connections, at risk of reducing the ability for fine movement
- `robot_timeout`
    - The amount of time a robot can go without communicating with the server before being marked inactive. Typically when an EV3 is connected over bluetooth, you see latency of around 150ms, so setting this around 500ms should be more than fine.

Robot commands in future will be determined by the robots themselves, hence why that is not a configuration option here.