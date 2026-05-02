# 🗨️ 局域网聊天系统

一个跨平台局域网聊天应用，支持 Windows 和 macOS，拥有现代化图形界面。

![Version](https://img.shields.io/badge/版本-1.4.0-blue)
![Platform](https://img.shields.io/badge/平台-Windows%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/许可证-MIT-orange)

---

## ✨ 功能特性

- 💬 **实时聊天** - 群聊和私聊
- 👥 **好友系统** - 添加、接受和管理好友
- 🎨 **现代界面** - 微信风格界面，支持头像和气泡
- 🌐 **局域网通信** - 通过本地网络通信
- 📁 **文件上传** - 分享图片、视频和文件
- 🔐 **用户认证** - 安全的注册和登录
- 🌏 **双语支持** - 支持英文和中文
- 🚀 **跨平台** - Windows 和 macOS 支持

---

## 📥 快速开始

### 普通用户

#### Windows
1. 下载 `ChatClient.exe`
2. 双击运行（无需安装Python）

#### macOS
1. 从 GitHub Releases 下载
2. 或手动构建（见开发者部分）

---

## 🚀 开发者

### 自动安装（推荐）

**Windows:**
```cmd
# 双击运行
install.bat
```

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

安装程序会自动：
- ✅ 检查 Python 是否安装
- ✅ 升级 pip 到最新版本
- ✅ 安装 PyQt5
- ✅ 安装 PyInstaller
- ✅ 验证安装成功

### 手动安装

```bash
pip install PyQt5 pyinstaller
```

### 启动服务器

```bash
python chat_server.py
```

服务器默认运行在端口 **9999**。

### 启动客户端

#### GUI客户端（推荐）
```bash
python chat_gui.py
```

#### 文件上传客户端
```bash
python chat_client_simple.py
```

---

## 📸 界面预览

### 现代聊天界面
- 微信风格消息气泡
- 圆形头像
- 渐变按钮
- 跨平台系统字体

### 核心功能
- 自动接受好友请求
- 网络诊断工具
- 服务器自动重启
- 一键构建打包

---

## 🌐 网络配置

### 默认端口
- **服务器端口**: 9999

### 服务器地址
- **本地**: 127.0.0.1
- **局域网**: 本地IP（如 10.168.1.232）
- **远程**: 公网IP

### 防火墙设置

#### Windows
```cmd
netsh advfirewall firewall add rule name="Chat Server" dir=in action=allow protocol=TCP localport=9999 profile=any
```

#### macOS/Linux
```bash
# 开放端口 9999
sudo pfctl -e
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| `README.md` | 英文文档 |
| `QUICK_START.md` | 快速开始指南 |
| `CHANGELOG.md` | 版本历史 |

---

## 🛠️ 从源码构建

### Windows

```bash
# 安装依赖
pip install PyQt5 pyinstaller

# 构建可执行文件
pyinstaller --onefile --noconsole --name ChatClient chat_gui.py

# 输出在 dist/ChatClient.exe
```

### macOS

```bash
# 安装依赖
pip3 install PyQt5 pyinstaller

# 构建应用
pyinstaller --onefile --windowed --name ChatClient chat_gui.py

# 输出在 dist/ChatClient
```

---

## 📖 使用指南

### 注册与登录

1. 选择服务器地址
2. 点击"注册"创建账户
3. 输入用户名和密码
4. 点击"登录"进入

### 添加好友

1. 使用 `/add <用户名>` 发送好友请求
2. 对方使用 `/accept <用户名>` 接受
3. 使用 `/msg <用户名> <消息>` 开始私聊

### 命令列表

| 命令 | 说明 |
|------|------|
| `/add <用户>` | 发送好友请求 |
| `/accept <用户>` | 接受好友请求 |
| `/reject <用户>` | 拒绝好友请求 |
| `/friends` | 显示好友列表 |
| `/msg <用户> <文本>` | 私聊消息 |
| `/users` | 显示在线用户 |

---

## 🎯 系统要求

### 服务器
- Python 3.8+
- PyQt5
- 最低 512MB 内存

### 客户端
- **Windows**: Windows 10/11
- **macOS**: macOS 10.13+
- **内存**: 最低 256MB
- **磁盘**: 100MB 用于可执行文件

---

## 🤝 贡献

欢迎贡献！您可以：

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 提交 Pull Request

---

## 📄 许可证

本项目仅供学习和个人使用。

---

## 🆘 故障排除

### 无法连接服务器
- 检查服务器是否运行: `python chat_server.py`
- 验证 IP 地址是否正确
- 确保防火墙允许端口 9999

### GUI 启动崩溃
- 安装 PyQt5: `pip install PyQt5`
- 检查杀毒软件设置

### 文件上传失败
- 使用 `chat_client_simple.py`
- 检查文件大小（建议 < 10MB）
- 验证文件路径正确

---

## 📞 技术支持

如有问题和疑问：
- 查看 `dist_client/` 中的文档
- 阅读 `QUICK_START.md` 设置指南
- 查看 `CHANGELOG.md` 版本信息

---

## 🎉 版本历史

详见 [CHANGELOG.md](CHANGELOG.md)。

- **v1.4.0** - 自动接受好友请求
- **v1.3.0** - 现代微信风格界面
- **v1.2.0** - 网络诊断工具
- **v1.1.0** - 跨平台支持
- **v1.0.0** - 初始发布

---

**用 ❤️ 为局域网通信打造**

[⬆ 返回顶部](#-局域网聊天系统)
