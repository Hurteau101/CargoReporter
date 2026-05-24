import {toastNotification, createDataTable} from "./helpers.js";

const freighterForm = document.getElementById('add-freighter-form')
const addFreighterBtn = document.getElementById('btn-add-freighter')
const addFreighterCard = document.getElementById('add-freighter-card')

const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    toastNotification(savedToast, true);
    sessionStorage.removeItem('toast');
    addFreighterCard.classList.toggle('open');
}

addFreighterBtn.addEventListener('click', () => {
    addFreighterCard.classList.toggle('open');
})

createDataTable('freighter-table', {
    columnDefs: [
        { orderable: false, targets: 11 }
    ],
})


freighterForm.addEventListener('submit', async(e) => {
    e.preventDefault();

    const formData = new FormData(freighterForm);
    const response = await fetch('/freighters/add-freighter/', {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData
    })

    const responseData = await response.json();

    if (!response.ok) {
        responseData.errors.forEach(error => {
            toastNotification(error, false);
        });
        return;
    }

    sessionStorage.setItem('toast', 'Freighter added successfully');
    window.location.reload();
})