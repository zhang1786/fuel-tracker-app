tell application "Mail"
    activate
    
    set newMessage to make new outgoing message with properties {visible:true, subject:"6份党员领导干部民主生活会谈心谈话表"}
    
    tell newMessage
        set content to "您好，附件是6份党员领导干部民主生活会谈心谈话表，分别为：
谈心谈话表1-李华.xlsx
谈心谈话表2-赵敏.xlsx
谈心谈话表3-刘晓东.xlsx
谈心谈话表4-陈丽.xlsx
谈心谈话表5-马涛.xlsx
谈心谈话表6-王小军.xlsx

每份表格均已按要求完善，包含对谈话人和谈话对象的6条建议，请查收。"
        make new to recipient with properties {address:"172657125@qq.com"}
        
        -- 添加6个附件
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表1-李华.xlsx"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表2-赵敏.xlsx"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表3-刘晓东.xlsx"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表4-陈丽.xlsx"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表5-马涛.xlsx"}
        make new attachment with properties {file name:POSIX file "/Users/mrzhang/Desktop/谈心谈话表6-王小军.xlsx"}
    end tell
    
    delay 2
    send newMessage
end tell