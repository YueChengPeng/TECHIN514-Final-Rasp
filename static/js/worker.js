// worker.js
onmessage = function(e) {
    if (e.data === 'fetchData') {
        fetch('/get_raw')
            .then(response => response.json())
            .then(data => {
                if (data.joystick) {
                    postMessage(data.joystick);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}