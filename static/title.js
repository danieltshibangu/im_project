function grabUsername() {
    document.getElementById('text-to-replace').value = document.getElementById("username").innerHTML;
}

document.getElementById("#username")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        document.getElementById("#submit-name").click();
    }
}); 