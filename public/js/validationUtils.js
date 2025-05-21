// static/js/validationUtils.js
import { displayValidationError, clearValidationError } from './uiUtils.js';

// IDs dos elementos de erro
const API_KEY_ERROR_ID = 'apiKeyError';
// const REPO_URL_ERROR_ID = 'repoUrlError'; (Será passado como parâmetro para a função genérica)
// const PROJECT_URL_ERROR_ID = 'projectUrlError'; (Será passado como parâmetro)
// const LINKEDIN_URL_ERROR_ID = 'linkedinUrlError';
// const GEMINI_MODEL_ERROR_ID = 'geminiModelError';


export function validateApiKey(key, silent = false) {
    const trimmedKey = key.trim();
    if (!trimmedKey) {
        if (!silent) displayValidationError(API_KEY_ERROR_ID, "API Key é obrigatória.");
        return false;
    }
    if (/\s/.test(key)) {
        if (!silent) displayValidationError(API_KEY_ERROR_ID, "API Key não pode conter espaços.");
        return false;
    }
    if (trimmedKey.length !== 39) {
        if (!silent) displayValidationError(API_KEY_ERROR_ID, "API Key parece ter um formato inválido (comprimento esperado: 39 caracteres).");
        return false;
    }
    if (!silent) clearValidationError(API_KEY_ERROR_ID);
    return true;
}

export function validateUrlField(inputElement, errorElementId, fieldName, allowedDomain = null, silent = false) {
    const url = inputElement.value.trim();
    if (!url) {
        // Se o campo não for obrigatório e estiver vazio, é válido.
        // A lógica de obrigatoriedade deve ser tratada fora, se necessário.
        if (!silent) clearValidationError(errorElementId);
        return true;
    }
    try {
        const urlObj = new URL(url);
        if (!['http:', 'https:'].includes(urlObj.protocol)) {
            if (!silent) displayValidationError(errorElementId, `Link do ${fieldName} deve começar com http:// ou https://.`);
            return false;
        }
        if (allowedDomain) {
            const hostname = urlObj.hostname.toLowerCase(); // Normalize to lowercase for comparison
            const normalizedAllowedDomain = allowedDomain.toLowerCase();

            // Check if the hostname is exactly the allowed domain or a www subdomain of it.
            if (hostname === normalizedAllowedDomain || hostname === `www.${normalizedAllowedDomain}`) {
                // Valid
            } else if (normalizedAllowedDomain === 'linkedin.com' && hostname.endsWith('.linkedin.com')) {
                // Also allow subdomains like 'br.linkedin.com' for LinkedIn
            }
            else {
                 if (!silent) displayValidationError(errorElementId, `Link do ${fieldName} deve ser um domínio ${allowedDomain}.`);
                 return false;
            }
        }
    } catch (_) {
        if (!silent) displayValidationError(errorElementId, `Link do ${fieldName} inválido.`);
        return false;
    }
    if (!silent) clearValidationError(errorElementId);
    return true;
}

export function validateSelectedModel(geminiModelSelectElement, errorElementId, silent = false) {
    if (geminiModelSelectElement.value === "DEFAULT_OPTION") {
        if (!silent) displayValidationError(errorElementId, "Por favor, selecione um modelo Gemini.");
        return false;
    }
    if (!silent) clearValidationError(errorElementId);
    return true;
}
