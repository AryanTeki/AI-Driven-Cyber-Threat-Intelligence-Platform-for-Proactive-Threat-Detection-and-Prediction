// Initialize theme based on stored preference or system default
function initializeTheme() {
    const storedTheme = localStorage.getItem('theme-preference');
    if (storedTheme) {
        setTheme(storedTheme);
    } else {
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
    }
}

// Set theme
function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme-preference', theme);
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (localStorage.getItem('theme-preference') === 'system') {
        setTheme(e.matches ? 'dark' : 'light');
    }
});

// Initialize theme when page loads
document.addEventListener('DOMContentLoaded', initializeTheme); 