// ==================== Authentication Check ====================
// Kiểm tra xem đã đăng nhập chưa trước khi load trang
(() => {
    const token = localStorage.getItem('authToken');
    const currentUser = localStorage.getItem('currentUser');
    
    // Nếu chưa đăng nhập, redirect đến login
    if (!token || !currentUser) {
        window.location.href = 'login.html';
        return;
    }
})();

// ==================== Global State ====================
const state = {
    backendUrl: localStorage.getItem('backendUrl') || 'http://localhost:5000',
    token: localStorage.getItem('authToken') || null,
    currentUser: JSON.parse(localStorage.getItem('currentUser') || 'null'),
    conversationId: 'chat_' + Date.now(),
    contextCount: parseInt(localStorage.getItem('contextCount') || '5'),
    isLoading: false,
    kbLoaded: false
};

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', () => {
    // Khởi tạo main app (vì index.html chỉ là trang chính)
    showMainApp();
    setupMainAppListeners();
    verifyToken();
});

// ==================== Authentication ====================
function showMainApp() {
    document.getElementById('mainApp').classList.remove('hidden');
    updateUserDisplay();
    checkAdminRole();
}

async function verifyToken() {
    try {
        const response = await fetch(`${state.backendUrl}/api/auth/verify`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        
        if (!data.success) {
            logout();
        }
    } catch (error) {
        console.error('Token verification failed:', error);
    }
}

function logout() {
    state.token = null;
    state.currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}

function updateUserDisplay() {
    document.getElementById('userName').textContent = state.currentUser.full_name || state.currentUser.username;
    document.getElementById('userRole').textContent = state.currentUser.is_admin ? 'Admin' : 'User';
}

function checkAdminRole() {
    const adminMenu = document.getElementById('adminMenu');
    if (state.currentUser.is_admin) {
        adminMenu.classList.remove('hidden');
    } else {
        adminMenu.classList.add('hidden');
    }
}

// ==================== Main App Setup ====================
function setupMainAppListeners() {
    // Navigation
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => switchSection(btn.dataset.section));
    });
    
    // Chat
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Clear and Logout
    document.getElementById('clearChat').addEventListener('click', clearChat);
    document.getElementById('logoutBtn').addEventListener('click', logout);
    
    // Search
    document.getElementById('searchBtn').addEventListener('click', performSearch);
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
    
    // Knowledge Base
    document.getElementById('loadKB').addEventListener('click', loadKB);
    document.getElementById('reInitKB').addEventListener('click', initializeKB);
    
    // Settings
    document.getElementById('testConnection').addEventListener('click', testConnection);
    document.getElementById('backendUrl').addEventListener('change', (e) => {
        state.backendUrl = e.target.value;
        localStorage.setItem('backendUrl', state.backendUrl);
    });
    document.getElementById('updateProfileBtn').addEventListener('click', updateProfile);
    document.getElementById('changePasswordBtn').addEventListener('click', changePassword);
    
    // Load initial data
    loadUserChatHistory();
    getKBInfo();
    document.getElementById('userFullName').value = state.currentUser.full_name || '';
}

