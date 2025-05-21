// static/js/tooltipManager.js

export function initTooltips() {
    // Seleciona todos os botões de ajuda
    const helpButtons = document.querySelectorAll('.help-button');
    // Seleciona todos os tooltips
    const helpTooltips = document.querySelectorAll('.help-tooltip');

    console.log('Help buttons found:', helpButtons.length); // Log de depuração
    console.log('Help tooltips found:', helpTooltips.length); // Log de depuração

    // Adiciona event listeners para abrir/fechar tooltips
    helpButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // Impede que o clique se propague para o document
            const targetId = button.dataset.tooltipTarget;
            const targetTooltip = document.getElementById(targetId);

            console.log('Button clicked, targetId:', targetId); // Log de depuração

            if (targetTooltip) {
                console.log('Target tooltip found:', targetTooltip.id); // Log de depuração
                // Fecha qualquer outro tooltip aberto
                helpTooltips.forEach(tooltip => {
                    if (tooltip.id !== targetId && tooltip.classList.contains('active')) {
                        tooltip.classList.remove('active');
                        console.log('Closed tooltip:', tooltip.id); // Log de depuração
                    }
                });
                // Alterna a visibilidade do tooltip clicado
                targetTooltip.classList.toggle('active');
                console.log('Toggled active class on:', targetTooltip.id, 'New state:', targetTooltip.classList.contains('active')); // Log de depuração
            } else {
                console.warn('Target tooltip not found for ID:', targetId); // Log de depuração
            }
        });
    });

    // Adiciona event listeners para os botões de fechar dentro dos tooltips
    const closeButtons = document.querySelectorAll('.help-tooltip-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tooltip = button.closest('.help-tooltip');
            if (tooltip) {
                tooltip.classList.remove('active');
                console.log('Closed tooltip via close button:', tooltip.id); // Log de depuração
            }
        });
    });

    // Fecha tooltips quando o usuário clica fora deles
    document.addEventListener('click', (event) => {
        helpTooltips.forEach(tooltip => {
            // Verifica se o clique foi fora do tooltip E não em um botão de ajuda
            if (tooltip.classList.contains('active') && !tooltip.contains(event.target) && !event.target.closest('.help-button')) {
                tooltip.classList.remove('active');
                console.log('Closed tooltip via outside click:', tooltip.id); // Log de depuração
            }
        });
    });
}
