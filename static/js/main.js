// 360° Event Manager - Main JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 76
            }, 1000);
        }
    });

    // Navbar scroll effect
    $(window).scroll(function() {
        if ($(window).scrollTop() > 50) {
            $('.navbar').addClass('navbar-scrolled');
        } else {
            $('.navbar').removeClass('navbar-scrolled');
        }
    });

    // Form validation
    $('.needs-validation').on('submit', function(event) {
        if (!this.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        $(this).addClass('was-validated');
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // 360° Tour functionality
    init360Tour();

    // Search functionality
    initSearch();

    // Notification system
    initNotifications();

    // Chat functionality
    initChat();

    // Initialize all interactive features
    initParticleEffect();
    initScrollProgress();
    initTypingAnimation();
    initSmoothScrolling();
    initCardInteractions();
    initParallaxEffect();
    initLoadingStates();
});

// 360° Tour initialization
function init360Tour() {
    if (typeof pannellum !== 'undefined') {
        const tourContainers = document.querySelectorAll('.tour-container');
        tourContainers.forEach(container => {
            const tourId = container.dataset.tourId;
            if (tourId) {
                pannellum.viewer(container, {
                    type: 'equirectangular',
                    panorama: tourId,
                    autoLoad: true,
                    autoRotate: -2,
                    showControls: true,
                    showFullscreenCtrl: true,
                    showZoomCtrl: true,
                    onLoad: function() {
                        console.log('360° tour loaded');
                    }
                });
            }
        });
    }
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                searchResults.style.display = 'none';
            }
        });

        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
}

// Perform search
function performSearch(query) {
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

// Display search results
function displaySearchResults(data) {
    const searchResults = document.getElementById('search-results');
    if (!searchResults) return;

    let html = '';
    
    if (data.venues && data.venues.length > 0) {
        html += '<div class="search-section"><h6>Venues</h6>';
        data.venues.forEach(venue => {
            html += `<a href="/venues/${venue.slug}/" class="search-item">
                        <div class="search-item-title">${venue.name}</div>
                        <div class="search-item-subtitle">${venue.city}, ${venue.state}</div>
                     </a>`;
        });
        html += '</div>';
    }

    if (data.managers && data.managers.length > 0) {
        html += '<div class="search-section"><h6>Event Managers</h6>';
        data.managers.forEach(manager => {
            html += `<a href="/managers/${manager.slug}/" class="search-item">
                        <div class="search-item-title">${manager.user.get_full_name}</div>
                        <div class="search-item-subtitle">${manager.company_name}</div>
                     </a>`;
        });
        html += '</div>';
    }

    if (data.vendors && data.vendors.length > 0) {
        html += '<div class="search-section"><h6>Vendors</h6>';
        data.vendors.forEach(vendor => {
            html += `<a href="/vendors/${vendor.slug}/" class="search-item">
                        <div class="search-item-title">${vendor.name}</div>
                        <div class="search-item-subtitle">${vendor.category.name}</div>
                     </a>`;
        });
        html += '</div>';
    }

    if (html === '') {
        html = '<div class="search-no-results">No results found</div>';
    }

    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
}

// Notification system
function initNotifications() {
    // Check for new notifications
    if (document.getElementById('notifications-dropdown')) {
        checkNewNotifications();
        setInterval(checkNewNotifications, 30000); // Check every 30 seconds
    }
}

// Check for new notifications
function checkNewNotifications() {
    fetch('/api/notifications/unread/')
        .then(response => response.json())
        .then(data => {
            updateNotificationBadge(data.count);
        })
        .catch(error => {
            console.error('Notification check error:', error);
        });
}

// Update notification badge
function updateNotificationBadge(count) {
    const badge = document.getElementById('notification-badge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline';
        } else {
            badge.style.display = 'none';
        }
    }
}

// Chat functionality
function initChat() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        // Initialize WebSocket connection for real-time chat
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            displayChatMessage(data);
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        // Send message
        const chatForm = document.getElementById('chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const messageInput = document.getElementById('message-input');
                const message = messageInput.value.trim();
                
                if (message) {
                    chatSocket.send(JSON.stringify({
                        'message': message,
                        'room_id': chatContainer.dataset.roomId
                    }));
                    messageInput.value = '';
                }
            });
        }
    }
}

