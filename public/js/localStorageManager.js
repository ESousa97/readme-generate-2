// static/js/localStorageManager.js

export function setupLocalStorageItem(inputId, checkboxId, storageKey, statusElementId = null, successMessage = '') { //
    const inputElement = document.getElementById(inputId); //
    const checkboxElement = document.getElementById(checkboxId); //
    const statusElement = statusElementId ? document.getElementById(statusElementId) : null; //

    if (!inputElement || !checkboxElement) {
        // console.warn(`Elemento não encontrado para setupLocalStorageItem: ${inputId} ou ${checkboxId}`);
        return;
    }
    
    const storedValue = localStorage.getItem(storageKey); //
    if (storedValue) { //
        inputElement.value = storedValue; //
        checkboxElement.checked = true; //
        if (statusElement && successMessage) { //
            statusElement.textContent = successMessage; //
            statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400'; //
        }
    } else { //
         if (statusElement) { //
            statusElement.textContent = `Nenhuma ${storageKey.replace(/([A-Z])/g, ' $1').toLowerCase().replace('gemini', 'Gemini')} salva.`; //
            statusElement.className = 'text-xs mt-1 text-gray-500 dark:text-gray-400'; //
        }
    }

    checkboxElement.addEventListener('change', () => { //
        const currentValue = inputElement.value.trim(); //
        if (checkboxElement.checked && currentValue) { //
            localStorage.setItem(storageKey, currentValue); //
            if (statusElement) { //
                statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1').replace('gemini', 'Gemini')} será salva.`; //
                 statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400'; //
            }
        } else if (!checkboxElement.checked) { //
            localStorage.removeItem(storageKey); //
             if (statusElement) { //
                statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1').replace('gemini', 'Gemini')} não será salva. Removida se estava salva.`; //
                statusElement.className = 'text-xs mt-1 text-orange-600 dark:text-orange-400'; //
            }
        } else if (checkboxElement.checked && !currentValue && statusElement) { //
            statusElement.textContent = `O campo ${storageKey.replace(/([A-Z])/g, ' $1').toLowerCase().replace('gemini', 'Gemini')} está vazio. Preencha para salvar.`; //
            statusElement.className = 'text-xs mt-1 text-orange-600 dark:text-orange-400'; //
            checkboxElement.checked = false; //
        }
    });

    inputElement.addEventListener('input', () => { //
        if (checkboxElement.checked) { //
            const currentValue = inputElement.value.trim(); //
            if (currentValue) { //
                localStorage.setItem(storageKey, currentValue); //
                if (statusElement) { //
                    statusElement.textContent = `${storageKey.replace(/([A-Z])/g, ' $1').replace('gemini', 'Gemini')} atualizada e salva.`; //
                    statusElement.className = 'text-xs mt-1 text-green-600 dark:text-green-400'; //
                }
            } else { //
                localStorage.removeItem(storageKey); //
                 if (statusElement) { //
                    statusElement.textContent = `Campo ${storageKey.replace(/([A-Z])/g, ' $1').toLowerCase().replace('gemini', 'Gemini')} vazio, removido do armazenamento.`; //
                    statusElement.className = 'text-xs mt-1 text-orange-600 dark:text-orange-400'; //
                }
            }
        }
    });
    if (inputElement.tagName === 'SELECT') { //
        inputElement.addEventListener('change', () => { //
             if (checkboxElement.checked) { //
                localStorage.setItem(storageKey, inputElement.value); //
             }
        });
    }
}

export function loadRadioPreference(radioGroupName, storageKey, defaultValue) {
    const savedValue = localStorage.getItem(storageKey);
    const valueToSelect = savedValue || defaultValue;
    const radioToCheck = document.querySelector(`input[name="${radioGroupName}"][value="${valueToSelect}"]`);
    if (radioToCheck) {
        radioToCheck.checked = true;
    } else if (defaultValue) { // Se o valor salvo não existir mais, mas houver um default
        const defaultRadio = document.querySelector(`input[name="${radioGroupName}"][value="${defaultValue}"]`);
        if (defaultRadio) defaultRadio.checked = true;
    }

    document.querySelectorAll(`input[name="${radioGroupName}"]`).forEach(radio => {
        radio.addEventListener('change', (event) => {
            localStorage.setItem(storageKey, event.target.value);
        });
    });
}

export function loadSelectedBadges() {
    const savedBadges = localStorage.getItem('selectedBadges');
    return savedBadges ? JSON.parse(savedBadges) : null;
}

export function saveSelectedBadges(selectedBadgesArray) {
    localStorage.setItem('selectedBadges', JSON.stringify(selectedBadgesArray));
}
