import {toastNotification} from "./helpers.js";

document.getElementById("sla-file").addEventListener("change", function() {
    if (this.files.length > 0) {
        document.getElementById("file-label").innerHTML = this.files[0].name;
        const uploadBtn = document.getElementById("upload-btn");
        uploadBtn.disabled = false;
    }
});

const clearBtns = document.querySelectorAll(".btn-clear");
const massClearBtn = document.querySelector('[data-tab="mass_clear"]');

clearBtns.forEach(btn => {
    btn.addEventListener("click", async function(event) {
        const tabType = event.currentTarget.dataset.tab
        const tabName = event.currentTarget.dataset.tabName

        btn.classList.add('btn-disabled')
        btn.disabled = true;

        if (tabType !== 'mass_clear') {
            const otherBtns = [...clearBtns].filter(b => b.dataset.tab !== 'mass_clear');
            if (otherBtns.every(b => b.disabled)) {
                massClearBtn.disabled = true;
                massClearBtn.classList.add('btn-disabled');
            }
        }

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