// Display chat message
function displayChatMessage(data) {
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message';
        messageDiv.innerHTML = `
            <div class="chat-message-header">
                <strong>${data.sender_name}</strong>
                <small class="text-muted">${new Date(data.timestamp).toLocaleTimeString()}</small>
            </div>
            <div class="chat-message-content">${data.message}</div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Venue booking functionality
function initVenueBooking() {
    const bookingForms = document.querySelectorAll('.venue-booking-form');
    bookingForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch('/api/venues/book/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Booking request submitted successfully!', 'success');
                    this.reset();
                } else {
                    showAlert(data.error || 'Booking failed. Please try again.', 'danger');
                }
            })
            .catch(error => {
                console.error('Booking error:', error);
                showAlert('An error occurred. Please try again.', 'danger');
            });
        });
    });
}

// Event manager consultation request
function initConsultationRequest() {
    const consultationForms = document.querySelectorAll('.consultation-form');
    consultationForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch('/api/consultations/request/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Consultation request sent successfully!', 'success');
                    this.reset();
                } else {
                    showAlert(data.error || 'Request failed. Please try again.', 'danger');
                }
            })
            .catch(error => {
                console.error('Consultation error:', error);
                showAlert('An error occurred. Please try again.', 'danger');
            });
        });
    });
}

// Payment processing
function initPayment() {
    const paymentForms = document.querySelectorAll('.payment-form');
    paymentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;
            
            fetch('/api/payments/process/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Payment processed successfully!', 'success');
                    window.location.href = data.redirect_url;
                } else {
                    showAlert(data.error || 'Payment failed. Please try again.', 'danger');
                }
            })
            .catch(error => {
                console.error('Payment error:', error);
                showAlert('An error occurred. Please try again.', 'danger');
            })
            .finally(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    });
}

// Utility functions
function showAlert(message, type) {
    const alertContainer = document.getElementById('alert-container') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize additional functionality when DOM is ready
$(document).ready(function() {
    initVenueBooking();
    initConsultationRequest();
    initPayment();
});

// Particle Background Effect
function initParticleEffect() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'particles';
    document.body.appendChild(particlesContainer);
    
    for (let i = 0; i < 50; i++) {
        createParticle(particlesContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    const size = Math.random() * 3 + 1;
    const startX = Math.random() * window.innerWidth;
    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 20;
    
    particle.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${startX}px;
        animation-duration: ${duration}s;
        animation-delay: ${delay}s;
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
            createParticle(container);
        }
    }, duration * 1000);
}

// Scroll Progress Bar
function initScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// Typing Animation
function initTypingAnimation() {
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        heroTitle.classList.add('typing-animation');
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
}

// Smooth Scrolling
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Enhanced Card Interactions
function initCardInteractions() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        // Add hover sound effect (optional)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            addGlowEffect(this);
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            removeGlowEffect(this);
        });
        
        // Add click ripple effect
        card.addEventListener('click', function(e) {
            createRipple(e, this);
        });
    });
}

function addGlowEffect(element) {
    element.style.boxShadow = '0 25px 50px rgba(6, 182, 212, 0.3)';
}

function removeGlowEffect(element) {
    element.style.boxShadow = '';
}

function createRipple(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Parallax Effect
function initParallaxEffect() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax-section');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// Loading States
function initLoadingStates() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('loading')) {
                this.classList.add('loading');
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading-spinner"></span> Loading...';
                
                // Simulate loading (remove in production)
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.innerHTML = originalText;
                }, 2000);
            }
        });
    });
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('[data-aos]').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn.loading {
        pointer-events: none;
        opacity: 0.7;
    }
`;
document.head.appendChild(style);

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close any open modals or dropdowns
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    }
});

// Performance optimization
let ticking = false;

function updateOnScroll() {
    // Update scroll-based animations
    ticking = false;
}

window.addEventListener('scroll', function() {
    if (!ticking) {
        requestAnimationFrame(updateOnScroll);
        ticking = true;
    }
});

// Console welcome message
console.log(`
🎉 Welcome to 360° Event Manager!

🚀 Features loaded:
✅ Particle effects
✅ Scroll progress bar
✅ Typing animations
✅ Smooth scrolling
✅ Enhanced card interactions
✅ Parallax effects
✅ Loading states

🎨 Enjoy the enhanced UI/UX experience!
`); 