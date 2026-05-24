import {toastNotification, updateStatValue, createDataTable} from "./helpers.js";

createDataTable('under-30-table', {
    columnDefs: [
        { orderable: false, targets: [7, 8] }
    ]
})

function updateStats(hours) {
    updateStatValue('total-stat', false)

    const statId = hours < 6 ? 'critical-stat' : hours <= 15 ? 'warning-stat' : 'ok-stat';
    updateStatValue(statId, false)
}


const tbody = document.getElementById('under-30-table-body');

tbody.addEventListener('click', async(e) => {
    if (e.target.closest('input[type="checkbox"]')) {
        const row = e.target.closest('tr');
        row.classList.add('row-sent');

        const checkboxStatus = row.querySelector('input[type="checkbox"]').checked;

        const awbNumber = row.dataset.rowId;
        const foundAwbData = AWB_LIST.find(awb => awb.awb_number === awbNumber);

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


    if (e.target.closest('.btn-img')) {
        const row = e.target.closest('tr');

        const awbNumber = row.dataset.rowId;
        const foundAwbData = AWB_LIST.find(awb => awb.awb_number === awbNumber);
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

            row.remove();
            updateStats(foundAwbData.hours)
            toastNotification(`Transferred AWB: ${awbNumber}`, true)
        }
    }
});