tell application "Mail"
    activate
    
    set newMessage to make new outgoing message with properties {visible:true, subject:"榆阳区气象局谈心谈话分析报告"}
    
    tell newMessage
        set content to "您好，附件是榆阳区气象局谈心谈话分析报告，基于实际谈心谈话内容分析，包含对谈话人和谈话对象的意见建议各6条，请查收。"
        make new to recipient with properties {address:"172657125@qq.com"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/榆阳区气象局谈心谈话分析报告.xlsx"}
    end tell
    
    delay 2
    send newMessage
end tell