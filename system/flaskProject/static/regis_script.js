
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if(urlParams.get('error') == 'existed'){
    alert("The user ID has existed in the system");
}else if(urlParams.get('error') == 'wrongId'){
    alert("Something went wrong with user ID or user type");
}else if(urlParams.get('error') == 'wrongDate'){
    alert("Error with expiration date format");
}


document.querySelector(".regis-form").addEventListener("mousemove",function(){
    var getType = document.querySelector("#type")
    var expirationInput = document.querySelector('#exp-day')
    console.log(getType.value) 
    if(getType.value == 'visitor'){
        expirationInput.required = false;
        expirationInput.style.display = 'none';
        document.querySelector('#exp-day-label').style.display = 'none';
    }else{
        expirationInput.style.display = "block";
        expirationInput.required = true;
        document.querySelector('#exp-day-label').style.display = "block";
    } 
})