function showLogin() {
    window.location.href = '/login/';
}

document.addEventListener('DOMContentLoaded', function () {
    const registerButton = document.getElementById('button');
    const form = document.getElementById('registrationForm');

    function checkForm() {
        let allFilled = true;
        const inputs = form.querySelectorAll('input[type="password"]');

        inputs.forEach(input => {
            if (input.value === '') {
                allFilled = false;
            }
        });

        registerButton.style.opacity = allFilled ? "1" : "0.5";
        registerButton.disabled = !allFilled;
    }

    form.addEventListener('keyup', checkForm);
});

document.addEventListener('DOMContentLoaded', function () {
    const userTypeRadio = document.querySelectorAll('input[name="user_type"]');
    const departmentField = document.getElementById('departmentField');
    userTypeRadio.forEach(radio => {
        radio.addEventListener('change', function () {
            departmentField.style.display = (this.value === 'officer') ? 'block' : 'none';
        });
    });
    switchGovIDType();
    document.getElementById('registrationForm').addEventListener('submit', function () {
        if (document.getElementById('aadhar_card_id_input').style.display === 'none') {
            document.getElementById('aadhar_card_id_input').value = '';
        }
        if (document.getElementById('pan_card_id_input').style.display === 'none') {
            document.getElementById('pan_card_id_input').value = '';
        }
        if (document.getElementById('ration_card_id_input').style.display === 'none') {
            document.getElementById('ration_card_id_input').value = '';
        }
    });
});

function switchGovIDType() {
    var selector = document.getElementById('government_id_input');
    var selectedValue = selector.value;

    var aadharInput = document.getElementById('aadhar_card_id_input');
    var panInput = document.getElementById('pan_card_id_input');
    var rationInput = document.getElementById('ration_card_id_input');

    aadharInput.style.display = 'none';
    panInput.style.display = 'none';
    rationInput.style.display = 'none';

    aadharInput.required = false;
    panInput.required = false;
    rationInput.required = false;

    if (selectedValue == 'aadhar') {
        aadharInput.style.display = 'block';
        aadharInput.required = true;
    } else if (selectedValue == 'pan') {
        panInput.style.display = 'block';
        panInput.required = true;
    } else if (selectedValue == 'ration') {
        rationInput.style.display = 'block';
        rationInput.required = true;
    }
}