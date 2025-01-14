window.dashExtensions = Object.assign({}, window.dashExtensions, {
    theme_handler: {
        function(theme) {
            if (!theme) return;
            
            if (theme === 'system') {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    theme = 'dark';
                } else {
                    theme = 'light';
                }
            }
            
            document.documentElement.setAttribute('data-bs-theme', theme);
            return theme;
        }
    }
}); 