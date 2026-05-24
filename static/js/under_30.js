import {toastNotification} from "./helpers.js";




function updateStats(hours) {
    function updateValue(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = `${Number(element.textContent) - 1}`;
        }
    }

    updateValue('total-stat')

    const statId = hours < 6 ? 'critical-stat' : hours <= 15 ? 'warning-stat' : 'ok-stat';
    updateValue(statId)

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
            const response = await fetch(`/update-sent-awb/${awbNumber}`, {
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
            const response = await fetch('/transfer-awb', {
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