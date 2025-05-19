// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // Elementos do DOM
    const apiKeyInput = document.getElementById('geminiApiKey');
    const saveApiKeyCheckbox = document.getElementById('saveApiKey');
    const apiKeyStatus = document.getElementById('apiKeyStatus');
    
    const repoUrlInput = document.getElementById('repoUrl');
    const saveRepoUrlCheckbox = document.getElementById('saveRepoUrl');
    const linkedinUrlInput = document.getElementById('linkedinUrl');
    const saveLinkedinUrlCheckbox = document.getElementById('saveLinkedinUrl');

    const readmeLevelRadios = document.querySelectorAll('input[name="readmeLevel"]');

    const uploadForm = document.getElementById('uploadForm');
    const projectZipInput = document.getElementById('projectZip');
    const fileNameDisplay = document.getElementById('fileName');
    const generateButton = document.getElementById('generateButton');
    const buttonText = document.getElementById('buttonText');
    const buttonIconSvg = document.getElementById('buttonIcon');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const statusSection = document.getElementById('statusSection');
    const statusMessage = document.getElementById('statusMessage');
    const outputSection = document.getElementById('outputSection');
    const readmeContentElement = document.getElementById('readmeContent');
    const copyButton = document.getElementById('copyButton');
    const downloadButton = document.getElementById('downloadButton');
    const currentYear = document.getElementById('currentYear');
    const themeToggleButton = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');

    let originalButtonIconHTML = buttonIconSvg.innerHTML;
    let currentReadmeFilename = "README.md";
    let rawReadmeContent = "";

    // --- LÓGICA DO TEMA (como antes) ---
    const sunIcon = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>`;
    const moonIcon = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>`;

    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
            themeIcon.innerHTML = sunIcon;
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            themeIcon.innerHTML = moonIcon;
            localStorage.setItem('theme', 'light');
        }
    }
    themeToggleButton.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme') || 'light';
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (savedTheme) { applyTheme(savedTheme); } 
    else if (prefersDark) { applyTheme('dark'); } 
    else { applyTheme('light'); }
    // --- FIM DA LÓGICA DO TEMA ---

    if (currentYear) { currentYear.textContent = new Date().getFullYear(); }

    // Função auxiliar para carregar/salvar itens no localStorage
    function setupLocalStorageItem(inputId, checkboxId, storageKey, statusElementId = null, successMessage = '') {
        const inputElement = document.getElementById(inputId);
        const checkboxElement = document.getElementById(checkboxId);
        const statusElement = statusElementId ? document.getElementById(statusElementId) : null;

        const storedValue = localStorage.getItem(storageKey);
        if (storedValue) {
            inputElement.value = storedValue;
            checkboxElement.checked = true;
            if (statusElement && successMessage) {
                statusElement.textContent = successMessage;
                statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400';
            }
        } else {
             if (statusElement) {
                statusElement.textContent = `Nenhum ${storageKey.replace(/([A-Z])/g, ' $1').toLowerCase()} salvo.`;
                statusElement.className = 'text-xs mt-1 text-gray-500 dark:text-gray-400';
            }
        }

        checkboxElement.addEventListener('change', () => {
            const currentValue = inputElement.value.trim();
            if (checkboxElement.checked && currentValue) {
                localStorage.setItem(storageKey, currentValue);
                if (statusElement) {
                    statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1')} será salvo.`;
                     statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400';
                }
            } else if (!checkboxElement.checked) {
                localStorage.removeItem(storageKey);
                 if (statusElement) {
                    statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1')} não será salvo. Removido se estava salvo.`;
                    statusElement.className = 'text-xs mt-1 text-orange-600 dark:text-orange-400';
                }
            }
        });

        inputElement.addEventListener('input', () => {
            if (checkboxElement.checked) {
                const currentValue = inputElement.value.trim();
                if (currentValue) {
                    localStorage.setItem(storageKey, currentValue);
                    if (statusElement) {
                        statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1')} atualizado e salvo.`;
                        statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400';
                    }
                } else {
                    localStorage.removeItem(storageKey);
                     if (statusElement) {
                        statusElement.textContent = `Campo ${storageKey.replace(/([A-Z])/g, ' $1').toLowerCase()} vazio, removido do armazenamento.`;
                        statusElement.className = 'text-xs mt-1 text-orange-600 dark:text-orange-400';
                    }
                }
            }
        });
    }

    // Configurar localStorage para API Key, Repo URL e LinkedIn URL
    setupLocalStorageItem('geminiApiKey', 'saveApiKey', 'geminiApiKey', 'apiKeyStatus', 'API Key carregada do armazenamento local.');
    setupLocalStorageItem('repoUrl', 'saveRepoUrl', 'repoUrl');
    setupLocalStorageItem('linkedinUrl', 'saveLinkedinUrl', 'linkedinUrl');

    // Carregar nível de README salvo ou definir padrão
    const savedReadmeLevel = localStorage.getItem('readmeLevel');
    if (savedReadmeLevel) {
        const radioToCheck = document.querySelector(`input[name="readmeLevel"][value="${savedReadmeLevel}"]`);
        if (radioToCheck) radioToCheck.checked = true;
    } else {
        document.getElementById('levelModerate').checked = true; // Padrão para moderado
    }

    readmeLevelRadios.forEach(radio => {
        radio.addEventListener('change', (event) => {
            localStorage.setItem('readmeLevel', event.target.value);
        });
    });


    projectZipInput.addEventListener('change', () => {
        if (projectZipInput.files.length > 0) {
            fileNameDisplay.textContent = `Arquivo: ${projectZipInput.files[0].name}`;
        } else {
            fileNameDisplay.textContent = '';
        }
    });

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const apiKey = apiKeyInput.value.trim();
        if (!apiKey) {
            showStatus('Por favor, insira sua API Key do Gemini.', 'error');
            apiKeyInput.focus();
            return;
        }

        if (!projectZipInput.files || projectZipInput.files.length === 0) {
            showStatus('Por favor, selecione um arquivo .zip.', 'error');
            return;
        }

        const repoUrl = repoUrlInput.value.trim();
        const linkedinUrl = linkedinUrlInput.value.trim();
        const selectedReadmeLevel = document.querySelector('input[name="readmeLevel"]:checked').value;

        const formData = new FormData();
        formData.append('project_zip', projectZipInput.files[0]);
        // Adiciona os novos campos ao FormData para enviar ao backend
        formData.append('readme_level', selectedReadmeLevel);
        if (repoUrl) formData.append('repo_link', repoUrl);
        if (linkedinUrl) formData.append('linkedin_link', linkedinUrl);


        generateButton.disabled = true;
        buttonText.textContent = 'Gerando...';
        buttonIconSvg.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');
        outputSection.classList.add('hidden');
        showStatus('Enviando e processando... Por favor, aguarde.', 'info', false);

        try {
            const apiUrl = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
                ? 'http://127.0.0.1:8000/api/generate-readme' 
                : '/api/generate-readme';

            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData, // FormData agora inclui os novos campos
                headers: { 
                    'X-API-Key': apiKey 
                    // Não precisa de 'Content-Type': 'multipart/form-data', o fetch define automaticamente com FormData
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: `Erro HTTP: ${response.status} ${response.statusText}` }));
                let errorMessage = errorData.detail || `Erro ao gerar README: ${response.statusText}`;
                if (response.status === 401) errorMessage = "API Key inválida ou não autorizada.";
                throw new Error(errorMessage);
            }

            const result = await response.json();
            if (result.readme_content) {
                rawReadmeContent = result.readme_content;
                readmeContentElement.innerHTML = typeof marked !== 'undefined' ? marked.parse(rawReadmeContent) : rawReadmeContent;
                currentReadmeFilename = result.filename ? `${result.filename.replace(/\.zip$/i, '')}_README.md` : "README.md";
                outputSection.classList.remove('hidden');
                showStatus('README.md gerado com sucesso!', 'success');
                outputSection.scrollIntoView({ behavior: 'smooth' });
            } else {
                throw new Error('A API retornou uma resposta vazia.');
            }
        } catch (error) {
            console.error('Erro:', error);
            showStatus(`Falha ao gerar README: ${error.message}`, 'error');
            outputSection.classList.add('hidden');
        } finally {
            generateButton.disabled = false;
            buttonText.textContent = 'Gerar README.md';
            loadingSpinner.classList.add('hidden');
            buttonIconSvg.innerHTML = originalButtonIconHTML;
            buttonIconSvg.classList.remove('hidden');
        }
    });

    copyButton.addEventListener('click', () => {
        if (!rawReadmeContent) { showStatus('Nenhum conteúdo para copiar.', 'warning'); return; }
        navigator.clipboard.writeText(rawReadmeContent)
            .then(() => {
                const originalButtonContent = copyButton.innerHTML;
                copyButton.innerHTML = `<ion-icon name="checkmark-outline" class="mr-1"></ion-icon> Copiado!`;
                setTimeout(() => { copyButton.innerHTML = originalButtonContent; }, 2000);
            })
            .catch(err => { console.error('Erro ao copiar:', err); showStatus('Falha ao copiar.', 'error'); });
    });

    downloadButton.addEventListener('click', () => {
        if (!rawReadmeContent) { showStatus('Nenhum conteúdo para baixar.', 'warning'); return; }
        const blob = new Blob([rawReadmeContent], { type: 'text/markdown;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = currentReadmeFilename;
        document.body.appendChild(a); a.click();
        document.body.removeChild(a); URL.revokeObjectURL(url);
        showStatus(`Download de ${currentReadmeFilename} iniciado.`, 'success', true, 2000);
    });

    function showStatus(message, type = 'info', autoHide = true, duration = 4000) {
        statusSection.classList.remove('hidden');
        statusMessage.textContent = message;
        statusMessage.className = 'p-4 rounded-md text-sm border-l-4';
        statusMessage.classList.add(`status-${type}`);
        if (autoHide) { setTimeout(() => { statusSection.classList.add('hidden'); }, duration); }
    }
});
