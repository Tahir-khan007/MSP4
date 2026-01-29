// Main JavaScript file for Finance Tracker

document.addEventListener('DOMContentLoaded', function() {
    // Hamburger Menu Toggle
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const links = navLinks.querySelectorAll('a');
        links.forEach(function(link) {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!hamburger.contains(event.target) && !navLinks.contains(event.target)) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    const alertsContainer = document.querySelector('.alerts-container');

    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.classList.add('fade-out');
            setTimeout(function() {
                alert.remove();

                // Remove container if no alerts left
                if (alertsContainer && alertsContainer.querySelectorAll('.alert').length === 0) {
                    alertsContainer.remove();
                }
            }, 300);
        }, 5000);
    });
});

// Function to close alert and remove container if empty
function closeAlert(button) {
    const alert = button.parentElement;
    const alertsContainer = alert.parentElement;

    alert.classList.add('fade-out');
    setTimeout(function() {
        alert.remove();

        // Remove container if no alerts left
        if (alertsContainer && alertsContainer.querySelectorAll('.alert').length === 0) {
            alertsContainer.remove();
        }
    }, 300);
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error-field');
        } else {
            input.classList.remove('error-field');
        }
    });

    return isValid;
}

// Add error field styling
const style = document.createElement('style');
style.textContent = `
    .error-field {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1) !important;
    }
`;
document.head.appendChild(style);
