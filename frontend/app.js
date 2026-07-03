const API_URL = 'http://localhost:8000';

// Token Management
const TokenManager = {
    setTokens(accessToken, refreshToken) {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
    },

    getAccessToken() {
        return localStorage.getItem('accessToken');
    },

    getRefreshToken() {
        return localStorage.getItem('refreshToken');
    },

    clearTokens() {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    },

    isAuthenticated() {
        return this.getAccessToken() !== null;
    }
};

// API Helper
async function apiCall(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    const accessToken = TokenManager.getAccessToken();
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const options = {
        method,
        headers
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await refreshAccessToken();
            if (refreshed) {
                return apiCall(endpoint, method, data);
            } else {
                logout();
                return null;
            }
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Refresh Token
async function refreshAccessToken() {
    const refreshToken = TokenManager.getRefreshToken();
    if (!refreshToken) return false;

    try {
        const response = await fetch(`${API_URL}/auth_service/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            TokenManager.setTokens(data.access_token, data.refresh_token);
            return true;
        }
        return false;
    } catch (error) {
        console.error('Refresh Error:', error);
        return false;
    }
}

// Page Navigation
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    document.getElementById(pageName).classList.add('active');

    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });

    // Load page-specific data
    if (pageName === 'profile') {
        loadProfile();
    } else if (pageName === 'admin') {
        loadAdminData();
    }
}

// Update Navigation Menu
function updateNavigation() {
    const isAuth = TokenManager.isAuthenticated();
    const profileLink = document.querySelector('[data-page="profile"]');
    const adminLink = document.querySelector('[data-page="admin"]');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginLink = document.querySelector('[data-page="login"]');
    const registerLink = document.querySelector('[data-page="register"]');

    if (isAuth) {
        profileLink.style.display = 'block';
        adminLink.style.display = 'block';
        logoutBtn.style.display = 'block';
        loginLink.style.display = 'none';
        registerLink.style.display = 'none';
        showPage('profile');
    } else {
        profileLink.style.display = 'none';
        adminLink.style.display = 'none';
        logoutBtn.style.display = 'none';
        loginLink.style.display = 'block';
        registerLink.style.display = 'block';
        showPage('home');
    }
}

// Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorDiv = document.getElementById('loginError');
    errorDiv.classList.remove('show');

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const result = await apiCall('/auth_service/login', 'POST', {
        username,
        password
    });

    if (result && result.access_token) {
        TokenManager.setTokens(result.access_token, result.refresh_token);
        updateNavigation();
    } else {
        errorDiv.textContent = 'Ошибка входа. Проверьте данные.';
        errorDiv.classList.add('show');
    }
});

// Register
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    errorDiv.classList.remove('show');
    successDiv.classList.remove('show');

    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    const result = await apiCall('/auth_service/register', 'POST', {
        username,
        email,
        password
    });

    if (result && result !== null) {
        successDiv.textContent = 'Регистрация успешна! Письмо отправлено на вашу почту.';
        successDiv.classList.add('show');
        document.getElementById('registerForm').reset();
    } else {
        errorDiv.textContent = 'Ошибка регистрации. Проверьте данные.';
        errorDiv.classList.add('show');
    }
});

// Load Profile
async function loadProfile() {
    const profileContent = document.getElementById('profileContent');
    const profileError = document.getElementById('profileError');
    profileError.classList.remove('show');

    const user = await apiCall('/auth_service/me');

    if (user && user.username) {
        profileContent.innerHTML = `
            <p><strong>Имя пользователя:</strong> ${escapeHtml(user.username)}</p>
            <p><strong>Email:</strong> ${escapeHtml(user.email || 'N/A')}</p>
            <p><strong>ID:</strong> ${user.id || 'N/A'}</p>
            <p><strong>Дата создания:</strong> ${user.created_at ? new Date(user.created_at).toLocaleString('ru-RU') : 'N/A'}</p>
        `;
    } else {
        profileError.textContent = 'Ошибка загрузки профиля.';
        profileError.classList.add('show');
    }
}

// Refresh Profile
function refreshProfile() {
    loadProfile();
}

// Load Admin Data
async function loadAdminData() {
    const adminContent = document.getElementById('adminContent');
    const adminError = document.getElementById('adminError');
    adminError.classList.remove('show');

    const result = await apiCall('/admin_service/users');

    if (result && Array.isArray(result)) {
        if (result.length === 0) {
            adminContent.innerHTML = '<p>Нет пользователей.</p>';
        } else {
            adminContent.innerHTML = result.map(user => `
                <div class="user-item">
                    <p><strong>Имя:</strong> ${escapeHtml(user.username)}</p>
                    <p><strong>Email:</strong> ${escapeHtml(user.email || 'N/A')}</p>
                    <p><strong>ID:</strong> ${user.id}</p>
                    <p><strong>Создан:</strong> ${user.created_at ? new Date(user.created_at).toLocaleString('ru-RU') : 'N/A'}</p>
                </div>
            `).join('');
        }
    } else {
        adminError.textContent = 'Ошибка загрузки данных администратора. Проверьте права доступа.';
        adminError.classList.add('show');
    }
}

// Logout
function logout() {
    const refreshToken = TokenManager.getRefreshToken();
    if (refreshToken) {
        apiCall('/auth_service/logout', 'POST', {
            refresh_token: refreshToken
        });
    }
    TokenManager.clearTokens();
    updateNavigation();
}

document.getElementById('logoutBtn').addEventListener('click', logout);

// Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Page Link Handlers
document.querySelectorAll('[data-page]').forEach(link => {
    link.addEventListener('click', (e) => {
        if (link.dataset.page && !link.classList.contains('btn-logout')) {
            e.preventDefault();
            showPage(link.dataset.page);
        }
    });
});

// Initialize on page load
window.addEventListener('load', () => {
    updateNavigation();
});