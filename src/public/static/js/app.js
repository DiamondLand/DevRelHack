let form = document.querySelector('form');

form.addEventListener('submit', function(event) {
    let password1 = document.getElementById("password1").value;
    let password2 = document.getElementById("password2").value;

    if (password1 !== password2) {
        document.getElementById("password2").setCustomValidity("Пароли не совпадают");
        event.preventDefault();

        setTimeout(function() {
            document.getElementById("password2").reportValidity();
        }, 1);
    } else {
        document.getElementById("password2").setCustomValidity("");
    }
});