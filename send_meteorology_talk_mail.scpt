tell application "Mail"
    activate
    
    set newMessage to make new outgoing message with properties {visible:true, subject:"榆阳区气象局民主生活会谈心谈话记录表"}
    
    tell newMessage
        set content to "您好，附件是榆阳区气象局党员领导干部民主生活会谈心谈话记录表，包含6条谈话内容，请查收。"
        make new to recipient with properties {address:"172657125@qq.com"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/榆阳区气象局民主生活会谈心谈话记录表.xlsx"}
    end tell
    
    delay 2
    send newMessage
end tell