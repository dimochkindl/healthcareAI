document.getElementById('userCreateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorElement = document.getElementById('error-message');
    errorElement.style.display = 'none';

    const form = e.target;
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new URLSearchParams(formData),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });

        const result = await response.json();

        if (!response.ok) {
            if (result.error) {
                errorElement.textContent = result.error;
                errorElement.style.display = 'block';
            }
            return;
        }

        window.location.href = result.redirect || '/users/success';

    } catch (error) {
        errorElement.textContent = 'Network error - please try again';
        errorElement.style.display = 'block';
        console.error('Submission error:', error);
    }
});