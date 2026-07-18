// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

// Global Auth Helpers
function getCurrentUser() {
    const userStr = localStorage.getItem('currentUser');
    return userStr ? JSON.parse(userStr) : null;
}

function setCurrentUser(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
}

function logout() {
    localStorage.removeItem('currentUser');
    showNotification('Logged out successfully!');
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 1000);
}

// Show Custom Notification
function showNotification(message) {
    const banner = document.getElementById('notification-banner');
    if (banner) {
        banner.querySelector('.notification-content').innerText = message;
        banner.classList.add('active');
        setTimeout(() => {
            banner.classList.remove('active');
        }, 3000);
    } else {
        alert(message);
    }
}

// API Fetch Helper
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Default headers
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (options.body && typeof options.body === 'object') {
        options.body = JSON.stringify(options.body);
    }
    
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Something went wrong');
        }
        return data;
    } catch (error) {
        console.error(`API Error on ${endpoint}:`, error);
        showNotification(error.message);
        throw error;
    }
}

// Update Navbar Links and Actions
function updateNavbar() {
    const user = getCurrentUser();
    const navActions = document.getElementById('nav-actions');
    const navLinks = document.getElementById('nav-links');
    
    if (!navActions || !navLinks) return;
    
    // Update links depending on role
    let linksHtml = `
        <li><a href="index.html" class="nav-link">Home</a></li>
        <li><a href="events.html" class="nav-link">Browse Events</a></li>
    `;
    
    if (user) {
        if (user.role === 'admin') {
            linksHtml += `<li><a href="admin_dashboard.html" class="nav-link">Admin Panel</a></li>`;
        } else if (user.role === 'organizer') {
            linksHtml += `<li><a href="organizer_dashboard.html" class="nav-link">Organizer Dashboard</a></li>`;
        } else {
            linksHtml += `
                <li><a href="user_dashboard.html" class="nav-link">Dashboard</a></li>
                <li><a href="booking_history.html" class="nav-link">Booking History</a></li>
            `;
        }
        navLinks.innerHTML = linksHtml;
        
        navActions.innerHTML = `
            <span style="font-weight:600; color:var(--accent);">Hi, ${user.full_name} (${user.role})</span>
            <button onclick="logout()" class="btn btn-secondary btn-sm">Logout</button>
        `;
    } else {
        navLinks.innerHTML = linksHtml;
        navActions.innerHTML = `
            <a href="login.html" class="btn btn-secondary btn-sm">Login</a>
            <a href="register.html" class="btn btn-primary btn-sm">Register</a>
        `;
    }
    
    // Set active link
    const path = window.location.pathname;
    const page = path.substring(path.lastIndexOf('/') + 1);
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href === page) {
            link.classList.add('active');
        }
    });
}

// Redirect if not authorized
function checkAuth(requiredRole = null) {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'login.html';
        return false;
    }
    if (requiredRole && user.role !== requiredRole) {
        showNotification('Unauthorized access.');
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Document Ready Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Inject notification banner element if missing
    if (!document.getElementById('notification-banner')) {
        const banner = document.createElement('div');
        banner.id = 'notification-banner';
        banner.className = 'notification-banner';
        banner.innerHTML = `
            <span class="notification-icon">✦</span>
            <span class="notification-content"></span>
        `;
        document.body.appendChild(banner);
    }
    
    updateNavbar();
});
