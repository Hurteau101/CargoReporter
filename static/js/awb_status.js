import {createDataTable, toastNotification} from "./helpers.js";


const statusTbody = document.getElementById('awb-status-tbody');
const cancelUploadModalBtn = document.getElementById('img-cancel-btn');
cancelUploadModalBtn.addEventListener('click', () => document.getElementById('img-modal').classList.remove('open'))

// Close modal
document.querySelectorAll('.img-modal-close').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => document.getElementById('img-modal').classList.remove('open'))
})

// Open the edit or view modal
statusTbody.querySelectorAll('.btn-img').forEach(btn => {
    btn.addEventListener('click', () => {
        const row = btn.closest('tr');
        document.getElementById('img-modal-awb').textContent = row.dataset.rowId;
        document.getElementById('img-modal').classList.add('open');

        // Check if the image is already uploaded. To show view.
        if (btn.classList.contains('has-img')) {
            document.getElementById('img-preview-el').src = btn.dataset.imageUrl;
            document.getElementById('img-preview').style.display = 'block';
            document.getElementById('img-upload-zone').style.display = 'none';
            document.getElementById('img-save-btn').style.display = 'none';
            document.getElementById('img-remove-btn').style.display = 'inline-flex';
        }
        // If not, show the upload.
        else {
            document.getElementById('img-preview').style.display = 'none';
            document.getElementById('img-upload-zone').style.display = 'block';
            document.getElementById('img-save-btn').style.display = 'inline-flex';
            document.getElementById('img-remove-btn').style.display = 'none';
        }
    })
})

// Remove the image.
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

// Open file explorer
document.getElementById('img-upload-zone').addEventListener('click', () => {
    document.getElementById('img-file-input').click();
})


const formData = new FormData();
const saveImage = document.getElementById('img-save-btn');

// Save the image
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

// Set the name of image to image zone and disable button.
document.getElementById('img-file-input').addEventListener('change', (e) => {
    formData.set('img', e.target.files[0]);
    document.getElementById('image-text').textContent = e.target.files[0].name;
    document.getElementById('img-save-btn').disabled = false;
})


// Handle toast notification
const savedToast = sessionStorage.getItem('toast');
if (savedToast) {
    toastNotification(savedToast, true);
    sessionStorage.removeItem('toast');
}

// Create data table (for sortability)
createDataTable('awb-status-table', {
    columnDefs: [
        { orderable: false, targets: [7] }
    ]
})

