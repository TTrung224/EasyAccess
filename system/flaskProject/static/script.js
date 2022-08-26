
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if(urlParams.get('error') == 'existed'){
    alert("Id existed");
}else if(urlParams.get('error') == 'wrongId'){
    alert("Wrong ID");
}else if(urlParams.get('error') == 'wrongDate'){
    alert("Wrong date");
}



function ShowAndHide(){
    var getType = document.querySelector("#type")
    var expirationInput = document.querySelector('#exp-day')
    console.log(getType.value) 
    if(getType.value == 'visitor'){
        expirationInput.required = false;
        expirationInput.style.display ='none';
    }else{expirationInput.style.display = "block";
    expirationInput.required = true;
    }
    
}