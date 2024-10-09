document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('response-form');
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const gameArea = document.getElementById('game-area');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const body = document.body;

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const response = document.getElementById('response-input').value;
            
            fetch('/submit_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `response=${encodeURIComponent(response)}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.game_ended) {
                    // Hide game area immediately
                    gameArea.classList.add('hidden');
                    
                    // Show loading animation
                    loadingDiv.classList.remove('hidden');
                    
                    // Start the loading animation
                    let dots = '';
                    const loadingText = loadingDiv.querySelector('p');
                    const interval = setInterval(() => {
                        dots = dots.length < 3 ? dots + '.' : '';
                        loadingText.textContent = `Game ending${dots}`;
                    }, 500);
                    
                    // Redirect after 2 seconds
                    setTimeout(() => {
                        clearInterval(interval);
                        window.location.href = '/';
                    }, 2000);
                } else {
                    document.getElementById('stimulus-word').textContent = data.next_stimulus;
                    document.getElementById('response-input').value = '';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    darkModeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
    });

    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        body.classList.add('dark-mode');
    }
});