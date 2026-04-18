#!/usr/bin/env python3
"""
Viewer v2 런처 — 서버가 준비된 뒤에 브라우저를 엽니다.
포트 충돌/ 브라우저 캐시 문제 없이 안정적으로 실행.
"""
import http.server
import os
import socket
import socketserver
import sys
import threading
import time
import webbrowser

PORT = 8765
HTML = "study_viewer_v2.html"

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def find_free_port(start):
    """시작 포트부터 사용 가능한 포트 찾기."""
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start


def open_browser_later(port, delay=0.8):
    """서버가 리슨하기 시작한 걸 확인한 후 브라우저 오픈."""
    time.sleep(0.1)
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                break
        except OSError:
            time.sleep(0.2)
    time.sleep(delay)
    url = f"http://localhost:{port}/{HTML}"
    print(f"▶ Opening: {url}")
    webbrowser.open(url)


def main():
    port = find_free_port(PORT)
    url = f"http://localhost:{port}/{HTML}"

    print("=" * 50)
    print("  IDM Viewer v2")
    print(f"  URL: {url}")
    print(f"  (change port: edit PORT in launch_viewer.py)")
    print("  Press Ctrl+C to stop.")
    print("=" * 50)

    # 브라우저를 백그라운드에서 열기 (서버가 준비된 뒤)
    threading.Thread(target=open_browser_later, args=(port,), daemon=True).start()

    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
