import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        # 处理SPA路由 - 如果请求的文件不存在，返回index.html
        if self.path != "/" and not os.path.exists(os.path.join(DIRECTORY, self.path.lstrip("/"))):
            self.path = "/"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"启动本地服务器在 http://localhost:{PORT}")
print(f"服务目录: {DIRECTORY}")
print("按Ctrl+C终止服务器")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"正在服务器上运行 http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n服务器已终止") 