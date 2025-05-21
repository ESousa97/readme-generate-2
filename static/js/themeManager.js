// static/js/themeManager.js

const themeToggleButton = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

const sunIcon = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>`; //
const moonIcon = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>`; //

function applyTheme(theme) { //
    if (theme === 'dark') { //
        document.documentElement.classList.add('dark'); //
        if (themeIcon) themeIcon.innerHTML = sunIcon; //
        localStorage.setItem('theme', 'dark'); //
    } else { //
        document.documentElement.classList.remove('dark'); //
        if (themeIcon) themeIcon.innerHTML = moonIcon; //
        localStorage.setItem('theme', 'light'); //
    }
}

export function initTheme() {
    if (!themeToggleButton || !themeIcon) {
        console.warn("Elementos do tema (botão ou ícone) não encontrados.");
        return;
    }
    themeToggleButton.addEventListener('click', () => { //
        const currentTheme = localStorage.getItem('theme') || 'light'; //
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark'); //
    });

    const savedTheme = localStorage.getItem('theme'); //
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches; //
    
    if (savedTheme) { 
        applyTheme(savedTheme); //
    } else if (prefersDark) { 
        applyTheme('dark'); //
    } else { 
        applyTheme('light'); //
    }
}
