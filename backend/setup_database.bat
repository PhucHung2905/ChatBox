@echo off
REM ==================== ChatBox Database Setup Script ====================
REM Chạy SQL migration cho SQL Server

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        ChatBox v2.0 - Database Setup for SQL Server           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Kiểm tra xem sqlcmd có được cài đặt không
where sqlcmd >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: sqlcmd not found!
    echo.
    echo SQL Server command-line tools not installed.
    echo.
    echo 💡 Alternative: Mở setup_database.sql với SQL Server Management Studio
    echo    và chạy script thủ công.
    echo.
    pause
    exit /b 1
)

echo ✅ SQL Server command tools detected
echo.
echo 🗄️  Server: PHUCHUNG\SQLEXPRESS
echo 📊 Database: ChatBoxDB
echo.
echo Đang tạo database và tables...
echo.

REM Chạy SQL script
sqlcmd -S PHUCHUNG\SQLEXPRESS -U PhucHung -P 1234 -i setup_database.sql -o migration_log.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ Database setup completed successfully!
    echo.
    echo 📋 Log file: migration_log.txt
    echo.
    type migration_log.txt
) else (
    echo.
    echo ❌ Error during migration!
    echo.
    echo 📋 Check migration_log.txt for details:
    type migration_log.txt
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                      Setup Complete! ✅                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📊 Database Ready! Tables created:
echo   • users (with 5 indexes)
echo   • chat_histories (with 3 indexes + Foreign Key)
echo   • audit_logs (with 4 indexes)
echo.
echo 🔧 Additional resources:
echo   • Stored Procedures: 2 (sp_GetUserChatStats, sp_GetAdminStats)
echo   • Views: 1 (vw_UserActivitySummary)
echo.
echo 🚀 Next steps:
echo   1. Start backend: python app.py
echo   2. Open browser: http://localhost:5000
echo   3. Login: admin@chatbox.local / admin123
echo.
pause
