var serverAddress
const fs = require("fs");
fs.readFile("/ipAddress.txt", (err, data) => {
    if (err) throw err;
    
    serverAddress = "http://" + data.toString() + ":5000/status_send"
});

// var serverAddress = "http://192.168.2.248:5000/status_send"

var interval = setInterval(function(){
    var req = new XMLHttpRequest();
    req.open("POST", serverAddress);
    req.setRequestHeader("Content-type", "application/json");
    req.send();
    req.onreadystatechange = function() {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var jsonResponse = JSON.parse(req.responseText);
                if (jsonResponse.regisStatus === true){
                    document.querySelector(".move-to-mask-res").classList.remove("disabled")
                    alert("register successfully")
                    clearInterval(interval)
                }
            }
        }
    };
}, 1000);