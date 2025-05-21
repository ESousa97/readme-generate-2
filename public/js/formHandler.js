// static/js/formHandler.js
import { setupLocalStorageItem, loadRadioPreference, loadSelectedBadges, saveSelectedBadges as saveBadgesToStorage } from './localStorageManager.js';
import { validateApiKey, validateUrlField, validateSelectedModel } from './validationUtils.js';
import { displayValidationError, clearValidationError, showStatus, escapeHtml } from './uiUtils.js';
import { listModels, generateReadme } from './apiService.js';

// DOM Elements (precisam ser acessíveis)
let apiKeyInput, geminiModelSelect, repoUrlInput, projectUrlInput, linkedinUrlInput, projectZipInput, generateButton; // Added projectUrlInput
let fileNameDisplay, badgeSelectionContainer, outputSection, readmeContentElement;
let originalButtonIconHTMLStorage, buttonIconSvgElement, buttonTextElement, loadingSpinnerElement; // Para o botão de gerar

const API_KEY_ERROR_ID = 'apiKeyError';
const REPO_URL_ERROR_ID = 'repoUrlError';
const PROJECT_URL_ERROR_ID = 'projectUrlError'; // Added
const LINKEDIN_URL_ERROR_ID = 'linkedinUrlError';
const GEMINI_MODEL_ERROR_ID = 'geminiModelError';
const PROJECT_ZIP_ERROR_ID = 'projectZipError';

let currentReadmeFilename = "README.md"; //
let rawReadmeContent = ""; //

const availableBadges = [  //
    { value: "License", label: "Licença", defaultChecked: true },  //
    { value: "Issues", label: "Issues Abertas", defaultChecked: true },  //
    { value: "Pull Requests", label: "Pull Requests" },  //
    { value: "Last Commit", label: "Último Commit" },  //
    { value: "Top Language", label: "Linguagem Principal" },  //
    { value: "Code Size", label: "Tamanho do Código" },  //
    { value: "Contributors", label: "Contribuidores" }  //
];

function updateGenerateButtonState() { //
    const isApiKeyCurrentlyValid = validateApiKey(apiKeyInput.value, true); //
    const isRepoUrlCurrentlyValid = validateUrlField(repoUrlInput, REPO_URL_ERROR_ID, "GitHub", "github.com", true); //
    const isProjectUrlCurrentlyValid = validateUrlField(projectUrlInput, PROJECT_URL_ERROR_ID, "Projeto", null, true); // Added projectUrl validation (null for any domain)
    const isLinkedinUrlCurrentlyValid = validateUrlField(linkedinUrlInput, LINKEDIN_URL_ERROR_ID, "LinkedIn", "linkedin.com", true); //
    const isZipFileSelected = projectZipInput.files && projectZipInput.files.length > 0; //
    const isModelSelectedValid = validateSelectedModel(geminiModelSelect, GEMINI_MODEL_ERROR_ID, true); //

    if (isApiKeyCurrentlyValid && isRepoUrlCurrentlyValid && isProjectUrlCurrentlyValid && isLinkedinUrlCurrentlyValid && isZipFileSelected && isModelSelectedValid) { // Added isProjectUrlCurrentlyValid
        generateButton.disabled = false; //
    } else { //
        generateButton.disabled = true; //
    }
}

