import {createDataTable} from "./helpers.js";

// Create a DataTable for each SLA destination
document.querySelectorAll('.sla-dest-item').forEach(destination => {
    destination.addEventListener('click', () => {
        const dest = destination.dataset.dest;

        // Show the table for the selected destination
        document.querySelectorAll('.sla-dest-item').forEach(x => x.classList.remove('active'));
        destination.classList.add('active');

        document.querySelectorAll('.sla-dest-table').forEach(table => table.style.display = 'none');
        document.getElementById('sla-table-wrapper').style.display = 'block';
        document.getElementById('sla-placeholder').style.display = 'none';

        // Create a DataTable for the selected destination
        const table = document.getElementById(`sla-table-${dest}`);
        if (table) {
            table.style.display = 'table';
            createDataTable(table.id, {columnDefs: []});
        }

        // Update the heading with the number of shipments for the selected destination
        const rowCount = table.rows.length - 1;
        document.getElementById('sla-dest-heading').innerHTML = `${dest} <span>${rowCount} shipment${rowCount !== 1 ? 's' : ''}</span>`;
    });
});
