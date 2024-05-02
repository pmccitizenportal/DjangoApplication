document.addEventListener('DOMContentLoaded', function () {
    const headers = document.querySelectorAll('.text-container');
    const contentSections = document.querySelectorAll('.content-section');

    function hideAllContent() {
        contentSections.forEach(section => {
            section.style.display = 'none';
        });
    }

    headers.forEach(header => {
        header.addEventListener('click', function () {
            headers.forEach(h => {
                h.classList.remove('active');
            });
            hideAllContent();

            this.classList.add('active');
            const targetId = this.getAttribute('data-target');
            const targetContent = document.getElementById(targetId);
            targetContent.style.display = 'flex';
        });
    });
});