// static/js/uiUtils.js

// Elementos de erro que podem ser acessados globalmente se necessário, ou passados como parâmetros
// Para simplicidade, vamos assumir que os seletores de ID são estáveis.
// const apiKeyError = document.getElementById('apiKeyError'); // Removidos pois não são usados diretamente neste arquivo
// const repoUrlError = document.getElementById('repoUrlError');
// const linkedinUrlError = document.getElementById('linkedinUrlError');
// const projectZipError = document.getElementById('projectZipError');
// const geminiModelError = document.getElementById('geminiModelError');

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

/**
 * Exibe uma mensagem de status para o usuário.
 * @param {string} message - A mensagem a ser exibida.
 * @param {string} type - O tipo de mensagem ('info', 'success', 'warning', 'error').
 * @param {boolean} autoHide - Se a mensagem deve desaparecer automaticamente.
 * @param {number} duration - Duração em milissegundos para autoHide.
 */
export function showStatus(message, type = 'info', autoHide = true, duration = 5000) {
    if (statusSection && statusMessage) {
        statusSection.classList.remove('hidden');
        statusMessage.textContent = message;
        // Define a classe base primeiro, depois a classe específica do tipo.
        // Isso garante que os estilos de .status-message-base sejam aplicados
        // e possam ser complementados/sobrescritos por .status-${type}.
        statusMessage.className = 'status-message-base'; // Alteração aqui para usar a classe base do style.css
        statusMessage.classList.add(`status-${type}`); // Adiciona a classe específica do tipo (ex: status-error)

        // Remove o timer anterior se houver um para evitar múltiplos desaparecimentos
        if (statusMessage.autoHideTimeout) {
            clearTimeout(statusMessage.autoHideTimeout);
        }

        if (autoHide) {
            statusMessage.autoHideTimeout = setTimeout(() => {
                statusSection.classList.add('hidden');
            }, duration);
        }
    } else {
        console.warn("Elementos de status (#statusSection ou #statusMessage) não encontrados no DOM.");
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
