function validate(event){
    v = document.getElementById("email").value;
    if(v.indexOf("@") == -1){
        event.preventDefault();
        alert("Enter a valid email")
        return false;
    }
    return true;
}