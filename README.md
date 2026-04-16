# BuilderPulse 日报自动推送

自动监控 BuilderPulse 仓库的每日中文日报，并推送到飞书群。

## 功能

- ✅ 每天自动获取 BuilderPulse 的最新中文日报
- ✅ 自动推送到飞书 webhook
- ✅ 支持手动触发
- ✅ 智能查找日报文件（支持多种命名格式）

## 使用方法

### 方式一：GitHub Actions（推荐）

1. **Fork 或创建此仓库**

2. **设置 Secrets（可选）**
   - 进入仓库的 Settings → Secrets and variables → Actions
   - 添加 `FEISHU_WEBHOOK`（如果想隐藏 webhook URL）
   - 如果不设置，会使用代码中的默认 webhook

3. **启用 GitHub Actions**
   - 进入 Actions 标签页
   - 启用工作流

4. **自动运行**
   - 每天北京时间 9:00 自动运行
   - 也可以手动触发：Actions → 选择工作流 → Run workflow

### 方式二：本地运行

```bash
# 安装依赖
pip install requests

# 运行脚本
python3 send_daily_report.py
```

### 方式三：使用 cron 定时任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 9:00 运行）
0 9 * * * cd /path/to/BuilderPulse && python3 send_daily_report.py
```

## 配置说明

### 飞书 Webhook

当前配置的 webhook 地址：
```
https://open.larksuite.com/open-apis/bot/v2/hook/5f789770-cd88-4846-aaea-702e38eaaff0
```

如需修改：
- GitHub Actions: 修改 `.github/workflows/daily-report.yml` 中的 `FEISHU_WEBHOOK`
- 本地脚本: 修改 `send_daily_report.py` 中的 `FEISHU_WEBHOOK`

### 运行时间

默认每天北京时间 9:00 运行。修改时间：

编辑 `.github/workflows/daily-report.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 1 * * *'  # UTC 1:00 = 北京时间 9:00
```

常用时间对照：
- 北京时间 8:00 → `0 0 * * *`
- 北京时间 9:00 → `0 1 * * *`
- 北京时间 10:00 → `0 2 * * *`
- 北京时间 18:00 → `0 10 * * *`

## 日报文件查找逻辑

脚本会按以下顺序查找日报：

1. `reports/YYYY-MM-DD_zh.md`
2. `reports/YYYY-MM-DD.md`
3. `daily/YYYY-MM-DD_zh.md`
4. `daily/YYYY-MM-DD.md`
5. `YYYY-MM-DD_zh.md`
6. `YYYY-MM-DD.md`
7. `README.md`
8. 最新的包含"中文"或"zh"的 markdown 文件

## 故障排查

### GitHub Actions 未运行

1. 检查 Actions 是否已启用
2. 查看 Actions 标签页的运行日志
3. 确认 cron 时间设置正确

### 飞书未收到消息

1. 检查 webhook URL 是否正确
2. 确认飞书机器人未被禁用
3. 查看 Actions 运行日志中的错误信息

### 找不到日报

1. 确认 BuilderPulse 仓库中有日报文件
2. 检查文件命名格式是否匹配
3. 查看 Actions 日志中的文件查找过程

## 手动测试

```bash
# 测试本地脚本
python3 send_daily_report.py

# 测试 GitHub Actions（需要 act 工具）
act workflow_dispatch -j send-daily-report
```

## 文件说明

- `.github/workflows/daily-report.yml` - GitHub Actions 工作流配置
- `send_daily_report.py` - 本地运行脚本
- `README.md` - 本文档

## 更新日志

- 2026-04-16: 初始版本，支持 GitHub Actions 和本地运行
