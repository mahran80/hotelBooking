document.addEventListener('DOMContentLoaded', function() {
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    const icon = darkModeToggle.querySelector('i');
    
    function setDarkMode(isDark) {
        if (isDark) {
            body.classList.add('dark-mode');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            document.cookie = 'darkMode=true; path=/';
        } else {
            body.classList.remove('dark-mode');
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            document.cookie = 'darkMode=false; path=/';
        }
    }
    
    // Check initial state
    const isDarkMode = document.cookie.includes('darkMode=true');
    setDarkMode(isDarkMode);
    
    // Toggle dark mode
    darkModeToggle.addEventListener('click', function() {
        const isDark = body.classList.contains('dark-mode');
        setDarkMode(!isDark);
    });
    
    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/logout/';
            
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            form.appendChild(csrfInput);
            document.body.appendChild(form);
            form.submit();
        });
    }
}); 