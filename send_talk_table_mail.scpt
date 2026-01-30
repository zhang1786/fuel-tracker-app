tell application "Mail"
    activate
    
    set newMessage to make new outgoing message with properties {visible:true, subject:"完善版党员领导干部民主生活会谈心谈话表"}
    
    tell newMessage
        set content to "您好，附件是完善版党员领导干部民主生活会谈心谈话表，已为每个人添加了6条建议，请查收。"
        make new to recipient with properties {address:"172657125@qq.com"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/完善版党员领导干部民主生活会谈心谈话表.xlsx"}
    end tell
    
    delay 2
    send newMessage
end tell