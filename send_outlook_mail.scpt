tell application "Microsoft Outlook"
    activate
    
    set newMessage to make new outgoing message with properties {subject:"谈心谈话记录表", content:"您好，附件是谈心谈话记录表，包含6条谈话内容，请查收。"}
    
    make new recipient at newMessage with properties {address:"172657125@qq.com"}
    
    -- 添加附件
    make new attachment at newMessage with properties {file:(POSIX file ("/Users/mrzhang/Desktop/谈心谈话记录.xlsx"))}
    
    -- 发送邮件
    send newMessage
end tell