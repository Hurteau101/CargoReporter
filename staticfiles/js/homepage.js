import {toastNotification} from "./helpers.js";

document.getElementById("sla-file").addEventListener("change", function() {
    if (this.files.length > 0) {
        document.getElementById("file-label").innerHTML = this.files[0].name;
        const uploadBtn = document.getElementById("upload-btn");
        uploadBtn.disabled = false;
    }
});

const clearBtns = document.querySelectorAll(".btn-clear");

clearBtns.forEach(btn => {
    btn.addEventListener("click", async function(event) {
        const tabType = event.currentTarget.dataset.tab
        const tabName = event.currentTarget.dataset.tabName

        const response = await fetch(`/delete`, {
            "method": "DELETE",
            "headers": {
                "X-CSRFToken": CSRF_TOKEN,
            },
            "body": JSON.stringify({
                "tab_type": tabType
            })
        })

        if (!response.ok) {
            const responseData = await response.json()
            toastNotification(responseData.message, false)
            return;
        }

        toastNotification(tabType !== 'mass_clear' ? `Deleted all data from ${tabName}` : 'Mass cleared all data', true)


    })
});