async function populateGeminiModels() { //
    const userApiKey = apiKeyInput.value;
    const defaultOptionInitial = geminiModelSelect.querySelector('option[value="DEFAULT_OPTION"]') || document.createElement('option');
    defaultOptionInitial.value = "DEFAULT_OPTION";

    if (!validateApiKey(userApiKey, true)) { // true para silencioso
        defaultOptionInitial.textContent = "API Key inválida para carregar modelos";
        geminiModelSelect.innerHTML = '';
        geminiModelSelect.appendChild(defaultOptionInitial);
        updateGenerateButtonState();
        return;
    }

    defaultOptionInitial.textContent = "Carregando modelos...";
    geminiModelSelect.innerHTML = '';
    geminiModelSelect.appendChild(defaultOptionInitial);

    try {
        const data = await listModels(userApiKey); // Usa apiService

        geminiModelSelect.innerHTML = '';
        const placeholderOption = document.createElement('option');
        placeholderOption.value = "DEFAULT_OPTION";
        placeholderOption.textContent = "Selecione um modelo";
        geminiModelSelect.appendChild(placeholderOption);

        const systemDefaultOption = document.createElement('option');
        systemDefaultOption.value = "";
        systemDefaultOption.textContent = "Usar modelo padrão do sistema";
        geminiModelSelect.appendChild(systemDefaultOption);

        if (data.models && data.models.length > 0) {
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                let displayName = model.name || model.id;
                const modelIdLowerCase = model.id.toLowerCase();

                if (modelIdLowerCase === 'gemini-2.5-pro-preview-03-25' || modelIdLowerCase === 'gemini-2.5-pro-preview-03-25') {
                    displayName = `${model.name || model.id} (Recomendado p/ Projetos de Grande Escala)`;
                } else if (modelIdLowerCase === 'gemini-2.0-flash' || modelIdLowerCase === 'gemini-2.0-flash') {
                    displayName = `${model.name || model.id} (Recomendado)`;
                }
                option.textContent = displayName;
                geminiModelSelect.appendChild(option);
            });
            // Aplica seleção salva APÓS popular
            const storedModel = localStorage.getItem('selectedGeminiModel');
            if (storedModel && geminiModelSelect.querySelector(`option[value="${storedModel}"]`)) {
                geminiModelSelect.value = storedModel;
            }
             // Configura o localStorage para o select de modelos AQUI
            setupLocalStorageItem('geminiModelSelect', 'saveGeminiModel', 'selectedGeminiModel');
        } else {
            placeholderOption.textContent = "Nenhum modelo compatível encontrado";
        }
    } catch (error) {
        console.error('Erro ao popular modelos Gemini:', error);
        const existingPlaceholder = geminiModelSelect.querySelector('option[value="DEFAULT_OPTION"]');
        if (existingPlaceholder) existingPlaceholder.textContent = "Erro ao carregar modelos";
    }
    validateSelectedModel(geminiModelSelect, GEMINI_MODEL_ERROR_ID);
    updateGenerateButtonState();
}

function populateBadges() { //
    if (!badgeSelectionContainer) return;

    const previouslySavedBadges = loadSelectedBadges() || availableBadges.filter(b => b.defaultChecked).map(b => b.value); //
    
    badgeSelectionContainer.innerHTML = '';
    availableBadges.forEach(badge => { //
        const input = document.createElement('input'); //
        input.type = 'checkbox'; //
        input.name = 'badge'; //
        input.value = badge.value; //
        input.id = `badge-${badge.value.toLowerCase().replace(/\s+/g, '-')}`; //
        input.className = 'checkbox-custom';
        if (previouslySavedBadges.includes(badge.value)) { //
            input.checked = true; //
        }
        
        const labelWrapper = document.createElement('label'); //
        labelWrapper.htmlFor = input.id; //
        labelWrapper.className = 'badge-checkbox-label';
        
        labelWrapper.appendChild(input); //
        labelWrapper.appendChild(document.createTextNode(badge.label)); //

        badgeSelectionContainer.appendChild(labelWrapper); //

        input.addEventListener('change', () => {
            const currentSelectedBadges = Array.from(document.querySelectorAll('#badgeSelectionContainer input[name="badge"]:checked'))
                                        .map(cb => cb.value);
            saveBadgesToStorage(currentSelectedBadges);
        });
    });
}

