// static/js/uiUtils.js

// Elementos de erro que podem ser acessados globalmente se necessário, ou passados como parâmetros
// Para simplicidade, vamos assumir que os seletores de ID são estáveis.
const apiKeyError = document.getElementById('apiKeyError');
const repoUrlError = document.getElementById('repoUrlError');
const linkedinUrlError = document.getElementById('linkedinUrlError');
const projectZipError = document.getElementById('projectZipError');
const geminiModelError = document.getElementById('geminiModelError');
const statusSection = document.getElementById('statusSection');
const statusMessage = document.getElementById('statusMessage');


export function displayValidationError(elementId, message) {
    const element = document.getElementById(elementId); // Busca o elemento pelo ID
    if (element) {
        element.textContent = message;
        element.classList.remove('hidden');
    }
}

export function clearValidationError(elementId) {
    const element = document.getElementById(elementId); // Busca o elemento pelo ID
    if (element) {
        element.textContent = '';
        element.classList.add('hidden');
    }
}

export function showStatus(message, type = 'info', autoHide = true, duration = 5000) {
    if (statusSection && statusMessage) {
        statusSection.classList.remove('hidden');
        statusMessage.textContent = message;
        statusMessage.className = 'p-4 rounded-md text-sm border-l-4 shadow'; // Reset classes
        statusMessage.classList.add(`status-${type}`);
        if (autoHide) {
            setTimeout(() => {
                statusSection.classList.add('hidden');
            }, duration);
        }
    }
}

export function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return '';
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
