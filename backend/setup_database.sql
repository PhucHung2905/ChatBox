-- ==================== ChatBox v2.0 Database Setup ====================
-- Chạy script này trên SQL Server Management Studio
-- Database: ChatBoxDB, Server: PHUCHUNG\SQLEXPRESS

-- ==================== 1. Tạo Database ====================
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'ChatBoxDB')
BEGIN
    CREATE DATABASE ChatBoxDB;
    PRINT 'Database ChatBoxDB created successfully!';
END
ELSE
BEGIN
    PRINT 'Database ChatBoxDB already exists!';
END
GO

USE ChatBoxDB;
GO

-- ==================== 2. Tạo bảng USERS ====================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    CREATE TABLE users (
        id VARCHAR(36) PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(500) NOT NULL,
        full_name VARCHAR(255) NULL,
        is_admin BIT DEFAULT 0,
        is_active BIT DEFAULT 1,
        created_at DATETIME DEFAULT GETUTCDATE(),
        updated_at DATETIME DEFAULT GETUTCDATE(),
        last_login DATETIME NULL
    );
    
    -- Tạo indexes
    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_username ON users(username);
    CREATE INDEX idx_users_is_admin ON users(is_admin);
    CREATE INDEX idx_users_is_active ON users(is_active);
    CREATE INDEX idx_users_created_at ON users(created_at);
    
    PRINT 'Table [users] created successfully with 5 indexes!';
END
ELSE
BEGIN
    PRINT 'Table [users] already exists!';
END
GO

-- ==================== 3. Tạo bảng CHAT_HISTORIES ====================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'chat_histories')
BEGIN
    CREATE TABLE chat_histories (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(36) NOT NULL,
        conversation_id VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        response TEXT NOT NULL,
        context_used INT DEFAULT 0,
        sources TEXT NULL,
        created_at DATETIME DEFAULT GETUTCDATE(),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    
    -- Tạo indexes
    CREATE INDEX idx_chat_histories_user_id ON chat_histories(user_id);
    CREATE INDEX idx_chat_histories_conversation_id ON chat_histories(conversation_id);
    CREATE INDEX idx_chat_histories_created_at ON chat_histories(created_at);
    
    PRINT 'Table [chat_histories] created successfully with 3 indexes and Foreign Key!';
END
ELSE
BEGIN
    PRINT 'Table [chat_histories] already exists!';
END
GO

-- ==================== 4. Tạo bảng AUDIT_LOGS ====================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'audit_logs')
BEGIN
    CREATE TABLE audit_logs (
        id VARCHAR(36) PRIMARY KEY,
        admin_id VARCHAR(36) NOT NULL,
        action VARCHAR(255) NOT NULL,
        target_user_id VARCHAR(36) NULL,
        details TEXT NULL,
        created_at DATETIME DEFAULT GETUTCDATE()
    );
    
    -- Tạo indexes
    CREATE INDEX idx_audit_logs_admin_id ON audit_logs(admin_id);
    CREATE INDEX idx_audit_logs_action ON audit_logs(action);
    CREATE INDEX idx_audit_logs_target_user_id ON audit_logs(target_user_id);
    CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
    
    PRINT 'Table [audit_logs] created successfully with 4 indexes!';
END
ELSE
BEGIN
    PRINT 'Table [audit_logs] already exists!';
END
GO

-- ==================== 5. Tạo Stored Procedure: Get User Stats ====================
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetUserChatStats]'))
BEGIN
    DROP PROCEDURE sp_GetUserChatStats;
END
GO

CREATE PROCEDURE sp_GetUserChatStats
    @UserId VARCHAR(36)
AS
BEGIN
    SELECT 
        COUNT(*) as total_chats,
        COUNT(DISTINCT conversation_id) as total_conversations,
        SUM(context_used) as total_context_used,
        MAX(created_at) as last_chat_date
    FROM chat_histories
    WHERE user_id = @UserId;
END
GO

PRINT 'Stored Procedure [sp_GetUserChatStats] created successfully!';

-- ==================== 6. Tạo Stored Procedure: Get Admin Stats ====================
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetAdminStats]'))
BEGIN
    DROP PROCEDURE sp_GetAdminStats;
END
GO

