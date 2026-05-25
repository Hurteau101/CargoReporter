import {toastNotification, createDataTable, postForm} from "./helpers.js";

const freighterForm = document.getElementById('add-freighter-form')
const addFreighterBtn = document.getElementById('btn-add-freighter')
const addFreighterCard = document.getElementById('add-freighter-card')
const freightTbody = document.getElementById('freighter-tbody');

const cancelAddFreighterBtn = document.getElementById('btn-cancel-add');
cancelAddFreighterBtn.addEventListener('click', () => addFreighterCard.classList.remove('open'))

const cancelEditModalBtn = document.getElementById('btn-cancel-edit');
cancelEditModalBtn.addEventListener('click', () => document.getElementById('edit-modal').classList.remove('open'))


freighterForm.addEventListener('submit', async(e) => {
    await postForm(e, freighterForm, '/freighters/add-freighter/', 'POST', new FormData(freighterForm), 'Freighter added successfully')
})


document.querySelectorAll('.modal-close').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => document.getElementById('edit-modal').classList.remove('open'))
})


freightTbody.querySelectorAll('[data-del]').forEach(btn => {
    btn.addEventListener('click', async(e) => {
        const freighterId = btn.dataset.del;

        const response = await fetch(`/freighters/delete-freighter/${freighterId}`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": CSRF_TOKEN,
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            }
        })

        if (!response.ok) {
            const responseData = await response.json();
            toastNotification(responseData.message, false);
            return;
        }

        sessionStorage.setItem('toast', JSON.stringify({
            message: "Freighter Deleted Successfully",
            shouldOpenCard: false,
        }));

        window.location.reload();
    })
})


freightTbody.querySelectorAll('[data-edit]').forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('edit-modal').classList.add('open')
        const freighterId = btn.dataset.edit;
        const foundFreighter = FREIGHTER_LIST.find(freighter => freighter.id === Number(freighterId));

        const formatDateTime = (str) => str ? str.slice(0, 16).replace(' ', 'T') : '';


        if (!foundFreighter) return;

        document.getElementById('edit-aircraft-type').value = foundFreighter.aircraft_type;
        document.getElementById('edit-tail-number').value = foundFreighter.tail_number;
        document.getElementById('edit-flight-number').value = foundFreighter.flight_number;
        document.getElementById('edit-departure').value = foundFreighter.departure;
        document.getElementById('edit-destination').value = foundFreighter.destination;
        document.getElementById('edit-departure-time').value = formatDateTime(foundFreighter.departure_time);
        document.getElementById('edit-arrival-time').value = formatDateTime(foundFreighter.arrival_time);
        document.getElementById('edit-status').value = foundFreighter.status;
        document.getElementById('edit-station-notified').checked = foundFreighter.station_notified;
        document.getElementById('edit-station-informed-name').value = foundFreighter.station_informed_name;
        document.getElementById('edit-notes').value = foundFreighter.notes;

        const editFreighterForm = document.getElementById('edit-freighter-form')

        editFreighterForm.addEventListener('submit', async(e) => {
            await postForm(e, editFreighterForm, `/freighters/edit-freighter/${freighterId}`, 'POST',
                new FormData(editFreighterForm), 'Freighter Updated Successfully', false)
        })
    })
})


const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    const toastData = JSON.parse(savedToast);
    toastNotification(toastData.message, true);
    if (toastData.shouldOpenCard) {
        addFreighterCard.classList.add('open');
    }
    sessionStorage.removeItem('toast');
}

addFreighterBtn.addEventListener('click', () => {
    addFreighterCard.classList.toggle('open');
})

createDataTable('freighter-table', {
    columnDefs: [
        { orderable: false, targets: 11 },

    ],
})