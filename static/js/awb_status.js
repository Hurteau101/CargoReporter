import {createDataTable} from "./helpers.js";


createDataTable('awb-status-table', {
    columnDefs: [
        { orderable: false, targets: [7] }
    ]
})