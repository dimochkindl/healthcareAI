// Simple confetti effect
function createConfetti() {
    const colors = ['#4361ee', '#4cc9f0', '#7209b7', '#f72585', '#4895ef'];
    const card = document.querySelector('.success-card');

    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = -10 + 'px';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        confetti.style.width = Math.random() * 8 + 4 + 'px';
        confetti.style.height = confetti.style.width;

        card.appendChild(confetti);

        const animationDuration = Math.random() * 3 + 2;

        confetti.animate([
            { top: '-10px', opacity: 0, transform: 'rotate(0deg)' },
            { opacity: 1 },
            { top: '100%', opacity: 0.5, transform: 'rotate(' + Math.random() * 360 + 'deg)' }
        ], {
            duration: animationDuration * 1000,
            easing: 'cubic-bezier(0.1, 0.8, 0.9, 1)',
            delay: Math.random() * 2000
        });

        setTimeout(() => confetti.remove(), animationDuration * 1000);
    }
}

// Trigger confetti after a slight delay
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(createConfetti, 800);
});