CREATE PROCEDURE sp_GetAdminStats
AS
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM users) as total_users,
        (SELECT COUNT(*) FROM users WHERE is_active = 1) as active_users,
        (SELECT COUNT(*) FROM users WHERE is_active = 0) as inactive_users,
        (SELECT COUNT(*) FROM users WHERE is_admin = 1) as admin_users,
        (SELECT COUNT(*) FROM chat_histories) as total_chats,
        (SELECT COUNT(*) FROM chat_histories WHERE created_at >= DATEADD(DAY, -1, GETUTCDATE())) as chats_last_24h;
END
GO

PRINT 'Stored Procedure [sp_GetAdminStats] created successfully!';

-- ==================== 7. Tạo View: User Activity Summary ====================
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[vw_UserActivitySummary]'))
BEGIN
    DROP VIEW vw_UserActivitySummary;
END
GO

CREATE VIEW vw_UserActivitySummary AS
SELECT 
    u.id,
    u.email,
    u.username,
    u.full_name,
    u.is_admin,
    u.is_active,
    u.created_at,
    u.last_login,
    COUNT(ch.id) as total_chats,
    COUNT(DISTINCT ch.conversation_id) as total_conversations,
    MAX(ch.created_at) as last_chat_date
FROM users u
LEFT JOIN chat_histories ch ON u.id = ch.user_id
GROUP BY u.id, u.email, u.username, u.full_name, u.is_admin, u.is_active, u.created_at, u.last_login;
GO

PRINT 'View [vw_UserActivitySummary] created successfully!';

-- ==================== 8. Tạo Admin User Mặc Định ====================
DECLARE @AdminId VARCHAR(36) = CAST(NEWID() AS VARCHAR(36));
DECLARE @AdminEmail VARCHAR(255) = 'admin@chatbox.local';
DECLARE @AdminUsername VARCHAR(100) = 'admin';
DECLARE @AdminPassword VARCHAR(500) = '$2b$12$xZ6.S.VzVkDjxQ9pVnzH3OWx8T0YcRGkJ4Z9eDyxFZvZNvZkYvVVe'; -- Hash of 'admin123'

-- Kiểm tra xem admin đã tồn tại chưa
IF NOT EXISTS (SELECT 1 FROM users WHERE email = @AdminEmail)
BEGIN
    INSERT INTO users (id, email, username, password_hash, full_name, is_admin, is_active, created_at, updated_at)
    VALUES (@AdminId, @AdminEmail, @AdminUsername, @AdminPassword, 'Administrator', 1, 1, GETUTCDATE(), GETUTCDATE());
    
    PRINT 'Default admin user created:';
    PRINT '  Email: admin@chatbox.local';
    PRINT '  Password: admin123';
    PRINT '  Please change password after first login!';
END
ELSE
BEGIN
    PRINT 'Admin user already exists!';
END
GO

-- ==================== 9. Xem tóm tắt ====================
SELECT '==== Database Setup Complete ====' as Status;
GO

SELECT 
    'users' as TableName,
    COUNT(*) as RecordCount
FROM users
UNION ALL
SELECT 
    'chat_histories' as TableName,
    COUNT(*) as RecordCount
FROM chat_histories
UNION ALL
SELECT 
    'audit_logs' as TableName,
    COUNT(*) as RecordCount
FROM audit_logs;
GO

-- ==================== 10. Kiểm tra chi tiết ====================
SELECT '===== Table Structure =====' as Info;
GO

SELECT 'users' as TableName, * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users'
UNION ALL
SELECT 'chat_histories' as TableName, * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'chat_histories'
UNION ALL
SELECT 'audit_logs' as TableName, * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'audit_logs';
GO

PRINT '';
PRINT '✅ Database setup completed successfully!';
PRINT '📊 Tables created: 3 (users, chat_histories, audit_logs)';
PRINT '📈 Indexes created: 12';
PRINT '🔧 Stored Procedures: 2 (sp_GetUserChatStats, sp_GetAdminStats)';
PRINT '👁️ Views: 1 (vw_UserActivitySummary)';
PRINT '';
PRINT 'You can now:';
PRINT '  1. Start the Flask application: python app.py';
PRINT '  2. Access frontend: http://localhost:5000';
PRINT '  3. Login with: admin@chatbox.local / admin123';
PRINT '';
