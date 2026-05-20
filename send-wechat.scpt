-- WeChat Group Message Sender
-- 使用方法: 打开微信，按 Cmd+Q 退出后，双击此脚本运行

property targetGroup : "妈妈和他的好女儿群"
property messageText : "嘿嘿"

on run
    tell application "WeChat"
        activate
    end tell
    
    delay 0.5
    
    tell application "System Events"
        -- Open search with Cmd+F
        keystroke "f" using {command down}
    end tell
    
    delay 0.3
    
    tell application "System Events"
        -- Type group name
        keystroke targetGroup
    end tell
    
    delay 0.8
    
    tell application "System Events"
        -- Press Enter to search
        keystroke return
    end tell
    
    delay 0.3
    
    tell application "System Events"
        -- Press Enter to open chat
        keystroke return
    end tell
    
    delay 0.5
    
    tell application "System Events"
        -- Type message
        keystroke messageText
    end tell
    
    delay 0.3
    
    tell application "System Events"
        -- Send with Enter
        keystroke return
    end tell
    
    display notification "消息已发送: " & messageText & " → " & targetGroup with title "微信自动发送"
    
end run
