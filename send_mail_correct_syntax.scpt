tell application "Mail"
    activate
    
    set newMessage to make new outgoing message with properties {visible:true, subject:"谈心谈话记录表"}
    
    tell newMessage
        set content to "您好，附件是谈心谈话记录表，包含6条谈话内容，请查收。"
        make new to recipient with properties {address:"172657125@qq.com"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话记录.xlsx"}
    end tell
    
    delay 2
    send newMessage
end tell