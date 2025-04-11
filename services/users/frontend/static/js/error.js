document.addEventListener('DOMContentLoaded', function() {
    const showDetailsBtn = document.getElementById('showDetailsBtn');
    const errorDetails = document.getElementById('errorDetails');

    // Only add click handler if elements exist
    if (showDetailsBtn && errorDetails) {
        showDetailsBtn.addEventListener('click', function() {
            if (errorDetails.style.display === 'none') {
                errorDetails.style.display = 'block';
                this.textContent = 'Hide Details';

                // If you want to dynamically load error details from the backend:
                // fetch('/api/error-details')
                //     .then(response => response.json())
                //     .then(data => {
                //         document.getElementById('errorStack').textContent = data.stack;
                //     });
            } else {
                errorDetails.style.display = 'none';
                this.textContent = 'Show Details';
            }
        });
    }

    // Add any error-specific animations
    const errorIcon = document.querySelector('.error-icon');
    if (errorIcon) {
        setTimeout(() => {
            errorIcon.style.animation = 'pulse 1.5s infinite';
        }, 1000);
    }
});