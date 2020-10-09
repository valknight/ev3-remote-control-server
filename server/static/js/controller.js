var controls = JSON.parse(document.getElementById('x-controls').innerHTML);
var activeControls = [];
var robotId = document.getElementById('x-robot-id').innerHTML;

function is_touch_enabled() {
    return ('ontouchstart' in window) ||
        (navigator.maxTouchPoints > 0) ||
        (navigator.msMaxTouchPoints > 0);
}

function checkIfAlive() {
    fetch('/get_robots', { method: 'GET' })
        .then(response => response.json())
        .then(function (data) {
            found_robot = false;
            for (robot of data) {
                if (String(robot.id) === robotId) {
                    found_robot = true;
                }
            }
            if (!found_robot) {
                window.location.reload();
            }
        })
}
function doControl() {
    kd.tick();
    activeControls.forEach(function (item, index) {
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(activeControls),
        });
    })
}

function get_control_from_keybind(keybind) {
    for (item of controls) {
        if (item.binding == keybind) {
            return item;
        }
    }
    return undefined;
}

function addControl(commandCode) {
    var index = activeControls.indexOf(commandCode);
    if (index == -1) {

        activeControls.push(commandCode);
    }
}
function releaseControl(commandCode) {
    const index = activeControls.indexOf(commandCode);
    if (index > -1) {
        activeControls.splice(index, 1);
    }
}
// this deals with when a user clicks on a button

document.body.onmousedown = function (evt) {
    if (evt.target.attributes.command !== undefined) {
        controls.forEach(function (item, index) {
            if (evt.target.attributes.command.value == item.code) {
                addControl(item);
            }
        })
    }
}

// handles user touching a button
document.body.ontouchstart = function (evt) {
    if (evt.target.attributes.command !== undefined) {
        controls.forEach(function (item, index) {
            if (evt.target.attributes.command.value == item.code) {
                addControl(item);
            }
        })
    }
}

// handles a user lifting their finger from a button
document.body.ontouchend = function (evt) {
    if (evt.target.attributes.command !== undefined) {
        releaseControl(evt.target.attributes.command.value);
    }
}

// handles a user unclicking (? is that a word) a button
document.body.onmouseup = function (evt) {
    if (evt.target.attributes.command !== undefined) {
        releaseControl(evt.target.attributes.command.value);
        activeControls = [];
    }
}
kd.UP.down(function () {
    addControl(get_control_from_keybind("ArrowUp"));
});
kd.DOWN.down(function () {
    addControl(get_control_from_keybind("ArrowDown"));
});
kd.LEFT.down(function () {
    addControl(get_control_from_keybind("ArrowLeft"));
});
kd.RIGHT.down(function () {
    addControl(get_control_from_keybind("ArrowRight"));
});
// manage releasing of controls
kd.UP.up(function () {
    releaseControl(get_control_from_keybind("ArrowUp"));
});
kd.LEFT.up(function () {
    releaseControl(get_control_from_keybind("ArrowLeft"));
});
kd.RIGHT.up(function () {
    releaseControl(get_control_from_keybind("ArrowRight"));
});
kd.DOWN.up(function () {
    releaseControl(get_control_from_keybind("ArrowDown"));
});

var controlPusher = setInterval(doControl, 20);
// this is run on a seperate interval, as it's not necessary to be doing this check as frequently
var checkIfAliveInterval = setInterval(checkIfAlive, 500);
