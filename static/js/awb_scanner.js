import {createDataTable, toastNotification} from "./helpers.js";

new TomSelect('#scan-dest', {
    maxOptions: null,
    maxItems: 1,
    create: false,
    onItemAdd: function() {
        this.blur();
        this.input.setAttribute('readonly', true);
    },
    onItemRemove: function() {
        this.input.removeAttribute('readonly');
    }
});

const awb = document.getElementById('scan-awb')
const destination = document.getElementById('scan-dest')
const saveBtn = document.getElementById('btn-scan-add')

function addRow(awb, destination, count, time) {
    const tbody = document.getElementById('scan-table-body');

    const empty = tbody.querySelector('.dt-empty');
    if (empty) empty.closest('tr').remove();

    const tr = document.createElement('tr');
    tr.dataset.awb = awb;
    tr.dataset.dest = destination;

    const cells = [awb, destination];
    cells.forEach(value => {
        const td = document.createElement('td');
        td.textContent = value;
        tr.appendChild(td);
    });

    const countTd = document.createElement('td');
    const badge = document.createElement('span');
    badge.className = 'scan-count-badge';
    badge.textContent = count;
    countTd.appendChild(badge);
    tr.appendChild(countTd);

    const timeTd = document.createElement('td');
    timeTd.textContent = time;
    tr.appendChild(timeTd);


    const actionTd = document.createElement('td');
    const btn = document.createElement('button');
    btn.className = 'btn-icon del';
    btn.title = 'Remove';
    btn.dataset.del = awb;
    btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>`;
    actionTd.appendChild(btn);
    tr.appendChild(actionTd);

    tbody.prepend(tr);
}

// Clipboard copy AWB number
document.querySelectorAll('tr td:first-child').forEach(cell => {
    cell.addEventListener('click', () => {
        navigator.clipboard.writeText(cell.textContent.trim().slice(4))
            .then(() => {});
    })
})

function getValidationError(awb, destination) {
    if (!destination) return 'Please select a destination';
    if (!awb) return 'Please input an AWB';
    if (!/^632-\d{8}$/.test(awb)) return 'Invalid AWB';
    return null;
}

async function updateScanCount(awb, count) {
    const response = await fetch(`/awb-scanner/update-count/${awb}`, {
        "method": "PATCH",
        "headers": {
            "X-CSRFToken": CSRF_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        "body": JSON.stringify({
            "count": count
        })
    })

    if (!response.ok) {
        const responseData = await response.json();
        toastNotification(responseData.error, false);
        return;
    }

    toastNotification(`Updated Count AWB: ${awb}`, true)
}

async function saveScanAWB(awb, destination, count) {
    const response = await fetch('/awb-scanner/save-awb-scanner', {
        "method": "POST",
        "headers": {
            "X-CSRFToken": CSRF_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        "body": JSON.stringify({
            "awb": awb,
            "destination": destination,
            "time": new Date().toISOString()
        })
    })

    if (!response.ok) {
        const responseData = await response.json();
        toastNotification(responseData.error, false);
        return;
    }

    toastNotification(`Saved AWB: ${awb}`, true)

}

saveBtn.addEventListener('click', async () => {
    const awbValue = awb.value;
    const destinationValue = destination.value;

    const error = getValidationError(awbValue, destinationValue);
    if (error) return toastNotification(error, false);

    const now = new Date().toLocaleString('en-US', {
        month: 'short', day: '2-digit', year: '2-digit',
        hour: '2-digit', minute: '2-digit', hour12: true
    });

    const existingRow = document.querySelector(`tr[data-awb="${awbValue}"]`);

    console.log('existingRow', existingRow);
    console.log('rowDest', existingRow?.dataset.dest);
    console.log('destinationValue', destinationValue);

    if (existingRow) {
        console.log('existingRow', existingRow);
        console.log('rowDest', existingRow?.dataset.dest);
        console.log('destinationValue', destinationValue);

        const rowDest = existingRow.dataset.dest;
        if (rowDest.trim() !== destinationValue.trim()) {
            return toastNotification('Wrong destination for this AWB', false);
        }

        const badge = existingRow.querySelector('.scan-count-badge');
        const newCount = parseInt(badge.textContent) + 1;
        badge.textContent = String(newCount);
        awb.value = '';
        awb.focus();
        updateScanCount(awbValue, newCount);
        return;
    }

    addRow(awbValue, destinationValue, 1, now);
    awb.value = '';
    awb.focus();

    saveScanAWB(awbValue, destinationValue, 1);
});

awb.addEventListener('input', () => {
    if (awb.value.length === 12) {
        const error = getValidationError(awb.value, destination.value);
        if (error) return toastNotification(error, false);
        saveBtn.click();
    }
})

destination.addEventListener('change', () => {
    if (awb.value.length === 12) {
        const error = getValidationError(awb.value, destination.value);
        if (error) return toastNotification(error, false);
        saveBtn.click();
    }
});

document.getElementById('scan-table-body').addEventListener('click', async(e) => {
    const btn = e.target.closest('[data-del]');
    const awb = btn?.dataset.del;
    if (!btn) return;
    const row = document.querySelector(`tr[data-awb="${btn.dataset.del}"]`);
    row?.remove();

    const tbody = document.getElementById('scan-table-body');
    if (tbody.querySelectorAll('tr').length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 5;
        td.className = 'dt-empty';
        td.textContent = 'No scanned AWBs found';
        tr.appendChild(td);
        tbody.appendChild(tr);
    }

    const response = await fetch(`/awb-scanner/remove-awb-scanner/${awb}`, {
        "method": "DELETE",
        "headers": {
            "X-CSRFToken": CSRF_TOKEN,
        }
    })

    if (!response.ok) {
        const responseData = await response.json();
        toastNotification(responseData.error, false);
        return;
    }

    toastNotification(`Deleted AWB: ${awb}`, true)
});