function setupEventListeners() {
    apiKeyInput.addEventListener('input', () => { //
        clearValidationError(API_KEY_ERROR_ID); //
        if (validateApiKey(apiKeyInput.value, true)) { //
            populateGeminiModels();
        } else {
            const defaultOption = geminiModelSelect.querySelector('option[value="DEFAULT_OPTION"]') || document.createElement('option');
            defaultOption.value = "DEFAULT_OPTION";
            defaultOption.textContent = "Insira uma API Key válida para carregar modelos";
            geminiModelSelect.innerHTML = '';
            geminiModelSelect.appendChild(defaultOption);
            updateGenerateButtonState();
        }
    });
    apiKeyInput.addEventListener('blur', () => { //
        validateApiKey(apiKeyInput.value); //
        updateGenerateButtonState(); //
    });

    repoUrlInput.addEventListener('input', () => { //
        clearValidationError(REPO_URL_ERROR_ID); //
        updateGenerateButtonState(); //
    });
    repoUrlInput.addEventListener('blur', () => { //
        validateUrlField(repoUrlInput, REPO_URL_ERROR_ID, "GitHub", "github.com"); //
        updateGenerateButtonState(); //
    });

    projectUrlInput.addEventListener('input', () => { // Added
        clearValidationError(PROJECT_URL_ERROR_ID); // Added
        updateGenerateButtonState(); // Added
    });
    projectUrlInput.addEventListener('blur', () => { // Added
        validateUrlField(projectUrlInput, PROJECT_URL_ERROR_ID, "Projeto", null); // Added (null for any domain)
        updateGenerateButtonState(); // Added
    });

    linkedinUrlInput.addEventListener('input', () => { //
        clearValidationError(LINKEDIN_URL_ERROR_ID); //
        updateGenerateButtonState(); //
    });
    linkedinUrlInput.addEventListener('blur', () => { //
        validateUrlField(linkedinUrlInput, LINKEDIN_URL_ERROR_ID, "LinkedIn", "linkedin.com"); //
        updateGenerateButtonState(); //
    });

    geminiModelSelect.addEventListener('change', () => { //
        validateSelectedModel(geminiModelSelect, GEMINI_MODEL_ERROR_ID); //
        updateGenerateButtonState(); //
    });
    
    projectZipInput.addEventListener('change', () => {  //
        clearValidationError(PROJECT_ZIP_ERROR_ID);  //
        if (projectZipInput.files.length > 0) { //
            fileNameDisplay.textContent = `Arquivo: ${projectZipInput.files[0].name}`; //
        } else { //
            fileNameDisplay.textContent = ''; //
        }
        updateGenerateButtonState(); //
    });

    const uploadFormElement = document.getElementById('uploadForm');
    uploadFormElement.addEventListener('submit', handleSubmit);

    const copyBtn = document.getElementById('copyButton');
    copyBtn.addEventListener('click', () => {  //
        if (!rawReadmeContent) { showStatus('Nenhum conteúdo para copiar.', 'warning'); return; }  //
        navigator.clipboard.writeText(rawReadmeContent)  //
            .then(() => {  //
                const originalButtonContent = copyBtn.innerHTML;  //
                copyBtn.innerHTML = `<ion-icon name="checkmark-done-outline" class="mr-1.5 text-lg"></ion-icon> Copiado!`;  //
                setTimeout(() => { copyBtn.innerHTML = originalButtonContent; }, 2000);  //
            })
            .catch(err => { console.error('Erro ao copiar:', err); showStatus('Falha ao copiar.', 'error'); });  //
    });

    const downloadBtn = document.getElementById('downloadButton');
    downloadBtn.addEventListener('click', () => {  //
        if (!rawReadmeContent) { showStatus('Nenhum conteúdo para baixar.', 'warning'); return; }  //
        const blob = new Blob([rawReadmeContent], { type: 'text/markdown;charset=utf-8' });  //
        const url = URL.createObjectURL(blob);  //
        const a = document.createElement('a');  //
        a.href = url; a.download = currentReadmeFilename;  //
        document.body.appendChild(a); a.click();  //
        document.body.removeChild(a); URL.revokeObjectURL(url);  //
        showStatus(`Download de ${currentReadmeFilename} iniciado.`, 'success', true, 2000);  //
    });
}

