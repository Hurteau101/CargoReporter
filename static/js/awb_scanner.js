import {createDataTable, toastNotification} from "./helpers.js";

const storedStations = GROUPED_STATIONS

const toast = sessionStorage.getItem('scanned-awb');
if (toast) {
    const { message, success } = JSON.parse(toast);
    sessionStorage.removeItem('scanned-awb');
    toastNotification(message, success);
}

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
const deletionBtn = document.getElementById('btn-deletion-manager');

updateDeletionBtn();

function addRow(awb, destination, count=1, fullOrder=false) {
    const tbody = document.getElementById('scan-table-body');

    const empty = tbody.querySelector('.dt-empty');
    if (empty) empty.closest('tr').remove();

    const tr = document.createElement('tr');
    tr.dataset.awb = awb;
    tr.dataset.dest = destination;

    const cells = [awb, destination];
    cells.forEach((value, index) => {
        const td = document.createElement('td');
        td.textContent = value;
        if (index === 0) td.style.cursor = 'pointer';
        tr.appendChild(td);
    });

    const countTd = document.createElement('td');
    const badge = document.createElement('span');
    badge.className = 'scan-count-badge';
    badge.textContent = count;
    countTd.appendChild(badge);
    tr.appendChild(countTd);

    const fullOrderCheckbox = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = fullOrder;
    checkbox.dataset.awb = awb;
    checkbox.classList.add('full-order-checkbox');
    fullOrderCheckbox.appendChild(checkbox);
    tr.appendChild(fullOrderCheckbox);

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
function updateClipboardHandle () {
    document.querySelectorAll('tr td:first-child').forEach(cell => {
        cell.addEventListener('click', () => {
            navigator.clipboard.writeText(cell.textContent.trim().slice(4))
                .then(() => {});
        })
    })
}


function getValidationError(awb, destination) {
    if (!destination) return 'Please select a destination';
    if (!awb) return 'Please input an AWB';
    if (!/^632-\d{8}$/.test(awb)) return 'Invalid AWB';
    return null;
}

function handleEmptyTable() {
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
}

function findAWb(awbValue, destinationValue) {
    const currentDestination = storedStations[destinationValue];
    return currentDestination.find(station => station.awb_number === awbValue);
}

function findAWBInOtherDest(awbValue, destinationValue) {
    return Object.entries(storedStations).find(([dest]) =>
        dest !== destinationValue && storedStations[dest].some(s => s.awb_number === awbValue)
    );
}


document.getElementById('scan-table-body').addEventListener('change', async (e) => {
    if (!e.target.classList.contains('full-order-checkbox')) return;
    const row = e.target.closest('tr');
    const awb = row.dataset.awb;
    const fullOrder = e.target.checked;
    const scanCount = row.querySelector('.scan-count-badge').textContent;

    const foundObj = findAWb(awb, destination.value);
    foundObj.full_order = fullOrder;

    updateScanCount(awb, scanCount, fullOrder, true);

});


destination.addEventListener('change', () => {
    const tbody = document.getElementById("scan-table-body");
    tbody.replaceChildren();

    const currentDestination = storedStations[destination.value];

    if (!currentDestination) {
        handleEmptyTable();
        return;
    }

    currentDestination.forEach(destination => {
        addRow(destination.awb_number, destination.destination, destination.scan_count, destination.full_order);
    })
})

async function updateScanCount(awb, count, full_order, isCheckboxChange = false) {
    const response = await fetch(`/awb-scanner/update-count/${awb}`, {
        "method": "PATCH",
        "headers": {
            "X-CSRFToken": CSRF_TOKEN,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        "body": JSON.stringify({
            "count": count,
            "full_order": full_order,
        })
    })

    if (!response.ok) {
        const responseData = await response.json();
        toastNotification(responseData.error, false);
        return;
    }

    toastNotification(isCheckboxChange ? `Updated Full Order AWB: ${awb}` : `Updated Count AWB: ${awb}`, true)
}


async function saveScanAWB(awb, destination, full_order) {
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
            "full_order": full_order,
        })
    })

    if (!response.ok) {
        const responseData = await response.json();
        toastNotification(responseData.error, false);
        return;
    }

    toastNotification(`Saved AWB: ${awb}`, true)

}

function updateDeletionBtn() {
    deletionBtn.disabled = Object.keys(storedStations).length === 0;
}

