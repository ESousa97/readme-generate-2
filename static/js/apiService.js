// static/js/apiService.js
import { showStatus } from './uiUtils.js'; // Supondo que uiUtils exporte showStatus

const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:8000/api' 
    : '/api';

export async function listModels(apiKey) {
    if (!apiKey || !apiKey.trim()) {
        // console.warn("API Key é necessária para listar modelos.");
        throw new Error("API Key é necessária para listar modelos.");
    }
    const response = await fetch(`${API_BASE_URL}/list-models`, {
        headers: {
            'X-API-Key': apiKey.trim()
        }
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `Falha ao buscar modelos: ${response.statusText}` }));
        throw new Error(errorData.detail || `Falha ao buscar modelos: ${response.statusText}`);
    }
    return await response.json();
}

export async function generateReadme(formData, apiKey) {
    if (!apiKey || !apiKey.trim()) {
        throw new Error("API Key é obrigatória para gerar o README.");
    }
    const response = await fetch(`${API_BASE_URL}/generate-readme`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-API-Key': apiKey.trim()
        }
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `Erro HTTP: ${response.status} ${response.statusText}` })); //
        let errorMessage = errorData.detail || `Erro ao gerar README: ${response.statusText}`; //
        if (response.status === 401) errorMessage = "API Key inválida ou não autorizada."; //
        if (response.status === 400 && errorMessage.includes("PROMPT BLOQUEADO PELA IA")) { //
            errorMessage = "O prompt foi bloqueado pela IA devido a políticas de segurança. Tente ajustar o conteúdo do projeto ou as informações fornecidas."; //
        } else if (errorMessage.includes("PROMPT BLOQUEADO PELA IA")) { //
             errorMessage = "A IA bloqueou a solicitação devido a políticas de segurança. Detalhe: " + errorMessage; //
        }
        throw new Error(errorMessage); //
    }
    return await response.json();
}