async function handleSubmit(event) { //
    event.preventDefault(); //
    
    const isApiKeyValidOnSubmit = validateApiKey(apiKeyInput.value); //
    const isRepoUrlValidOnSubmit = validateUrlField(repoUrlInput, REPO_URL_ERROR_ID, "GitHub", "github.com"); //
    const isProjectUrlValidOnSubmit = validateUrlField(projectUrlInput, PROJECT_URL_ERROR_ID, "Projeto", null); // Added
    const isLinkedinUrlValidOnSubmit = validateUrlField(linkedinUrlInput, LINKEDIN_URL_ERROR_ID, "LinkedIn", "linkedin.com"); //
    const isModelSelectedOnSubmit = validateSelectedModel(geminiModelSelect, GEMINI_MODEL_ERROR_ID); //
    let isZipSelectedOnSubmit = projectZipInput.files && projectZipInput.files.length > 0; //

    if (!isZipSelectedOnSubmit) { //
        displayValidationError(PROJECT_ZIP_ERROR_ID, "Por favor, selecione um arquivo .zip."); // Corrected to use constant
    } else { //
        clearValidationError(PROJECT_ZIP_ERROR_ID); // Corrected to use constant
    }
    
    updateGenerateButtonState(); //

    if (generateButton.disabled) { //
        showStatus('Por favor, corrija os erros no formulário antes de enviar.', 'warning'); //
        if (!document.getElementById(API_KEY_ERROR_ID).classList.contains('hidden')) apiKeyInput.focus(); //
        else if (!document.getElementById(GEMINI_MODEL_ERROR_ID).classList.contains('hidden')) geminiModelSelect.focus(); //
        else if (!document.getElementById(REPO_URL_ERROR_ID).classList.contains('hidden')) repoUrlInput.focus(); //
        else if (!document.getElementById(PROJECT_URL_ERROR_ID).classList.contains('hidden')) projectUrlInput.focus(); // Added
        else if (!document.getElementById(LINKEDIN_URL_ERROR_ID).classList.contains('hidden')) linkedinUrlInput.focus(); //
        else if (!document.getElementById(PROJECT_ZIP_ERROR_ID).classList.contains('hidden')) projectZipInput.focus(); //
        return; //
    }
    
    const trimmedApiKey = apiKeyInput.value.trim(); //
    const repoUrl = repoUrlInput.value.trim(); //
    const projectUrl = projectUrlInput.value.trim(); // Added
    const linkedinUrl = linkedinUrlInput.value.trim(); //
    const selectedReadmeLevel = document.querySelector('input[name="readmeLevel"]:checked').value; //
    const selectedGeminiModel = geminiModelSelect.value; //
    const selectedBadges = Array.from(document.querySelectorAll('#badgeSelectionContainer input[name="badge"]:checked')).map(cb => cb.value); //

    const formData = new FormData(); //
    formData.append('project_zip', projectZipInput.files[0]); //
    formData.append('readme_level', selectedReadmeLevel); //
    if (repoUrl) formData.append('repo_link', repoUrl); //
    if (projectUrl) formData.append('project_link', projectUrl); // Added
    if (linkedinUrl) formData.append('linkedin_link', linkedinUrl); //
    if (selectedBadges.length > 0) { formData.append('requested_badges', selectedBadges.join(',')); } //
    if (selectedGeminiModel && selectedGeminiModel !== "DEFAULT_OPTION") { formData.append('gemini_model_select', selectedGeminiModel); } //

    generateButton.disabled = true; buttonTextElement.textContent = 'Gerando...'; buttonIconSvgElement.classList.add('hidden'); loadingSpinnerElement.classList.remove('hidden'); outputSection.classList.add('hidden'); //
    showStatus('Enviando e processando... Por favor, aguarde. Isso pode levar alguns segundos.', 'info', false); //

    try { //
        const result = await generateReadme(formData, trimmedApiKey); // Usa apiService

        if (result.readme_content) { //
            rawReadmeContent = result.readme_content; //
            readmeContentElement.innerHTML = typeof marked !== 'undefined' ? marked.parse(rawReadmeContent) : escapeHtml(rawReadmeContent); //
            currentReadmeFilename = result.filename ? `${result.filename.replace(/\.zip$/i, '')}_README.md` : "README.md"; //
            outputSection.classList.remove('hidden'); //
            showStatus('README.md gerado com sucesso!', 'success'); //
            outputSection.scrollIntoView({ behavior: 'smooth' }); //
        } else { throw new Error('A API retornou uma resposta vazia ou inválida.'); } //
    } catch (error) { //
        console.error('Erro:', error); //
        showStatus(`Falha ao gerar README: ${error.message}`, 'error'); //
        outputSection.classList.add('hidden'); //
    } finally { //
        buttonTextElement.textContent = 'Gerar README.md'; //
        loadingSpinnerElement.classList.add('hidden'); //
        buttonIconSvgElement.innerHTML = originalButtonIconHTMLStorage; //
        buttonIconSvgElement.classList.remove('hidden'); //
        updateGenerateButtonState(); //
    }
}


