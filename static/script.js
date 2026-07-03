// Toggle between login and signup forms
function toggleForm() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    loginForm.classList.toggle('active');
    signupForm.classList.toggle('active');
    
    // Clear messages
    document.getElementById('login-message').textContent = '';
    document.getElementById('signup-message').textContent = '';
    
    // Reset forms
    document.getElementById('login-form').reset();
    document.getElementById('signup-form').reset();
}

// Show message
function showMessage(formType, message, type) {
    const messageElement = document.getElementById(`${formType}-message`);
    messageElement.textContent = message;
    messageElement.className = `message ${type}`;
    
    if (type !== 'error') {
        setTimeout(() => {
            messageElement.textContent = '';
            messageElement.className = 'message';
        }, 4000);
    }
}

// Handle login form submission
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    const messageElement = document.getElementById('login-message');
    messageElement.textContent = 'Signing in';
    messageElement.className = 'message loading';
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('login', '✓ Login successful! Redirecting...', 'success');
            setTimeout(() => {
                // Redirect to chat page or dashboard
                window.location.href = '/dashboard';
            }, 2000);
        } else {
            showMessage('login', data.message || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('login', 'Connection error. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Handle signup form submission
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    
    // Validate password length
    if (password.length < 6) {
        showMessage('signup', 'Password must be at least 6 characters', 'error');
        return;
    }
    
    const messageElement = document.getElementById('signup-message');
    messageElement.textContent = 'Creating account';
    messageElement.className = 'message loading';
    
    try {
        const response = await fetch('/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('signup', '✓ Account created successfully! Redirecting to login...', 'success');
            setTimeout(() => {
                toggleForm();
                document.getElementById('signup-form').reset();
            }, 2000);
        } else {
            showMessage('signup', data.message || 'Signup failed', 'error');
        }
    } catch (error) {
        showMessage('signup', 'Connection error. Please try again.', 'error');
        console.error('Error:', error);
    }
});

// Password strength indicator
document.getElementById('signup-password').addEventListener('input', (e) => {
    const password = e.target.value;
    const strengthBars = document.querySelectorAll('.strength-bar');
    
    let strength = 0;
    
    // Check password length
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    
    // Check for uppercase letters
    if (/[A-Z]/.test(password)) strength++;
    
    // Check for numbers
    if (/[0-9]/.test(password)) strength++;
    
    // Check for special characters
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
    
    // Update visual indicators
    strengthBars.forEach((bar, index) => {
        if (index < strength) {
            if (strength <= 2) {
                bar.style.backgroundColor = '#ef4444';
            } else if (strength <= 3) {
                bar.style.backgroundColor = '#f59e0b';
            } else {
                bar.style.backgroundColor = '#10b981';
            }
        } else {
            bar.style.backgroundColor = '#e5e7eb';
        }
    });
});

// Real-time email validation
document.getElementById('signup-email').addEventListener('blur', (e) => {
    const email = e.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        e.target.setCustomValidity('Please enter a valid email address');
    } else {
        e.target.setCustomValidity('');
    }
});

// Prevent form submission on Enter for better UX
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        const form = e.target.closest('form');
        if (form) {
            const submitBtn = form.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.click();
            }
        }
    }
});

// Add focus effects to form groups
document.querySelectorAll('.input-field').forEach(input => {
    input.addEventListener('focus', () => {
        input.parentElement.style.transform = 'scale(1.01)';
    });
    
    input.addEventListener('blur', () => {
        input.parentElement.style.transform = 'scale(1)';
    });
});

// Initialize form on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat App - Authentication loaded');
});