saveBtn.addEventListener('click', async () => {
    const awbValue = awb.value;
    const destinationValue = destination.value;

    const currentDestination = storedStations[destinationValue];

    const stationObj = {
        awb_number: awbValue,
        destination: destinationValue,
        scan_count: 1,
        full_order: false,
    }


    const error = getValidationError(awbValue, destinationValue);
    if (error) return toastNotification(error, false);

    const existingInOtherDest = findAWBInOtherDest(awbValue, destinationValue);

    if (existingInOtherDest) {
        const [dest] = existingInOtherDest;
        return toastNotification(`AWB already scanned under ${dest}`, false);
    }

    const existingRow = document.querySelector(`tr[data-awb="${awbValue}"]`);

    if (existingRow) {
        const foundObj = findAWb(awbValue, destinationValue);
        foundObj.scan_count += 1;

        const fullOrderCheckbox = existingRow.querySelector('.full-order-checkbox');
        const fullOrder = fullOrderCheckbox.checked;

        const badge = existingRow.querySelector('.scan-count-badge');
        const newCount = parseInt(badge.textContent) + 1;
        badge.textContent = String(newCount);
        awb.value = '';
        awb.focus();
        updateClipboardHandle();
        updateScanCount(awbValue, newCount, fullOrder);
        return;
    }

    if (!currentDestination) {
        storedStations[destinationValue] = [stationObj]
    } else {
        storedStations[destinationValue].push(stationObj);
    }


    addRow(awbValue, destinationValue, 1);
    updateClipboardHandle();
    awb.value = '';
    awb.focus();
    updateDeletionBtn();

    saveScanAWB(awbValue, destinationValue, false);
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


function openModal() {
    const list = document.getElementById('deletion-dest-list');
    list.innerHTML = '';

    Object.keys(storedStations).forEach(dest => {
        const label = document.createElement('label');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = dest;

        const name = document.createElement('span');
        name.textContent = dest;

        const count = document.createElement('span');
        count.className = 'modal-dest-count';
        const awbCount = storedStations[dest].length;
        count.textContent = `${awbCount} AWB${awbCount !== 1 ? 's' : ''}`;

        label.appendChild(checkbox);
        label.appendChild(name);
        label.appendChild(count);
        list.appendChild(label);
    });

    document.getElementById('deletion-modal').style.display = 'flex';
}

document.getElementById('btn-confirm-delete').addEventListener('click', async() => {
    const stations = [...document.querySelectorAll('#deletion-dest-list input[type="checkbox"]:checked')].map(cb => cb.value);
    if (stations.length === 0) return toastNotification('No destinations selected', false);

    const params = new URLSearchParams();
    stations.forEach(dest => params.append('destinations', dest));

    const response = await fetch(`/awb-scanner/mass-delete-awb-scanner?${params.toString()}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
    });

    if (!response.ok) {
        const responseData = await response.json();
        sessionStorage.setItem('scanned-awb', JSON.stringify({ message: responseData.error, success: false }));
        document.getElementById('deletion-modal').style.display = 'none';
        window.location.reload();
        return;
    }

    sessionStorage.setItem('scanned-awb', JSON.stringify({ message: `Mass Delete Completed for: ${stations.join(', ')}`, success: true }));
    document.getElementById('deletion-modal').style.display = 'none';
    window.location.reload();
});

deletionBtn.addEventListener('click', () => {
    openModal();
})

document.getElementById('btn-close-modal').addEventListener('click', () => {
    document.getElementById('deletion-modal').style.display = 'none';
});

document.getElementById('btn-cancel-modal').addEventListener('click', () => {
    document.getElementById('deletion-modal').style.display = 'none';
});


document.getElementById('scan-table-body').addEventListener('click', async(e) => {
    const btn = e.target.closest('[data-del]');
    const awb = btn?.dataset.del;
    if (!btn) return;
    const row = document.querySelector(`tr[data-awb="${btn.dataset.del}"]`);
    row?.remove();

    const currentDestination = storedStations[destination.value];
    if (!currentDestination) return;

    storedStations[destination.value] = storedStations[destination.value].filter(s => s.awb_number !== awb);
    if (storedStations[destination.value].length === 0) {
        delete storedStations[destination.value];
    }

    updateDeletionBtn();
    handleEmptyTable();

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
