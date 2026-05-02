"""
简单的带文件上传的聊天客户端演示
Usage: python chat_client_with_file.py [server_ip] [port]
"""

import socket
import sys
import os
import base64
import mimetypes
from pathlib import Path

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

def send_file(conn, filepath):
    """Send file to server"""
    try:
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        
        # 读取文件并转换为base64
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # 获取文件类型
        filetype, _ = mimetypes.guess_type(filepath)
        if not filetype:
            filetype = 'application/octet-stream'
        
        # 检查文件大小（限制10MB）
        if filesize > 10 * 1024 * 1024:
            print(f"Error: File too large (max 10MB)")
            return False
        
        # 转换为base64
        file_b64 = base64.b64encode(file_data).decode('utf-8')
        
        # 发送文件上传命令
        message = f"FILE {filename} {filesize} {filetype} {file_b64}"
        conn.sendall(message.encode('utf-8'))
        
        print(f"File sent: {filename} ({filesize} bytes)")
        return True
        
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

def main():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        # 接收初始消息
        data = conn.recv(4096).decode('utf-8')
        print(data)
        
        while True:
            cmd = input("> ")
            
            # 处理文件上传命令
            if cmd.startswith("/file "):
                filepath = cmd.split(" ", 1)[1].strip()
                if os.path.exists(filepath):
                    send_file(conn, filepath)
                else:
                    print(f"File not found: {filepath}")
                continue
            
            if not cmd.strip():
                continue
            
            conn.sendall(cmd.encode('utf-8'))
            
            # 接收响应
            try:
                data = conn.recv(4096)
                if not data:
                    break
                print(data.decode('utf-8'), end="")
            except socket.timeout:
                pass
            
    except ConnectionRefusedError:
        print("Cannot connect to server")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Simple Chat Client with File Upload")
    print("Commands:")
    print("  /file <filepath>  - Upload file")
    print("  /msg <user> <text> - Private message")
    print("  /logout           - Logout")
    print()
    main()
