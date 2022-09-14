var ip = location.host;
var serverAddress = "http://" + ip.toString() + "/status_send"

// var serverAddress = "http://192.168.2.248:5000/status_send"

setInterval(function(){
    console.log(serverAddress)
    var req = new XMLHttpRequest();
    req.open("POST", serverAddress);
    req.setRequestHeader("Content-type", "application/json");
    req.send();
    req.onreadystatechange = function() {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var jsonResponse = JSON.parse(req.responseText);
                document.querySelector("#temp").innerHTML = "object temperature: " + jsonResponse.temp + "°C"
                if (jsonResponse.door == true){
                    iconSrc = "../static/opening_barrier.png"
                } else{ iconSrc = "../static/closing_barrier.png" }
                document.querySelector("#door-status").src = iconSrc
                // document.querySelector("#door-status").innerHTML = "door: " + door
            }               
        }
    };
}, 1000);

