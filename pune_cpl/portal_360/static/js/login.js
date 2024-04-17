function showRegister() {
    window.location.href = '/register/';
}

document.addEventListener('DOMContentLoaded', function () {
    let citizenInput = document.getElementById('username_input');
    let passwordInput = document.getElementById('password_input');
    let loginButton = document.getElementById('button');
    let resendButton = document.getElementById('resend-otp-button');
    let timerElement = document.getElementById('timer');

    if (document.querySelector('.otp.form')) {
        document.querySelector('.otp.form').scrollIntoView({ behavior: 'smooth' });
    }

    function checkInputs() {
        if (citizenInput && passwordInput && loginButton) {
            if (citizenInput.value && passwordInput.value) {
                loginButton.disabled = false;
                loginButton.style.opacity = "1";
            } else {
                loginButton.disabled = true;
                loginButton.style.opacity = "0.5";
            }
        }
    }

    if (citizenInput && passwordInput) {
        citizenInput.addEventListener('input', checkInputs);
        passwordInput.addEventListener('input', checkInputs);
        checkInputs();
    }

    function startTimer() {
        if (timerElement) {
            var timeLeft = 30;
            timerElement.innerHTML = "00:30";
            var timerInterval = setInterval(function () {
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    timerElement.innerHTML = "Expired";
                } else {
                    timerElement.innerHTML = "Time Left: " + "00:" + (timeLeft < 10 ? "0" : "") + timeLeft;
                    timeLeft--;
                }
            }, 1000);
        }
    }

    if (resendButton) {
        resendButton.addEventListener('click', function (event) {
            event.preventDefault();
            startTimer();
        });
    }

    if (timerElement) {
        startTimer();
    }
});