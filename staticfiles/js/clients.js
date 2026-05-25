import {createDataTable, postForm, toastNotification} from "./helpers.js";

const addClientBtn = document.getElementById('btn-add-client')
const addClientCard = document.getElementById('client-add-card')
const clientTbody = document.getElementById('client-tbody');

const cancelAddClientBtn = document.getElementById('btn-cancel-add');
cancelAddClientBtn.addEventListener('click', () => addClientCard.classList.remove('open'))

const cancelEditModalBtn = document.getElementById('btn-cancel-edit');
cancelEditModalBtn.addEventListener('click', () => document.getElementById('edit-modal').classList.remove('open'))

document.querySelectorAll('.modal-close').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => document.getElementById('edit-modal').classList.remove('open'))
})

addClientBtn.addEventListener('click', () => {
    addClientCard.classList.toggle('open');
})

const clientForm = document.getElementById('add-client-form')

clientForm.addEventListener('submit', async(e) => {
    await postForm(e, clientForm, '/clients/add-client/', 'POST', new FormData(clientForm), 'Client added successfully')
})

const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    const toastData = JSON.parse(savedToast);
    toastNotification(toastData.message, true);
    if (toastData.shouldOpenCard) {
        addClientCard.classList.add('open');
    }
    sessionStorage.removeItem('toast');
}

clientTbody.querySelectorAll('[data-del]').forEach(btn => {
    btn.addEventListener('click', async(e) => {
        const clientId = btn.dataset.del;

        const response = await fetch(`/clients/delete-client/${clientId}`, {
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
            message: "Client Deleted Successfully",
            shouldOpenCard: false,
        }));

        window.location.reload();
    })
})


clientTbody.querySelectorAll('[data-edit]').forEach(btn => {
    btn.addEventListener('click', () => {
        document.getElementById('edit-modal').classList.add('open')
        const clientId = btn.dataset.edit;

        const foundClient = CLIENT_LIST.find(client => client.id === Number(clientId));

        if (!foundClient) return;

        console.log(foundClient)

        document.getElementById('edit-company').value = foundClient.company_name;
        document.getElementById('edit-contact-name').value = foundClient.contact_name;
        document.getElementById('edit-email').value = foundClient.email;
        document.getElementById('edit-destination').value = foundClient.destination_iata;
        document.getElementById('edit-notes').value = foundClient.notes;

        const editClientForm = document.getElementById('edit-client-form')

        editClientForm.addEventListener('submit', async(e) => {
            await postForm(e, editClientForm, `/clients/edit-client/${clientId}`, 'POST',
                new FormData(editClientForm), 'Freighter Updated Successfully', false)
        })
    })
})

const table = createDataTable('client-table', {
    searching: true,
    columnDefs: [{ orderable: false, targets: 5 }],
})

document.getElementById('client-search').addEventListener('input', function() {
    table.search(this.value).draw();
});