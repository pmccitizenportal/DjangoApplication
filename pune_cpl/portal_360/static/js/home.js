document.querySelector('.settings-icon-dropdown').addEventListener('click', function () {
    var dropdown = document.querySelector('.settings-dropdown-content');
    if (dropdown.style.visibility === "visible") {
        dropdown.style.opacity = '0';
        dropdown.style.transform = 'translateY(-20px)';
        setTimeout(function () {
            dropdown.style.visibility = 'hidden';
        }, 500); // Match the timeout to the CSS transition duration
    } else {
        dropdown.style.visibility = 'visible';
        dropdown.style.opacity = '1';
        dropdown.style.transform = 'translateY(0)';
    }
});

document.addEventListener('click', function (event) {
    var dropdown = document.querySelector('.settings-dropdown-content');
    if (!document.querySelector('.settings-icon-dropdown').contains(event.target)) {
        dropdown.style.opacity = '0';
        dropdown.style.transform = 'translateY(-20px)';
        setTimeout(function () {
            dropdown.style.visibility = 'hidden';
        }, 500); // Ensure this matches the CSS transition time
    }
});

document.querySelector('.notification-icon-dropdown').addEventListener('click', function () {
    var dropdown = document.querySelector('.notification-dropdown-content');
    if (dropdown.style.visibility === "visible") {
        dropdown.style.opacity = '0';
        dropdown.style.transform = 'translateY(-20px)';
        setTimeout(function () {
            dropdown.style.visibility = 'hidden';
        }, 500); // Match the timeout to the CSS transition duration
    } else {
        dropdown.style.visibility = 'visible';
        dropdown.style.opacity = '1';
        dropdown.style.transform = 'translateY(0)';
    }
});

document.addEventListener('click', function (event) {
    var dropdown = document.querySelector('.notification-dropdown-content');
    if (!document.querySelector('.notification-settings-icon-dropdown').contains(event.target)) {
        dropdown.style.opacity = '0';
        dropdown.style.transform = 'translateY(-20px)';
        setTimeout(function () {
            dropdown.style.visibility = 'hidden';
        }, 500); // Ensure this matches the CSS transition time
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const content = document.getElementById('content');
    content.classList.add('fade-appear-active');
});

window.addEventListener('beforeunload', function (e) {
    const content = document.getElementById('content');
    content.classList.remove('fade-appear-active');
});

function confirmLogout() {
    if (confirm("Are you sure you want to log out?")) {
        window.location.href = this.href;
    }
    return false;
}

document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.top-bar-menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-target');
            const currentActive = document.querySelector('.top-bar-menu-item-div.active');
            const newActive = document.getElementById('menu-' + targetId.split('Content')[0]);

            if (currentActive) {
                currentActive.classList.remove('active');
            }
            if (newActive) {
                newActive.classList.add('active');
            }

            const contentContainers = document.querySelectorAll('.content-container');
            contentContainers.forEach(container => {
                if (container.id === targetId) {
                    container.style.display = 'block';
                    container.style.transform = 'translateX(0)';
                } else {
                    container.style.display = 'none';
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const updateUrl = document.body.getAttribute('data-update-url');
    const csrfToken = document.body.getAttribute('data-csrf-token');
    const appLinks = document.querySelectorAll('.ag-courses-item_link');

    appLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const applicationName = this.dataset.appName;
            const linkUrl = this.href;

            fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'application_name=' + encodeURIComponent(applicationName)
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Usage updated:', data);
                    window.location.href = linkUrl;
                })
                .catch(error => console.error('Error updating usage:', error));
        });
    });
});
