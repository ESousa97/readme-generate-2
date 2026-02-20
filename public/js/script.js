// static/js/script.js (Ponto de Entrada Principal)
import { initTheme } from './themeManager.js';
import { initForm } from './formHandler.js'; // Assumindo que formHandler.js existe
import { initTooltips } from './tooltipManager.js'; // Importa a função de inicialização dos tooltips

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initForm();
    initTooltips(); // Inicializa os tooltips

    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
});
