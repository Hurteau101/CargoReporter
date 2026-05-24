document.querySelectorAll('.sla-dest-item').forEach(destination => {
    destination.addEventListener('click', () => {
        const dest = destination.dataset.dest;

        document.querySelectorAll('.sla-dest-item').forEach(x => x.classList.remove('active'));
        destination.classList.add('active');

        document.querySelectorAll('.sla-dest-table').forEach(table => table.style.display = 'none');
        document.getElementById('sla-table-wrapper').style.display = 'block';
        document.getElementById('sla-placeholder').style.display = 'none';

        const table = document.getElementById(`sla-table-${dest}`);
        if (table) table.style.display = 'table';

        const rowCount = table.rows.length - 1;
        document.getElementById('sla-dest-heading').innerHTML = `${dest} <span>${rowCount} shipment${rowCount !== 1 ? 's' : ''}</span>`;
    });
});