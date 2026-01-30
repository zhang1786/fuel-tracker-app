from pyngrok import ngrok
import time
import os

def setup_tunnel():
    # 设置认证令牌（可选，注册ngrok后可以获得免费的）
    # ngrok.set_auth_token("YOUR_AUTH_TOKEN")

    # 创建HTTP隧道到本地8080端口
    public_url = ngrok.connect(8080, bind_tls=True)

    print(f"隧道已创建！您的应用可通过以下URL访问：")
    print(f"🌐 公共URL: {public_url}")
    print(f"🏠 本地URL: http://localhost:8080")
    print(f"\n💡 提示: 这个URL将允许任何人访问您的燃油追踪应用")
    print(f"🔒 请注意：不要在不安全的网络环境中使用此功能")
    print(f"\n按Ctrl+C停止隧道")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭隧道...")
        ngrok.disconnect(public_url)
        ngrok.kill()

if __name__ == "__main__":
    print("🔧 正在设置外网访问...")
    
    # 检查是否已安装pyngrok
    try:
        import pyngrok
    except ImportError:
        print("📦 正在安装pyngrok...")
        os.system("pip3 install pyngrok")
        import pyngrok
    
    setup_tunnel()