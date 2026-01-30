import subprocess
import os

def check_outlook():
    """检查Outlook是否安装"""
    try:
        result = subprocess.run(['osascript', '-e', 'tell application "Microsoft Outlook" to version'], 
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("检测到Outlook已安装")
            return True
        else:
            print("未检测到Outlook")
            return False
    except:
        print("未检测到Outlook")
        return False

def send_via_outlook():
    """使用AppleScript通过Outlook发送邮件"""
    script = '''
    tell application "Microsoft Outlook"
        set newMessage to make new outgoing message
        tell newMessage
            set subject to "谈心谈话记录表"
            set content to "您好，附件是谈心谈话记录表，包含6条谈话内容，请查收。"
            make new recipient with properties {address:"172657125@qq.com"}
            make new attachment with properties {file:(POSIX file "/Users/mrzhang/Desktop/谈心谈话记录.xlsx")}
        end tell
        delay 1
        send newMessage
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], 
                                capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("邮件已发送")
            return True
        else:
            print(f"邮件发送失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("邮件发送操作超时")
        return False
    except Exception as e:
        print(f"邮件发送出错: {str(e)}")
        return False

if __name__ == "__main__":
    if check_outlook():
        success = send_via_outlook()
        if success:
            print("邮件发送成功！")
        else:
            print("邮件发送失败。")
    else:
        print("Microsoft Outlook 未安装或不可用。")