#!/bin/bash
# 数据库备份脚本

# 从 .env 读取配置
export $(cat .env | grep -v '^#' | xargs)

# 备份目录
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

# 生成备份文件名（带时间戳）
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${DATABASE_NAME}_${TIMESTAMP}.sql"

# 执行备份
echo "开始备份数据库: $DATABASE_NAME"
mysqldump -h $DATABASE_HOST \
          -P $DATABASE_PORT \
          -u $DATABASE_USER \
          -p$DATABASE_PASSWORD \
          $DATABASE_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ 备份成功: $BACKUP_FILE"
    
    # 压缩备份文件
    gzip $BACKUP_FILE
    echo "✅ 压缩完成: $BACKUP_FILE.gz"
    
    # 显示备份文件大小
    ls -lh "$BACKUP_FILE.gz"
    
    # 清理7天前的备份
    find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
    echo "🗑️  已清理7天前的备份文件"
else
    echo "❌ 备份失败"
    exit 1
fi
