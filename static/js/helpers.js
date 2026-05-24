export function toastNotification(title, success=true, duration=2500, gravity="bottom", position="right", style={
    background: success ? "#16a34a" : "#dc3545",
    borderRadius: "8px",
    fontSize: "14px",
    padding: "10px 20px"
}) {

    Toastify({
        text: title,
        duration: duration,
        gravity: gravity,
        position: position,
        style: style
    }).showToast();
}

export function updateStatValue(elementId, shouldIncrease=true) {
    const element = document.getElementById(elementId);
    if (element) {

        element.textContent = shouldIncrease ? Number(element.textContent) + 1 : Number(element.textContent) - 1;
        // element.textContent = `${Number(element.textContent) - shouldIncrease ? 1 : -1}`;
    }
}

export function createDataTable(tableId, options) {
    return $(`#${tableId}`).DataTable({
        paging: false,
        info: false,
        ordering: true,
        columnDefs: [
            { orderable: false, targets: 11 }
        ],
        layout: {
            topStart: null,
            topEnd: null,
            bottomStart: null,
            bottomEnd: null,
        },
        ...options
    });
}

export async function postForm(e, freighterForm, url, method, formData, successMessage, showFreighterCard = true) {
    e.preventDefault();

    const response = await fetch(url, {
        method: method,
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

    sessionStorage.setItem('toast', JSON.stringify({
        message: successMessage,
        shouldOpenCard: showFreighterCard,
    }));

    window.location.reload();
}
