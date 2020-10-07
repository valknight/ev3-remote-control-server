

fetch('/static/templates/robotList.mustache')
    .then((response) => response.text())
    .then((template) => {
        function handleRobotData(robots) {
            function renderTemplate(robotId, robotName) {
                var list = document.getElementById("robotSelectionList");
                var rendered = Mustache.render(template, { name: robotName, id: robotId });
                list.innerHTML += (rendered);
            }
            document.getElementById("robotSelectionList").querySelectorAll('.robot-list-item').forEach(e => e.remove());
            if (robots.length == 0) {
                document.getElementById("robotSelectionProgress").style.display = "inherit";
                document.getElementById("noRobotFound").style.display = "inherit";
            }
            else {
                document.getElementById("robotSelectionProgress").style.display = "none";
                document.getElementById("noRobotFound").style.display = "none";
            }
            for (robot of robots) {
                renderTemplate(robot['id'], robot['name']);
            }
        }
        function showRobots() {
            fetch('{{ url_for("get_robots") }}')
                .then(response => response.json())
                .then(data => handleRobotData(data));
        }
        let timer = setInterval(showRobots, 1000)
    });
