function login(event) {
    event.preventDefault(); // Prevent default form submission (GET request)

    const email = document.getElementById('id_email').value;
    const phone = document.getElementById('id_phone').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Basic email and phone validation
    if (!/@gmail\.com$/.test(email)) {
        document.getElementById('login-error-message').innerText = 'Invalid email format';
        return;
    }

    if (!/^\d{10}$/.test(phone)) {
        document.getElementById('login-error-message').innerText = 'Invalid phone number';
        return;
    }

    // Sending POST request to the backend for login
    fetch('http://127.0.0.1:8000/api/simplelogin/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ email: email, phone: phone })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            localStorage.setItem('token', data.data.token);
            alert('Login successful!');
            window.location.href = '/home/';
        } else {
            document.getElementById('login-error-message').innerText = 'Login failed: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('login-error-message').innerText = 'An error occurred during login. Please try again.';
    });
}
