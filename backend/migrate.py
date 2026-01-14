"""
SQL Server Migration/Setup Script
Tạo database schema cho ChatBox v2.0
"""

# Create and run this script to set up SQL Server database

SQL_MIGRATION = """
-- ==================== Database ====================
-- Nếu database chưa tồn tại, tạo mới
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'ChatBoxDB')
BEGIN
    CREATE DATABASE ChatBoxDB;
END
GO

USE ChatBoxDB;
GO

-- ==================== Tables ====================

-- Users Table
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
        last_login DATETIME NULL,
    );
    
    -- Create indexes
    CREATE INDEX idx_users_email ON users(email);
    CREATE INDEX idx_users_username ON users(username);
    CREATE INDEX idx_users_is_admin ON users(is_admin);
    CREATE INDEX idx_users_is_active ON users(is_active);
    CREATE INDEX idx_users_created_at ON users(created_at);
    
    PRINT 'Created table: users';
END
GO

-- Chat History Table
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
    
    -- Create indexes
    CREATE INDEX idx_chat_histories_user_id ON chat_histories(user_id);
    CREATE INDEX idx_chat_histories_conversation_id ON chat_histories(conversation_id);
    CREATE INDEX idx_chat_histories_created_at ON chat_histories(created_at);
    
    PRINT 'Created table: chat_histories';
END
GO

-- Audit Logs Table
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
    
    -- Create indexes
    CREATE INDEX idx_audit_logs_admin_id ON audit_logs(admin_id);
    CREATE INDEX idx_audit_logs_action ON audit_logs(action);
    CREATE INDEX idx_audit_logs_target_user_id ON audit_logs(target_user_id);
    CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
    
    PRINT 'Created table: audit_logs';
END
GO

-- ==================== Stored Procedures ====================

-- Procedure: Get user chat statistics
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
        MIN(created_at) as first_chat,
        MAX(created_at) as last_chat
    FROM chat_histories
    WHERE user_id = @UserId;
END
GO

PRINT 'Created stored procedure: sp_GetUserChatStats';

-- Procedure: Get admin statistics
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
        (SELECT COUNT(DISTINCT user_id) FROM users WHERE last_login >= DATEADD(hour, -24, GETUTCDATE())) as active_users_last_24h;
END
GO

PRINT 'Created stored procedure: sp_GetAdminStats';

-- ==================== Views ====================

-- View: User activity summary
IF EXISTS (SELECT * FROM sys.views WHERE name = 'vw_UserActivitySummary')
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
    MIN(ch.created_at) as first_chat_date,
    MAX(ch.created_at) as last_chat_date
FROM users u
LEFT JOIN chat_histories ch ON u.id = ch.user_id
GROUP BY u.id, u.email, u.username, u.full_name, u.is_admin, u.is_active, u.created_at, u.last_login;

PRINT 'Created view: vw_UserActivitySummary';

GO

-- ==================== Default Admin User ====================
-- Tạo tài khoản admin mặc định
-- Password: admin123 (sẽ được hash bởi Flask)

DECLARE @AdminId VARCHAR(36) = LOWER(NEWID());
DECLARE @AdminEmail VARCHAR(255) = 'admin@chatbox.local';
DECLARE @AdminUsername VARCHAR(100) = 'admin';
DECLARE @AdminFullName VARCHAR(255) = 'Administrator';

IF NOT EXISTS (SELECT 1 FROM users WHERE email = @AdminEmail)
BEGIN
    INSERT INTO users (id, email, username, password_hash, full_name, is_admin, is_active)
    VALUES (
        @AdminId,
        @AdminEmail,
        @AdminUsername,
        'pbkdf2:sha256$260000$', -- Placeholder - sẽ được cập nhật khi app khởi động
        @AdminFullName,
        1,
        1
    );
    
    PRINT 'Created default admin user: ' + @AdminEmail;
END
ELSE
BEGIN
    PRINT 'Admin user already exists: ' + @AdminEmail;
END

GO

-- ==================== Summary ====================
PRINT '===============================================';
PRINT 'SQL Server Database Setup Complete!';
PRINT '===============================================';
PRINT '';
PRINT 'Database: ChatBoxDB';
PRINT 'Tables created:';
PRINT '  - users (Người dùng)';
PRINT '  - chat_histories (Lịch sử trò chuyện)';
PRINT '  - audit_logs (Nhật ký kiểm tra)';
PRINT '';
PRINT 'Views created:';
PRINT '  - vw_UserActivitySummary';
PRINT '';
PRINT 'Stored Procedures created:';
PRINT '  - sp_GetUserChatStats';
PRINT '  - sp_GetAdminStats';
PRINT '';
PRINT 'Next steps:';
PRINT '1. Update connection string in .env file';
PRINT '2. Run: pip install -r requirements.txt';
PRINT '3. Run: python app.py';
PRINT '';
"""

if __name__ == '__main__':
    import pyodbc
    from config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER, DB_TRUSTED_CONNECTION
    
    try:
        # Connect to SQL Server
        if DB_TRUSTED_CONNECTION:
            connection_string = f'Driver={DB_DRIVER};Server={DB_SERVER};Database=master;Trusted_Connection=yes;'
        else:
            connection_string = f'Driver={DB_DRIVER};Server={DB_SERVER};Database=master;UID={DB_USER};PWD={DB_PASSWORD};'
        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        print("✓ Connected to SQL Server")
        
        # Execute migration script
        for statement in SQL_MIGRATION.split('GO'):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        print("\nManual setup:")
        print("1. Open SQL Server Management Studio")
        print("2. Connect to your SQL Server instance")
        print("3. Copy and paste the SQL_MIGRATION script above")
        print("4. Execute the script")
