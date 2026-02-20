// static/js/tooltipManager.js

export function initTooltips() {
    const helpButtons = document.querySelectorAll('.help-button');
    const helpTooltips = document.querySelectorAll('.help-tooltip');

    helpButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            const targetId = button.dataset.tooltipTarget;
            const targetTooltip = document.getElementById(targetId);

            if (targetTooltip) {
                helpTooltips.forEach(tooltip => {
                    if (tooltip.id !== targetId && tooltip.classList.contains('active')) {
                        tooltip.classList.remove('active');
                    }
                });
                targetTooltip.classList.toggle('active');
            }
        });
    });

    const closeButtons = document.querySelectorAll('.help-tooltip-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tooltip = button.closest('.help-tooltip');
            if (tooltip) {
                tooltip.classList.remove('active');
            }
        });
    });

    document.addEventListener('click', (event) => {
        helpTooltips.forEach(tooltip => {
            if (tooltip.classList.contains('active') && !tooltip.contains(event.target) && !event.target.closest('.help-button')) {
                tooltip.classList.remove('active');
            }
        });
    });
}
