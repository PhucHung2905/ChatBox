-- Script tạo bảng user_info_requests
-- Chạy script này để tạo bảng trong SQL Server

-- Nếu bảng đã tồn tại, xóa nó
IF OBJECT_ID('user_info_requests', 'U') IS NOT NULL 
    DROP TABLE user_info_requests;

-- Tạo bảng
CREATE TABLE user_info_requests (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    message TEXT,
    is_reviewed BIT NOT NULL DEFAULT 0,
    reviewed_by VARCHAR(36) NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT GETUTCDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETUTCDATE()
);

-- Tạo indexes để tối ưu truy vấn
CREATE INDEX idx_user_info_is_reviewed ON user_info_requests(is_reviewed);
CREATE INDEX idx_user_info_phone ON user_info_requests(phone_number);
CREATE INDEX idx_user_info_created_at ON user_info_requests(created_at DESC);
CREATE INDEX idx_user_info_reviewed_by ON user_info_requests(reviewed_by);

-- Grant permissions nếu cần
-- GRANT SELECT, INSERT, UPDATE ON user_info_requests TO [username];

PRINT 'Bảng user_info_requests đã được tạo thành công!';