// ==================== Section Navigation ====================
function switchSection(sectionId) {
    // Convert kebab-case to camelCase (kb-info -> kbInfo, admin-users -> adminUsers)
    const sectionName = sectionId.replace(/-([a-z])/g, (match, letter) => letter.toUpperCase());
    
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    // Show selected section
    const targetSection = document.getElementById(sectionName + 'Section');
    if (targetSection) {
        targetSection.classList.add('active');
    } else {
        console.error(`Section ${sectionName}Section not found`);
        return;
    }
    
    // Update nav button active state
    document.querySelectorAll('.nav-btn').forEach(btn => {
        if (btn.dataset.section === sectionId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Load section-specific data
    if (sectionId === 'history') {
        loadUserChatHistory();
    } else if (sectionId === 'admin-users') {
        loadAdminUsers();
    } else if (sectionId === 'admin-audit') {
        loadAdminAuditLogs();
    } else if (sectionId === 'admin-stats') {
        loadAdminStats();
    }
}

// ==================== Chat Functionality ====================
async function sendMessage() {
    const message = document.getElementById('messageInput').value.trim();
    
    if (!message || state.isLoading) return;
    
    state.isLoading = true;
    document.getElementById('sendBtn').disabled = true;
    
    // Add user message to UI
    addMessageToChat(message, 'user');
    document.getElementById('messageInput').value = '';
    
    try {
        const response = await fetch(`${state.backendUrl}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.token}`
            },
            body: JSON.stringify({
                message,
                conversation_id: state.conversationId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat(data.response, 'assistant');
            document.getElementById('contextInfo').textContent = `📚 Sử dụng ${data.context_used} tài liệu tham khảo`;
        } else {
            addMessageToChat('❌ Lỗi: ' + data.error, 'error');
        }
    } catch (error) {
        addMessageToChat('❌ Lỗi kết nối: ' + error.message, 'error');
    } finally {
        state.isLoading = false;
        document.getElementById('sendBtn').disabled = false;
        document.getElementById('messageInput').focus();
    }
}

function addMessageToChat(message, role) {
    const chatMessages = document.getElementById('chatMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    // Parse Markdown để hiển thị đúng định dạng
    if (role === 'assistant' || role === 'system') {
        // Cấu hình marked để hỗ trợ Markdown
        marked.setOptions({
            breaks: true,
            gfm: true,
        });
        
        // Convert Markdown thành HTML
        const htmlContent = marked.parse(message);
        
        // Sanitize HTML để tránh XSS
        const cleanHTML = DOMPurify.sanitize(htmlContent, {
            ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'hr', 'code', 'pre', 'a'],
            ALLOWED_ATTR: ['href', 'target', 'rel']
        });
        
        messageEl.innerHTML = cleanHTML;
    } else {
        // User messages không cần parse
        messageEl.textContent = message;
    }
    
    chatMessages.appendChild(messageEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function clearChat() {
    if (!confirm('Bạn chắc chắn muốn xóa lịch sử trò chuyện?')) return;
    
    try {
        await fetch(`${state.backendUrl}/api/clear-conversation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.token}`
            },
            body: JSON.stringify({ conversation_id: state.conversationId })
        });
        
        document.getElementById('chatMessages').innerHTML = '<div class="message system"><p>💬 Cuộc trò chuyện đã được xóa</p></div>';
        state.conversationId = 'chat_' + Date.now();
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

// ==================== Search ====================
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) return;
    
    try {
        const response = await fetch(`${state.backendUrl}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.token}`
            },
            body: JSON.stringify({ query, k: state.contextCount })
        });
        
        const data = await response.json();
        
        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = '';
        
        if (data.success && data.results.length > 0) {
            data.results.forEach((result, index) => {
                const resultEl = document.createElement('div');
                resultEl.className = 'search-result';
                resultEl.innerHTML = `
                    <h4>Kết quả ${index + 1}</h4>
                    <p>${result.content}</p>
                    <small>Độ liên quan: ${(result.similarity * 100).toFixed(1)}%</small>
                `;
                resultsDiv.appendChild(resultEl);
            });
        } else {
            resultsDiv.innerHTML = '<p>Không tìm thấy kết quả</p>';
        }
    } catch (error) {
        document.getElementById('searchResults').innerHTML = '<p>❌ Lỗi tìm kiếm: ' + error.message + '</p>';
    }
}

// ==================== Chat History ====================
async function loadUserChatHistory() {
    try {
        const response = await fetch(`${state.backendUrl}/api/chat-history?page=1&per_page=50`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        const historyList = document.getElementById('chatHistoryList');
        
        historyList.innerHTML = '';
        
        if (data.success && data.chat_history.length > 0) {
            data.chat_history.forEach(chat => {
                const chatEl = document.createElement('div');
                chatEl.className = 'chat-history-item';
                
                // Hàm cắt text an toàn với tiếng Việt
                const truncateText = (text, maxLength) => {
                    if (!text) return '';
                    // Cắt bởi ký tự, không phải byte
                    const truncated = text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
                    return truncated;
                };
                
                // Tạo các thành phần riêng để tránh lỗi encoding
                const userLabel = document.createElement('p');
                userLabel.innerHTML = '<strong>Tôi:</strong> ';
                const userText = document.createElement('span');
                userText.textContent = truncateText(chat.message, 100);
                userLabel.appendChild(userText);
                
                const botLabel = document.createElement('p');
                botLabel.innerHTML = '<strong>Bot:</strong> ';
                const botText = document.createElement('span');
                botText.textContent = truncateText(chat.response, 100);
                botLabel.appendChild(botText);
                
                const timeEl = document.createElement('small');
                timeEl.textContent = new Date(chat.created_at).toLocaleString('vi-VN');
                
                chatEl.appendChild(userLabel);
                chatEl.appendChild(botLabel);
                chatEl.appendChild(timeEl);
                
                historyList.appendChild(chatEl);
            });
        } else {
            const noHistoryMsg = document.createElement('p');
            noHistoryMsg.textContent = 'Không có lịch sử trò chuyện';
            historyList.appendChild(noHistoryMsg);
        }
    } catch (error) {
        const errorEl = document.createElement('p');
        errorEl.textContent = '❌ Lỗi: ' + error.message;
        document.getElementById('chatHistoryList').innerHTML = '';
        document.getElementById('chatHistoryList').appendChild(errorEl);
    }
}

// ==================== Knowledge Base ====================
async function getKBInfo() {
    try {
        const response = await fetch(`${state.backendUrl}/api/knowledge-base-info`);
        const data = await response.json();
        
        document.getElementById('docCount').textContent = data.documents_count;
        document.getElementById('embeddingModel').textContent = data.embeddings_model;
        document.getElementById('llmModel').textContent = data.llm_model;
        document.getElementById('kbStatus').textContent = data.has_index ? '✅ Đã tải' : '⚠️ Chưa tải';
        state.kbLoaded = data.has_index;
    } catch (error) {
        console.error('Error loading KB info:', error);
    }
}

async function loadKB() {
    try {
        const response = await fetch(`${state.backendUrl}/api/load-knowledge-base`, {
            method: 'POST'
        });
        
        const data = await response.json();
        alert(data.success ? '✓ ' + data.message : '✗ ' + data.message);
        getKBInfo();
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function initializeKB() {
    if (!confirm('Tạo lại cơ sở dữ liệu? (Quá trình này có thể mất vài phút)')) return;
    
    try {
        const response = await fetch(`${state.backendUrl}/api/init-knowledge-base`, {
            method: 'POST'
        });
        
        const data = await response.json();
        alert(data.success ? '✓ ' + data.message : '✗ ' + data.message);
        getKBInfo();
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

// ==================== Settings ====================
async function updateProfile() {
    const fullName = document.getElementById('userFullName').value.trim();
    
    if (!fullName) {
        alert('Vui lòng nhập tên đầy đủ');
        return;
    }
    
    try {
        const response = await fetch(`${state.backendUrl}/api/auth/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.token}`
            },
            body: JSON.stringify({ full_name: fullName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            state.currentUser = data.user;
            localStorage.setItem('currentUser', JSON.stringify(state.currentUser));
            updateUserDisplay();
            alert('✓ Cập nhật hồ sơ thành công');
        } else {
            alert('✗ ' + data.error);
        }
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function changePassword() {
    const oldPassword = document.getElementById('oldPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmNewPassword').value;
    
    if (!oldPassword || !newPassword || !confirmPassword) {
        alert('Vui lòng điền tất cả các trường');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        alert('Mật khẩu mới không khớp');
        return;
    }
    
    if (newPassword.length < 6) {
        alert('Mật khẩu mới phải tối thiểu 6 ký tự');
        return;
    }
    
    try {
        const response = await fetch(`${state.backendUrl}/api/auth/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${state.token}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✓ Đổi mật khẩu thành công');
            document.getElementById('oldPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmNewPassword').value = '';
        } else {
            alert('✗ ' + data.error);
        }
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function testConnection() {
    try {
        const response = await fetch(`${state.backendUrl}/health`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            alert('✓ Kết nối thành công');
        } else {
            alert('✗ Kết nối thất bại');
        }
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

// ==================== Admin Features ====================
async function loadAdminUsers(page = 1) {
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/users?page=${page}&per_page=20`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        const usersTable = document.getElementById('usersTable');
        
        usersTable.innerHTML = '';
        
        if (data.success && data.users.length > 0) {
            const table = document.createElement('table');
            table.className = 'admin-table';
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Tên người dùng</th>
                        <th>Quyền</th>
                        <th>Trạng thái</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
            `;
            
            data.users.forEach(user => {
                table.innerHTML += `
                    <tr>
                        <td>${user.email}</td>
                        <td>${user.full_name || user.username}</td>
                        <td>${user.is_admin ? '🔑 Admin' : '👤 User'}</td>
                        <td>${user.is_active ? '✅ Active' : '❌ Inactive'}</td>
                        <td>
                            <button onclick="viewUserDetail('${user.id}')" class="btn-small">Xem</button>
                            ${!user.is_admin ? `<button onclick="promoteUser('${user.id}')" class="btn-small">Nâng cấp</button>` : ''}
                            ${user.is_active ? `<button onclick="deactivateUser('${user.id}')" class="btn-small" style="background:#e74c3c;">Vô hiệu</button>` : `<button onclick="activateUser('${user.id}')" class="btn-small">Kích hoạt</button>`}
                        </td>
                    </tr>
                `;
            });
            
            table.innerHTML += '</tbody></table>';
            usersTable.appendChild(table);
        } else {
            usersTable.innerHTML = '<p>Không có người dùng</p>';
        }
    } catch (error) {
        document.getElementById('usersTable').innerHTML = '<p>❌ Lỗi: ' + error.message + '</p>';
    }
}

async function promoteUser(userId) {
    if (!confirm('Bạn chắc chắn muốn nâng cấp người dùng này lên Admin?')) return;
    
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/users/${userId}/promote`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        alert(data.success ? '✓ ' + data.message : '✗ ' + data.error);
        loadAdminUsers();
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function deactivateUser(userId) {
    if (!confirm('Bạn chắc chắn muốn vô hiệu hóa người dùng này?')) return;
    
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/users/${userId}/deactivate`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        alert(data.success ? '✓ ' + data.message : '✗ ' + data.error);
        loadAdminUsers();
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function activateUser(userId) {
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/users/${userId}/activate`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        alert(data.success ? '✓ ' + data.message : '✗ ' + data.error);
        loadAdminUsers();
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function viewUserDetail(userId) {
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/users/${userId}`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const user = data.user;
            alert(`
Email: ${user.email}
Người dùng: ${user.username}
Tên: ${user.full_name}
Quyền: ${user.is_admin ? 'Admin' : 'User'}
Trạng thái: ${user.is_active ? 'Active' : 'Inactive'}
Tổng chat: ${user.chat_statistics.total_chats}
Chat lần cuối: ${user.chat_statistics.last_chat ? new Date(user.chat_statistics.last_chat).toLocaleString('vi-VN') : 'N/A'}
            `);
        }
    } catch (error) {
        alert('❌ Lỗi: ' + error.message);
    }
}

async function loadAdminAuditLogs(page = 1) {
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/audit-logs?page=${page}&per_page=50`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        const logsTable = document.getElementById('auditLogsTable');
        
        logsTable.innerHTML = '';
        
        if (data.success && data.audit_logs.length > 0) {
            const table = document.createElement('table');
            table.className = 'admin-table';
            table.innerHTML = `
                <thead>
                    <tr>
                        <th>Hành động</th>
                        <th>Người thực hiện</th>
                        <th>Mục tiêu</th>
                        <th>Thời gian</th>
                    </tr>
                </thead>
                <tbody>
            `;
            
            data.audit_logs.forEach(log => {
                table.innerHTML += `
                    <tr>
                        <td>${log.action}</td>
                        <td>${log.admin_id}</td>
                        <td>${log.target_user_id || 'N/A'}</td>
                        <td>${new Date(log.created_at).toLocaleString('vi-VN')}</td>
                    </tr>
                `;
            });
            
            table.innerHTML += '</tbody></table>';
            logsTable.appendChild(table);
        } else {
            logsTable.innerHTML = '<p>Không có audit log</p>';
        }
    } catch (error) {
        document.getElementById('auditLogsTable').innerHTML = '<p>❌ Lỗi: ' + error.message + '</p>';
    }
}

async function loadAdminStats() {
    try {
        const response = await fetch(`${state.backendUrl}/api/admin/stats`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        
        const data = await response.json();
        const statsDiv = document.getElementById('adminStats');
        
        statsDiv.innerHTML = '';
        
        if (data.success) {
            const stats = data.stats;
            statsDiv.innerHTML = `
                <div class="stat-card">
                    <h3>Tổng User</h3>
                    <p class="stat-number">${stats.total_users}</p>
                </div>
                <div class="stat-card">
                    <h3>User Active</h3>
                    <p class="stat-number">${stats.active_users}</p>
                </div>
                <div class="stat-card">
                    <h3>User Inactive</h3>
                    <p class="stat-number">${stats.inactive_users}</p>
                </div>
                <div class="stat-card">
                    <h3>Admin</h3>
                    <p class="stat-number">${stats.admin_users}</p>
                </div>
                <div class="stat-card">
                    <h3>Tổng Chat</h3>
                    <p class="stat-number">${stats.total_chats}</p>
                </div>
                <div class="stat-card">
                    <h3>Active 24h</h3>
                    <p class="stat-number">${stats.active_users_last_24h}</p>
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('adminStats').innerHTML = '<p>❌ Lỗi: ' + error.message + '</p>';
    }
}
