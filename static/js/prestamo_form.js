document.addEventListener('DOMContentLoaded', function () {
    const montoInput = document.getElementById('id_monto');
    const tasaInput = document.getElementById('id_tasa_interes');
    const fechaInicioInput = document.getElementById('id_fecha_inicio');
    const numeroCuotasInput = document.getElementById('id_numero_cuotas');
    const frecuenciaInput = document.getElementById('id_frecuencia_pago');

    const previewInteres = document.getElementById('preview_interes');
    const previewTotal = document.getElementById('preview_total');
    const previewFechaFin = document.getElementById('preview_fecha_fin');

    if (!montoInput || !tasaInput) {
        return; // evita errores si el script se carga en otra página sin este form
    }

    function calcularInteres() {
        const monto = parseFloat(montoInput.value) || 0;
        const tasa = parseFloat(tasaInput.value) || 0;

        const interes = monto * (tasa / 100);
        const total = monto + interes;

        previewInteres.value = '$' + interes.toFixed(2);
        previewTotal.value = '$' + total.toFixed(2);
    }

    function calcularFechaFin() {
        if (!fechaInicioInput.value || !numeroCuotasInput.value || !frecuenciaInput.value) {
            previewFechaFin.value = '--/--/----';
            return;
        }

        const fechaInicio = new Date(fechaInicioInput.value + 'T00:00:00');
        const numeroCuotas = parseInt(numeroCuotasInput.value) || 0;
        const frecuencia = frecuenciaInput.value;

        let fechaFin = new Date(fechaInicio);

        if (frecuencia === 'SEMANAL') {
            fechaFin.setDate(fechaFin.getDate() + (7 * numeroCuotas));
        } else if (frecuencia === 'QUINCENAL') {
            fechaFin.setDate(fechaFin.getDate() + (15 * numeroCuotas));
        } else if (frecuencia === 'MENSUAL') {
            fechaFin.setMonth(fechaFin.getMonth() + numeroCuotas);
        } else {
            previewFechaFin.value = '--/--/----';
            return;
        }

        const dia = String(fechaFin.getDate()).padStart(2, '0');
        const mes = String(fechaFin.getMonth() + 1).padStart(2, '0');
        const anio = fechaFin.getFullYear();

        previewFechaFin.value = `${dia}/${mes}/${anio}`;
    }

    montoInput.addEventListener('input', calcularInteres);
    tasaInput.addEventListener('input', calcularInteres);

    if (fechaInicioInput && numeroCuotasInput && frecuenciaInput) {
        fechaInicioInput.addEventListener('input', calcularFechaFin);
        numeroCuotasInput.addEventListener('input', calcularFechaFin);
        frecuenciaInput.addEventListener('change', calcularFechaFin);
    }

    calcularInteres();
    calcularFechaFin();
});