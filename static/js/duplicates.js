import {toastNotification} from "./helpers.js";

const duplicateTbody = document.getElementById('duplicate-table-body');

// Delete Duplicate AWB
duplicateTbody.querySelectorAll('[data-del]').forEach(btn => {
    btn.addEventListener('click', async(e) => {
        const duplicateAWB = btn.dataset.del;

        const response = await fetch(`/duplication/delete-duplicate/${duplicateAWB}`, {
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

        sessionStorage.setItem("toast", "Duplicate AWB Deleted Successfully");

        window.location.reload();
    })
})

// Handle toast notification
const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    toastNotification(savedToast, true);
    sessionStorage.removeItem('toast');
}
