#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信群消息监控系统
监控 Vidda 相关群聊，每天汇总发给草草
"""

import subprocess
import time
import os
import json
from datetime import datetime

# 监控的群列表
GROUPS = [
    "【Vidda-MGCC】众引沟通群",
    "【Vidda电视&星榜执行】",
    "【Vidda投影&星榜】B站执行",
    "【智元】Vidda小红书KOC26年执行",
]

# 截图保存目录
SCREENSHOT_DIR = "/Users/caocao/WorkBuddy/Claw/wechat-monitor/screenshots"

def screenshot(filename):
    """截取屏幕并保存"""
    path = os.path.join(SCREENSHOT_DIR, filename)
    result = subprocess.run(
        ["screencapture", "-x", "-R", "0,0,2560,1664", path],
        capture_output=True, text=True
    )
    return path

def activate_wechat():
    subprocess.run(["osascript", "-e", 'tell application "WeChat" to activate'])
    time.sleep(0.5)

def search_and_open_group(group_name):
    """搜索并打开群聊"""
    # 打开搜索
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            keystroke "f" using {command down}
        end tell
    '''])
    time.sleep(0.3)
    
    # 输入群名
    subprocess.run(["osascript", "-e", f'''
        tell application "System Events"
            keystroke "{group_name}"
        end tell
    '''])
    time.sleep(1.0)
    
    # 按回车打开
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            key code 36
        end tell
    '''])
    time.sleep(0.5)

def capture_chat_area():
    """截取聊天区域"""
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"chat_{timestamp}.png"
    return screenshot(filename)

def escape_press():
    """按 ESC 关闭弹窗"""
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            key code 53
        end tell
    '''])
    time.sleep(0.2)

def click_input_and_send(message):
    """点击输入框并发送消息"""
    # 先按 ESC 关闭可能的弹窗
    escape_press()
    
    # 点击输入框位置 (需要根据实际情况调整)
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            click at {300, 900}
        end tell
    '''])
    time.sleep(0.3)
    
    # 输入消息
    subprocess.run(["osascript", "-e", f'''
        tell application "System Events"
            keystroke "{message}"
        end tell
    '''])
    time.sleep(0.2)
    
    # 发送
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            key code 36
        end tell
    '''])
    time.sleep(0.5)

def send_to_caocao(summary):
    """发送给草草"""
    # 搜索草草
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            keystroke "f" using {command down}
        end tell
    '''])
    time.sleep(0.3)
    
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            keystroke "草草"
        end tell
    '''])
    time.sleep(1.0)
    
    # 选择第一个结果
    subprocess.run(["osascript", "-e", '''
        tell application "System Events"
            key code 36
        end tell
    '''])
    time.sleep(0.5)
    
    # 发送摘要
    click_input_and_send(summary)

def main():
    """主流程"""
    print("=" * 50)
    print("微信群消息监控系统启动")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"监控群数: {len(GROUPS)}")
    print("=" * 50)
    
    # 激活微信
    activate_wechat()
    
    summaries = []
    
    for group in GROUPS:
        print(f"\n正在处理: {group}")
        
        # 搜索并打开群
        search_and_open_group(group)
        time.sleep(0.5)
        
        # 滚到顶部加载历史消息
        escape_press()
        time.sleep(0.2)
        
        # 截图聊天区域
        img_path = capture_chat_area()
        print(f"  截图: {img_path}")
        
        # 向上滚动加载更多消息
        for _ in range(5):
            subprocess.run(["osascript", "-e", '''
                tell application "System Events"
                    key code 126 using {command down}
                end tell
            '''])
            time.sleep(0.2)
        
        time.sleep(0.5)
        
        # 再次截图（获取更多历史消息）
        img_path2 = capture_chat_area()
        print(f"  历史截图: {img_path2}")
        
        summaries.append({
            "group": group,
            "screenshots": [img_path, img_path2]
        })
        
        # 关闭搜索继续下一个
        escape_press()
        time.sleep(0.3)
    
    print("\n" + "=" * 50)
    print("截图完成，准备发送汇总")
    print("=" * 50)
    
    # 生成汇总消息
    summary = f"""📊 Vidda 群消息汇总
{datetime.now().strftime('%Y-%m-%d')}

已监控 {len(GROUPS)} 个群聊：
"""
    for i, s in enumerate(summaries, 1):
        summary += f"\n{i}. {s['group']}\n"
    
    summary += "\n\n📎 截图已保存，请查看详细消息"
    
    # 发送给草草
    # send_to_caocao(summary)
    
    print("汇总内容:")
    print(summary)
    print("\n截图文件:")
    for s in summaries:
        for img in s['screenshots']:
            print(f"  - {img}")
    
    print("\n✅ 处理完成!")

if __name__ == "__main__":
    main()