export function initForm() {
    // Atribui os elementos do DOM que este módulo precisa
    apiKeyInput = document.getElementById('geminiApiKey');
    geminiModelSelect = document.getElementById('geminiModelSelect');
    repoUrlInput = document.getElementById('repoUrl');
    projectUrlInput = document.getElementById('projectUrl'); // Added
    linkedinUrlInput = document.getElementById('linkedinUrl');
    projectZipInput = document.getElementById('projectZip');
    generateButton = document.getElementById('generateButton');
    fileNameDisplay = document.getElementById('fileName');
    badgeSelectionContainer = document.getElementById('badgeSelectionContainer');
    outputSection = document.getElementById('outputSection');
    readmeContentElement = document.getElementById('readmeContent');
    
    buttonIconSvgElement = document.getElementById('buttonIcon');
    buttonTextElement = document.getElementById('buttonText');
    loadingSpinnerElement = document.getElementById('loadingSpinner');
    if(buttonIconSvgElement) originalButtonIconHTMLStorage = buttonIconSvgElement.innerHTML;


    // Configura localStorage para os campos principais
    setupLocalStorageItem('geminiApiKey', 'saveApiKey', 'geminiApiKey', 'apiKeyStatus', 'API Key carregada.');
    setupLocalStorageItem('repoUrl', 'saveRepoUrl', 'repoUrl');
    setupLocalStorageItem('projectUrl', 'saveProjectUrl', 'projectUrl'); // Added
    setupLocalStorageItem('linkedinUrl', 'saveLinkedinUrl', 'linkedinUrl');
    
    // Carrega preferências de rádio e badges
    loadRadioPreference('readmeLevel', 'readmeLevel', 'moderate');
    populateBadges();

    // Inicializa o select de modelos e o estado do botão
    if (apiKeyInput && apiKeyInput.value.trim()) {
        populateGeminiModels();
    } else {
        const defaultOpt = geminiModelSelect.querySelector('option[value="DEFAULT_OPTION"]') || document.createElement('option');
        defaultOpt.value = "DEFAULT_OPTION";
        defaultOpt.textContent = "Insira a API Key para carregar modelos";
        if(geminiModelSelect) {
            geminiModelSelect.innerHTML = '';
            geminiModelSelect.appendChild(defaultOpt);
        }
    }
    
    setupEventListeners();
    updateGenerateButtonState(); // Estado inicial do botão Gerar
}
