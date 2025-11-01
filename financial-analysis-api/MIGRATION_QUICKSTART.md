# 数据库迁移快速参考

## 🎯 当前状态

✅ **已配置完成** - 可以直接使用数据库迁移系统

## 📋 文件清单

```
financial-analysis-api/
├── migrate.py                    # 迁移管理脚本（主要使用）
├── DATABASE_MIGRATION_GUIDE.md   # 完整使用指南
├── backup_db.bat                 # Windows 备份脚本
├── backup_db.sh                  # Linux/Mac 备份脚本
└── alembic/
    ├── env.py                    # 已配置自动模型检测
    ├── alembic.ini               # Alembic 配置
    └── versions/                 # 迁移文件目录
        └── 4f3b2c1a9d3e_add_role_to_users.py
```

## ⚡ 快速开始（3步搞定）

### 方式1：新数据库（推荐）

```bash
cd financial-analysis-api
python migrate.py upgrade
# 完成！✅
```

### 方式2：已有数据库

```bash
cd financial-analysis-api
python migrate.py stamp head  # 标记当前版本
# 完成！✅
```

## 📝 常用命令速查

| 操作 | 命令 | 说明 |
|------|------|------|
| 查看帮助 | `python migrate.py help` | 显示完整帮助 |
| 查看状态 | `python migrate.py current` | 查看当前版本 |
| 创建迁移 | `python migrate.py create "描述"` | 自动检测变化 |
| 应用迁移 | `python migrate.py upgrade` | 升级到最新 |
| 回滚迁移 | `python migrate.py downgrade` | 回退一个版本 |
| 查看历史 | `python migrate.py history` | 查看所有迁移 |

## 🔄 工作流程

### 开发新功能流程

```bash
# 1. 修改模型文件
# 编辑 app/models/user.py

# 2. 创建迁移
python migrate.py create "添加用户新字段"

# 3. 查看生成的迁移文件
# 检查 alembic/versions/ 下新生成的文件

# 4. 应用迁移
python migrate.py upgrade

# 5. 验证
python migrate.py current
```

### 团队协作流程

```bash
# 1. 拉取代码
git pull

# 2. 应用新迁移
python migrate.py upgrade

# 3. 验证
python migrate.py current
```

## 💡 最佳实践

### ✅ 推荐做法

1. **修改模型前先备份**
   ```bash
   # Windows
   backup_db.bat
   
   # Linux/Mac
   bash backup_db.sh
   ```

2. **小步迭代**
   ```bash
   # 好：一次只做一件事
   python migrate.py create "添加email字段"
   python migrate.py create "添加email索引"
   
   # 避免：一次性改太多
   python migrate.py create "重构整个用户系统"
   ```

3. **描述清晰**
   ```bash
   # ✅ 好的描述
   python migrate.py create "用户表添加邮箱验证字段"
   
   # ❌ 不好的描述
   python migrate.py create "update"
   ```

### ❌ 避免的操作

- ❌ 不要删除已应用的迁移文件
- ❌ 不要直接修改数据库结构
- ❌ 不要跳过迁移直接升级
- ❌ 生产环境不要降级

## 🆘 常见问题

### Q1: 如何知道数据库是否需要迁移？

```bash
python migrate.py current   # 查看当前版本
python migrate.py history   # 查看所有迁移
```

如果 current 版本不是最新，需要 upgrade。

### Q2: 迁移失败怎么办？

```bash
# 1. 查看错误信息
python migrate.py current

# 2. 如果需要回滚
python migrate.py downgrade

# 3. 修复问题后重新迁移
python migrate.py upgrade
```

### Q3: 如何在生产环境部署？

```bash
# 1. 测试环境先验证
python migrate.py upgrade

# 2. 生产环境备份
backup_db.bat  # 或 bash backup_db.sh

# 3. 生产环境迁移
python migrate.py upgrade

# 4. 验证
python migrate.py current
```

## 🎓 学习资源

- **完整指南**: `DATABASE_MIGRATION_GUIDE.md`
- **在线帮助**: `python migrate.py help`
- **Alembic 官方文档**: https://alembic.sqlalchemy.org/

## 📞 技术支持

如果遇到问题：
1. 查看 `DATABASE_MIGRATION_GUIDE.md` 常见问题部分
2. 运行 `python migrate.py help` 查看命令说明
3. 检查 `.env` 数据库配置是否正确

---

**版本**: 1.0.0  
**更新日期**: 2025-11-01  
**适用项目**: 金融分析系统 API
