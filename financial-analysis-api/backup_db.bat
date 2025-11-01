@echo off
REM 数据库备份脚本（Windows版本）

REM 设置编码为UTF-8
chcp 65001 > nul

REM 读取环境变量
for /f "usebackq tokens=1,2 delims==" %%a in (".env") do (
    if not "%%a"=="" if not "%%a:~0,1%"=="#" (
        set %%a=%%b
    )
)

REM 创建备份目录
if not exist "backups" mkdir backups

REM 生成备份文件名
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set TIMESTAMP=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%_%datetime:~8,2%%datetime:~10,2%%datetime:~12,2%
set BACKUP_FILE=backups\%DATABASE_NAME%_%TIMESTAMP%.sql

REM 执行备份
echo 开始备份数据库: %DATABASE_NAME%
mysqldump -h %DATABASE_HOST% -P %DATABASE_PORT% -u %DATABASE_USER% -p%DATABASE_PASSWORD% %DATABASE_NAME% > %BACKUP_FILE%

if %errorlevel% equ 0 (
    echo ✅ 备份成功: %BACKUP_FILE%
    
    REM 显示备份文件信息
    dir "%BACKUP_FILE%"
    
    echo.
    echo 💡 提示: 建议压缩备份文件以节省空间
    echo    可以使用 7-Zip 或 WinRAR 压缩 %BACKUP_FILE%
) else (
    echo ❌ 备份失败
    exit /b 1
)

pause
