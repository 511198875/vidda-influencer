-- WeChat Monitor: 截图所有监控群聊
-- 使用方法: 双击此脚本运行

property screenshotFolder : ((path to home folder as text) & "WorkBuddy:Claw:wechat-monitor:screenshots:")

-- 要监控的群聊列表
property groupList : {"【Vidda-MGCC】众引沟通群", "【Vidda电视&星榜执行】", "【Vidda投影&星榜】B站执行", "【智元】Vidda小红书KOC26年执行"}

-- 截图保存函数
on saveScreenshot(fileName)
    set fullPath to screenshotFolder & fileName
    do shell script "screencapture -x " & quoted form of POSIX path of fullPath
    return fullPath as text
end saveScreenshot

-- 主流程
tell application "WeChat"
    activate
end tell

delay 0.5

-- 关闭可能的弹窗
tell application "System Events"
    key code 53
end tell
delay 0.2

-- 遍历每个群
repeat with i from 1 to (length of groupList)
    set groupName to item i of groupList
    
    display notification "正在处理: " & groupName with title "微信监控"
    
    -- 打开搜索
    tell application "System Events"
        keystroke "f" using {command down}
    end tell
    delay 0.3
    
    -- 输入群名
    tell application "System Events"
        keystroke groupName
    end tell
    delay 1.0
    
    -- 按回车
    tell application "System Events"
        key code 36
    end tell
    delay 0.5
    
    -- 关闭搜索弹窗
    tell application "System Events"
        key code 53
    end tell
    delay 0.3
    
    -- 截图
    set timestamp to do shell script "date +%H%M%S"
    set fileName to ((i as text) & "_" & timestamp & ".png")
    saveScreenshot(fileName)
    
    delay 0.5
    
    display notification "已保存截图: " & fileName with title "微信监控"
    
end repeat

display notification "所有群聊截图完成！" with title "微信监控"

-- 关闭搜索状态
tell application "System Events"
    key code 53
end tell

display dialog "截图完成！" buttons {"确定"} default button 1
