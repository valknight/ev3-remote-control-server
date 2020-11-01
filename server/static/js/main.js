let isReloading = false;

function reload() {
    if (isReloading) {
        return;
    }
    isReloading = true;
    window.location = window.location;
}

function updateClockBar() {
    e = document.getElementById("menuBarClockText");
    d = new Date();
    e.innerHTML = d.toLocaleTimeString();
    setTimeout(updateClockBar, 1000 / 60);
}

updateClockBar();