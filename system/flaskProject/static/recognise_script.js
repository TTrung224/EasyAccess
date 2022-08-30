var serverAddress = "http://192.168.2.248:5000/status_send"

setInterval(function(){
    var req = new XMLHttpRequest();
    req.open("POST", serverAddress);
    req.setRequestHeader("Content-type", "application/json");
    req.send();
    req.onreadystatechange = function() {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var jsonResponse = JSON.parse(req.responseText);
                document.querySelector("#temp").innerHTML = "object temperature: " + jsonResponse.temp
                if (jsonResponse.door == true){
                    door = "opening"
                } else{ door = "locking" }
                document.querySelector("#door-status").innerHTML = "door: " + door
            }               
        }
    };
}, 1000);