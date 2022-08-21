

// function ExpirationDisplay(){
//     var getType = document.querySelector("#type").value 
//     if (getType == student){
//         alert("hi");
//     }
// }


function ShowAndHide(){
    var getType = document.querySelector("#type")
    var expirationInput = document.querySelector('#exp-day')
    console.log(getType.value) 
    if(getType.value == 'visitor'){
        expirationInput.style.display = "none";
    }else{expirationInput.style.display = "block";}
    
}