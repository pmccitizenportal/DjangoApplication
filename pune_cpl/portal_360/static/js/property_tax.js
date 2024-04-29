window.addEventListener('DOMContentLoaded', (event) => {
    if (window.location.hash) {
        const id = window.location.hash.substring(1);
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView();
        }
    }
});

function handleMeterChange(meterId) {
    const form = document.getElementById('meter-selection-form');
    const url = new URL(form.action);
    url.searchParams.set('meter_id', meterId);

    const activeTab = document.querySelector('.text-container.active').getAttribute('data-target');
    url.searchParams.set('active_tab', activeTab);

    window.location.href = url.toString();
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('export-pdf').addEventListener('click', function () {
        const element = document.getElementById('property-table');

        html2canvas(element).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jspdf.jsPDF({
                orientation: 'landscape',
                unit: 'px',
                format: [canvas.width, canvas.height]
            });
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save('properties.pdf');
        });
    });

    document.getElementById('export-pdf-form-history').addEventListener('click', function () {
        const element = document.getElementById('form-histories-table');

        html2canvas(element).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jspdf.jsPDF({
                orientation: 'landscape',
                unit: 'px',
                format: [canvas.width, canvas.height]
            });
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save('form-histories.pdf');
        });
    });

    const buttons = document.querySelectorAll('.docs-button');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const element = document.getElementById('form-histories-table');

            html2canvas(element).then((canvas) => {
                const imgData = canvas.toDataURL('image/png');
                const pdf = new jspdf.jsPDF({
                    orientation: 'landscape',
                    unit: 'px',
                    format: [canvas.width, canvas.height]
                });
                pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
                pdf.save('form-histories.pdf');
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('property-selection-form').elements['property_id'].addEventListener('change', function () {
        this.form.submit();
    });
});