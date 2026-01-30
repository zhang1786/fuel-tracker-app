tell application "Microsoft Outlook"
    set newMessage to make new outgoing message
    tell newMessage
        set subject to "谈心谈话记录表"
        set content to "您好，附件是谈心谈话记录表，包含6条谈话内容，请查收。"
        make new recipient with properties {address:"172657125@qq.com"}
        make new attachment with properties {file:(POSIX file ("/Users/mrzhang/Desktop/谈心谈话记录.xlsx"))}
    end tell
    delay 2
    send newMessage
end tell