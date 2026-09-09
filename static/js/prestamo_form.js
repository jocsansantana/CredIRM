document.addEventListener('DOMContentLoaded', function () {
    const montoInput = document.getElementById('id_monto');
    const tasaInput = document.getElementById('id_tasa_interes');
    const previewInteres = document.getElementById('preview_interes');
    const previewTotal = document.getElementById('preview_total');

    if (!montoInput || !tasaInput || !previewInteres || !previewTotal) {
        return; // evita errores si el script se carga en otra página sin este form
    }

    function calcular() {
        const monto = parseFloat(montoInput.value) || 0;
        const tasa = parseFloat(tasaInput.value) || 0;

        const interes = monto * (tasa / 100);
        const total = monto + interes;

        previewInteres.value = '$' + interes.toFixed(2);
        previewTotal.value = '$' + total.toFixed(2);
    }

    montoInput.addEventListener('input', calcular);
    tasaInput.addEventListener('input', calcular);

    calcular(); // por si el form ya tiene valores (modo edición)
});