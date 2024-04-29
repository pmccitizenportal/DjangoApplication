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

    document.getElementById('status-filter').addEventListener('change', function () {
        window.location.href = `?status=${this.value}`;
    });
});