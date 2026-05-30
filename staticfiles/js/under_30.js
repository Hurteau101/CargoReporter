import {toastNotification, updateStatValue, createDataTable} from "./helpers.js";

// Create data table (for sortability)
createDataTable('under-30-table', {
    columnDefs: [
        { orderable: false, targets: [7, 8] }
    ]
})

// function updateStats(hours) {
//     updateStatValue('total-stat', false)
//
//     const statId = hours < 6 ? 'critical-stat' : hours <= 15 ? 'warning-stat' : 'ok-stat';
//     updateStatValue(statId, false)
// }


const tbody = document.getElementById('under-30-table-body');

// Handle checkbox click
tbody.addEventListener('click', async(e) => {
    if (e.target.closest('input[type="checkbox"]')) {
        const row = e.target.closest('tr');

        const checkboxStatus = row.querySelector('input[type="checkbox"]').checked;

        // Highlight or remove highlight from row
        checkboxStatus ? row.classList.add('row-sent') : row.classList.remove('row-sent');

        const awbNumber = row.dataset.rowId;

        // Backend passes the list of AWBs. Find the AWB number.
        const foundAwbData = AWB_LIST.find(awb => awb.awb_number === awbNumber);

        // If AWB is found, update the status.
        if (foundAwbData) {
            const response = await fetch(`/under_30/update-sent-awb/${awbNumber}`, {
                "method": "PATCH",
                "headers": {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                "body": JSON.stringify({"status": checkboxStatus})
            })

            if (!response.ok) {
                const responseData = await response.json()
                toastNotification(responseData.message, false)
                return;
            }
        }
    }

    // Handle transfer button click
    if (e.target.closest('.btn-img')) {
        const row = e.target.closest('tr');
        const btn = e.target.closest('.btn-img');

        const awbNumber = row.dataset.rowId;
        const foundAwbData = AWB_LIST.find(awb => awb.awb_number === awbNumber);

        // If AWB is found, transfer it.
        if (foundAwbData) {
            const response = await fetch('/under_30/transfer-awb', {
                "method": "POST",
                "headers": {
                    "X-CSRFToken": CSRF_TOKEN,
                },
                "body": JSON.stringify(foundAwbData)
            })

            if (!response.ok) {
                const responseData = await response.json()
                toastNotification(responseData.message, false)
                return;
            }

            // Change text to be transferred
            btn.classList.add('transferred');
            btn.textContent = 'Transferred';
            // row.remove();
            // updateStats(foundAwbData.hours)
            toastNotification(`Transferred AWB: ${awbNumber}`, true)
        }
    }
});