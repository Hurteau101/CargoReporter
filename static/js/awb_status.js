import {createDataTable, toastNotification} from "./helpers.js";


const statusTbody = document.getElementById('awb-status-tbody');
const cancelUploadModalBtn = document.getElementById('img-cancel-btn');
cancelUploadModalBtn.addEventListener('click', () => document.getElementById('img-modal').classList.remove('open'))

document.querySelectorAll('.img-modal-close').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => document.getElementById('img-modal').classList.remove('open'))
})


// statusTbody.querySelectorAll('.btn-img').forEach(btn => {
//     btn.addEventListener('click', async(e) => {
//         const row = btn.closest('tr');
//         document.getElementById('img-modal-awb').textContent = row.dataset.rowId;
//         document.getElementById('img-modal').classList.add('open');
//     })
// })

statusTbody.querySelectorAll('.btn-img').forEach(btn => {
    btn.addEventListener('click', () => {
        const row = btn.closest('tr');
        document.getElementById('img-modal-awb').textContent = row.dataset.rowId;
        document.getElementById('img-modal').classList.add('open');

        if (btn.classList.contains('has-img')) {
            document.getElementById('img-preview-el').src = btn.dataset.imageUrl;
            document.getElementById('img-preview').style.display = 'block';
            document.getElementById('img-upload-zone').style.display = 'none';
            document.getElementById('img-save-btn').style.display = 'none';
            document.getElementById('img-remove-btn').style.display = 'inline-flex';
        } else {
            document.getElementById('img-preview').style.display = 'none';
            document.getElementById('img-upload-zone').style.display = 'block';
            document.getElementById('img-save-btn').style.display = 'inline-flex';
            document.getElementById('img-remove-btn').style.display = 'none';
        }
    })
})

document.getElementById('img-remove-btn').addEventListener('click', async() => {
    const awbNumber = document.getElementById('img-modal-awb').textContent;

    const response = await fetch(`/awb-status/delete-image/${awbNumber}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
            'X-Requested-With': 'XMLHttpRequest',
        }
    })

    if (!response.ok) return;

    sessionStorage.setItem('toast', 'Image removed successfully');
    window.location.reload();
})

document.getElementById('img-upload-zone').addEventListener('click', () => {
    document.getElementById('img-file-input').click();
})


const formData = new FormData();
const saveImage = document.getElementById('img-save-btn');

saveImage.addEventListener('click', async(e) => {
    e.preventDefault();

    if (!formData.get('img')) return;

    const awbNumber = document.getElementById('img-modal-awb').textContent;

    if (!awbNumber) return;

    const response = await fetch(`/awb-status/upload-image/${awbNumber}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
        body: formData
    })

    if (!response.ok) {
        const responseData = await response.json();

        responseData.errors.forEach(error => {
            toastNotification(error, false);
        });
        return;
    }

    sessionStorage.setItem("toast", "Image Stored Successfully");

    window.location.reload();
})

document.getElementById('img-file-input').addEventListener('change', (e) => {
    formData.set('img', e.target.files[0]);
    document.getElementById('image-text').textContent = e.target.files[0].name;
    document.getElementById('img-save-btn').disabled = false;
})


const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    toastNotification(savedToast, true);
    sessionStorage.removeItem('toast');
}


createDataTable('awb-status-table', {
    columnDefs: [
        { orderable: false, targets: [7] }
    ]
})

