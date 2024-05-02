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

    const complaintTypeSelect = document.getElementById('id_complaint_type');
    const complaintSubTypeSelect = document.getElementById('id_complaint_sub_type');

    complaintTypeSelect.onchange = function () {
        const type_id = this.value;
        fetch(`/get-cms-subtypes/${type_id}`).then(response => response.json()).then(data => {
            complaintSubTypeSelect.innerHTML = '';
            if (data.subtypes.length === 0) {
                complaintSubTypeSelect.append(new Option('No sub-categories available', ''));
            } else {
                data.subtypes.forEach(subType => {
                    complaintSubTypeSelect.append(new Option(subType.complaint_sub_type, subType.complaint_sub_type_id));
                });
            }
        });
    };

    const wardSelect = document.getElementById('id_ward');
    const pethSelect = document.getElementById('id_peth');

    wardSelect.onchange = function () {
        const ward_id = this.value;
        fetch(`/get-peths-for-ward/${ward_id}`).then(response => response.json()).then(data => {
            pethSelect.innerHTML = '<option value="">Select a Peth after choosing a Ward</option>';
            if (data.peths.length === 0) {
                pethSelect.append(new Option('No peths available', ''));
            } else {
                data.peths.forEach(peth => {
                    pethSelect.append(new Option(peth.peth_name, peth.peth_id));
                });
            }
        });
    };

    var statusDropdown = document.getElementById('status-filter');

    var urlParams = new URLSearchParams(window.location.search);
    var status = urlParams.get('status');
    if (status && statusDropdown) {
        statusDropdown.value = status;
    }

    statusDropdown.addEventListener('change', function () {
        window.location.href = `?status=${this.value}`;
    });

    var statusDropdown2 = document.getElementById('status-filter-2');

    var urlParams = new URLSearchParams(window.location.search);
    var status = urlParams.get('status');
    if (status && statusDropdown) {
        statusDropdown2.value = status;
    }

    var urlParams = new URLSearchParams(window.location.search);
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

function handleStatusChange(status) {
    const url = new URL(window.location.href);
    url.searchParams.set('status', status);

    const activeTab = document.querySelector('.text-container.active').getAttribute('data-target');
    url.searchParams.set('active_tab', activeTab);

    window.location.href = url.toString();
}