#!/usr/bin/env python3
"""
BuilderPulse 日报推送脚本
每天自动获取中文日报并推送到飞书
"""

import requests
import json
from datetime import datetime

# 配置
GITHUB_REPO = "BuilderPulse/BuilderPulse"
FEISHU_WEBHOOK = "https://open.larksuite.com/open-apis/bot/v2/hook/5f789770-cd88-4846-aaea-702e38eaaff0"

def get_latest_daily_report():
    """从 GitHub 获取最新的中文日报"""
    # 直接尝试获取 README.md，BuilderPulse 的日报通常在这里
    readme_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/README.md"

    try:
        # 先尝试获取 README
        response = requests.get(readme_url, timeout=30)
        if response.status_code == 200:
            content = response.text
            # 提取中文部分或今天的日报
            if "中文" in content or "日报" in content:
                return content

        # 如果 README 不行，尝试 API
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        contents = response.json()

        # 查找日报文件 (假设格式为 YYYY-MM-DD.md 或类似)
        today = datetime.now().strftime("%Y-%m-%d")

        # 尝试多种可能的文件名格式
        possible_names = [
            f"{today}.md",
            f"daily_{today}.md",
            f"report_{today}.md",
            f"{today}_zh.md",
        ]

        # 也检查 reports/ 或 daily/ 目录
        for item in contents:
            if item['type'] == 'dir' and item['name'] in ['reports', 'daily', 'dailies']:
                dir_url = item['url']
                dir_response = requests.get(dir_url, timeout=10)
                if dir_response.status_code == 200:
                    dir_contents = dir_response.json()
                    # 查找今天的日报
                    for file in dir_contents:
                        if today in file['name'] and file['name'].endswith('.md'):
                            return get_file_content(file['download_url'])

        # 在根目录查找
        for item in contents:
            if item['type'] == 'file' and item['name'] in possible_names:
                return get_file_content(item['download_url'])

        # 如果找不到今天的，获取最新的日报
        md_files = [f for f in contents if f['type'] == 'file' and f['name'].endswith('.md')]
        if md_files:
            # 按名称排序，获取最新的
            md_files.sort(key=lambda x: x['name'], reverse=True)
            return get_file_content(md_files[0]['download_url'])

        return None

    except Exception as e:
        print(f"获取日报失败: {e}")
        return None

def get_file_content(download_url):
    """下载文件内容"""
    try:
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"下载文件失败: {e}")
        return None

def send_to_feishu(content):
    """发送消息到飞书"""
    if not content:
        print("没有内容可发送")
        return False

    # 飞书消息格式
    # 限制长度，飞书单条消息有限制
    if len(content) > 3000:
        content = content[:3000] + "\n\n...(内容过长，已截断)"

    payload = {
        "msg_type": "text",
        "content": {
            "text": f"📊 BuilderPulse 日报\n\n{content}"
        }
    }

    try:
        response = requests.post(
            FEISHU_WEBHOOK,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()

        if result.get('code') == 0:
            print("✅ 发送成功")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False

    except Exception as e:
        print(f"❌ 发送到飞书失败: {e}")
        return False

def main():
    """主函数"""
    print(f"🚀 开始获取 BuilderPulse 日报 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取日报
    report = get_latest_daily_report()

    if report:
        print(f"📄 获取到日报，长度: {len(report)} 字符")
        # 发送到飞书
        send_to_feishu(report)
    else:
        print("❌ 未找到日报")
        # 发送提醒
        send_to_feishu("⚠️ 今天的日报还未生成")

if __name__ == "__main__":
    main()
