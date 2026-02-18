// ===================================
// Mobile Navigation Toggle
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Toggle mobile menu
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Close menu when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = event.target.closest('.navbar');
        if (!isClickInsideNav && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    });
});

// ===================================
// Contact Form Handling
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form values
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();

            // Validation
            if (!name || !email || !subject || !message) {
                showNotification('Παρακαλώ συμπληρώστε όλα τα υποχρεωτικά πεδία.', 'error');
                return;
            }

            // Email validation
            if (!isValidEmail(email)) {
                showNotification('Παρακαλώ εισάγετε ένα έγκυρο email.', 'error');
                return;
            }

            // Prepare form data
            const formData = {
                name: name,
                email: email,
                phone: phone,
                subject: subject,
                message: message,
                timestamp: new Date().toLocaleString('el-GR')
            };

            // Log to console (simulating form submission)
            console.log('Form submitted with data:', formData);

            // Store in localStorage for demonstration
            storeFormSubmission(formData);

            // Show success message
            showNotification('Το μήνυμά σας έχει λαμβάνεται! Θα επικοινωνήσουμε σύντομα.', 'success');

            // Reset form
            contactForm.reset();

            // Scroll to top after submission
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});

// ===================================
// Email Validation
// ===================================
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ===================================
// Store Form Submission
// ===================================
function storeFormSubmission(data) {
    let submissions = JSON.parse(localStorage.getItem('formSubmissions')) || [];
    submissions.push(data);
    localStorage.setItem('formSubmissions', JSON.stringify(submissions));
}

// ===================================
// Notification System
// ===================================
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.setAttribute('role', 'alert');
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close" aria-label="Κλείσιμο">&times;</button>
        </div>
    `;

    // Add to body
    document.body.appendChild(notification);

    // Add CSS for notification
    if (!document.querySelector('style[data-notification-styles]')) {
        const style = document.createElement('style');
        style.setAttribute('data-notification-styles', 'true');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 2000;
                animation: slideIn 0.3s ease;
                max-width: 400px;
            }

            .notification-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 1.5rem;
                border-radius: 5px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                gap: 1rem;
            }

            .notification-success .notification-content {
                background-color: #d4edda;
                border-left: 4px solid #28a745;
                color: #155724;
            }

            .notification-error .notification-content {
                background-color: #f8d7da;
                border-left: 4px solid #dc3545;
                color: #721c24;
            }

            .notification-info .notification-content {
                background-color: #d1ecf1;
                border-left: 4px solid #17a2b8;
                color: #0c5460;
            }

            .notification-close {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                color: inherit;
                opacity: 0.7;
                transition: opacity 0.3s ease;
            }

            .notification-close:hover {
                opacity: 1;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @media (max-width: 768px) {
                .notification {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            notification.remove();
        });
    }

    // Auto remove after 5 seconds
    setTimeout(function() {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// ===================================
// Smooth Scroll for Navigation Links
// ===================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            const element = document.querySelector(href);
            const offsetTop = element.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===================================
// Intersection Observer for Animations
// ===================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards and other elements
document.querySelectorAll('.service-card, .info-item').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// ===================================
// Performance Monitoring
// ===================================
window.addEventListener('load', function() {
    if (window.performance && window.performance.timing) {
        const loadTime = window.performance.timing.loadEventEnd - 
                        window.performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    }
});

// ===================================
// Accessibility Features
// ===================================
// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    // Close menu on Escape
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('navMenu');
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    }
});

// ===================================
// Theme Data & API Simulation
// ===================================
const clinicData = {
    name: 'Κλινική Γυναικολογίας',
    doctor: 'Δρ. Μαρία Παπαδοπούλου',
    phone: '+30 210 123 45 67',
    email: 'info@gyneclinic.gr',
    address: 'Οδός Ιατρική 123, 151 24, Αθήνα',
    hours: {
        weekday: '09:00 - 17:00',
        saturday: '10:00 - 13:00',
        sunday: 'Κλειστά'
    },
    services: [
        'Γυναικολογικές Εξετάσεις',
        'Υπερηχογραφίες',
        'Κολποσκοπία',
        'Παπανικολάου'
    ]
};

// Expose for testing/debugging
window.clinicData = clinicData;

// ===================================
// Console Debug Info
// ===================================
console.log('%c Κλινική Γυναικολογίας ', 'background: #0f3460; color: white; font-size: 16px; padding: 10px;');
console.log('Website loaded successfully. For more information, visit the contact page.');
