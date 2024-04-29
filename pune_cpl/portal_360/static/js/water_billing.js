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

    document.getElementById('export-pdf').addEventListener('click', function () {
        const element = document.getElementById('billing-table');

        html2canvas(element).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jspdf.jsPDF({
                orientation: 'landscape',
                unit: 'px',
                format: [canvas.width, canvas.height]
            });
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save('bills-and-payments.pdf');
        });
    });

    document.getElementById('export-pdf-bill-details').addEventListener('click', function () {
        const element = document.getElementById('bill-details-table');

        html2canvas(element).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jspdf.jsPDF({
                orientation: 'landscape',
                unit: 'px',
                format: [canvas.width, canvas.height]
            });
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save('bill.pdf');
        });
    });
    const buttons = document.querySelectorAll('.bill-detail-button');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const billId = this.getAttribute('data-bill-id');
            fetchBillDetails(billId);
        });
    });

    const payments_buttons = document.querySelectorAll('.payment-detail-button');

    payments_buttons.forEach(button => {
        button.addEventListener('click', function () {
            const billId = this.getAttribute('data-payment-id');
            fetchTransactionDetails(billId);
        });
    });

    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('active_tab');

    if (activeTab) {
        document.querySelectorAll('.text-container').forEach(tab => {
            tab.classList.remove('active');
            document.getElementById(tab.getAttribute('data-target')).style.display = 'none';
        });

        document.getElementById(activeTab + '-header').classList.add('active');
        document.getElementById(activeTab).style.display = 'flex';
    }
});

function fetchBillDetails(billId) {
    fetch(`/get-bill-details/${billId}/`)  // Update with the correct URL pattern
        .then(response => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            showPopup(createBillDetailTable(data));
        })
        .catch(error => {
            console.error('Error fetching bill details:', error);
        });
}

function createBillDetailTable(bill) {
    const table = `<table id="bill-details-table" class='bill-details-table'>
        <tr><th>Bill ID</th><td>${bill.bill_id}</td></tr>
        <tr><th>Bill Date</th><td>${bill.bill_date}</td></tr>
        <tr><th>Due Date</th><td>${bill.due_date}</td></tr>
        <tr><th>Bill Amount</th><td>${bill.bill_amount}</td></tr>
        <tr><th>Penalty</th><td>${bill.penalty}</td></tr>
        <tr><th>Month</th><td>${bill.month}</td></tr>
        <tr><th>Year</th><td>${bill.year}</td></tr>
        <tr><th>From Date</th><td>${bill.from_date}</td></tr>
        <tr><th>To Date</th><td>${bill.to_date}</td></tr>
    </table>`;
    return table;
}

function showPopup(content) {
    document.getElementById('details-content').innerHTML = content;
    document.getElementById('popup-overlay').style.display = 'flex';
}

function closePopup() {
    document.getElementById('popup-overlay').style.display = 'none';
}

function fetchTransactionDetails(transactionId) {
    fetch((`/get-transaction-details/${transactionId}/`))
        .then(response => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            showPopup(createTransactionDetailTable(data));
        })
        .catch(error => {
            console.error('Error fetching transaction details:', error);
        });
}

function createTransactionDetailTable(data) {
    const table = `<table id="bill-details-table" class='bill-details-table'>
        <tr><th>Transaction ID</th><td>${data.transaction_id}</td></tr>
        <tr><th>Payment Date</th><td>${data.payment_date}</td></tr>
        <tr><th>Amount</th><td>${data.amount}</td></tr>
        <tr><th>Method</th><td>${data.payment_method}</td></tr>
        <tr><th>Status</th><td>${data.status}</td></tr>
        <tr><th>Remarks</th><td>${data.remarks}</td></tr>
    </table>
    `;
    return table;
}

function handleMeterChange(meterId) {
    const form = document.getElementById('meter-selection-form');
    const url = new URL(form.action);
    url.searchParams.set('meter_id', meterId);

    const activeTab = document.querySelector('.text-container.active').getAttribute('data-target');
    url.searchParams.set('active_tab', activeTab);

    window.location.href = url.toString();
}