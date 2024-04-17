document.addEventListener('DOMContentLoaded', function () {
    let citizenInput = document.getElementById('username_input');
    let passwordInput = document.getElementById('new_password_input');
    let confirmPasswordInput = document.getElementById('confirm_password_input');
    let resetPasswordButton = document.getElementById('button');

    function checkInputs() {
        if (citizenInput && passwordInput && confirmPasswordInput && resetPasswordButton) {
            if (citizenInput.value && passwordInput.value && confirmPasswordInput.value) {
                resetPasswordButton.disabled = false;
                resetPasswordButton.style.opacity = "1";
            } else {
                resetPasswordButton.disabled = true;
                resetPasswordButton.style.opacity = "0.5";
            }
        }
    }

    if (citizenInput && passwordInput && confirmPasswordInput) {
        citizenInput.addEventListener('input', checkInputs);
        passwordInput.addEventListener('input', checkInputs);
        confirmPasswordInput.addEventListener('input', checkInputs);
        checkInputs();
    }

    window.onload = function () {
        const messages = document.querySelectorAll('.django-message');
        if (messages.length != 0) {
            messages.forEach(function (message) {
                alert(message.textContent.trim());
            });
            setTimeout(function () {
                window.location.href = '/login/';
            }, 2000);
        };
    };
});