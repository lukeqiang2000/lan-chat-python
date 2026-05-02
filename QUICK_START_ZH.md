# 🚀 聊天系统 - 快速开始指南

## 📥 安装

### Windows 用户
1. 从 [发布页](../../releases) 下载 `ChatClient.exe`
2. 双击运行 - 无需安装 Python！

### macOS 用户
1. 从 [发布页](../../releases) 下载或手动构建
2. 见下方"从源码构建"部分

### 开发者

#### 自动安装（推荐）

**Windows:**
```cmd
install.bat
```

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

#### 手动安装
```bash
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 启动服务器

```bash
python chat_server.py
```

服务器默认在端口 **9999** 上启动。

**输出：**
```
========================================
   局域网聊天系统服务器 v1.4.0
========================================

服务器启动于 0.0.0.0:9999
等待连接...
```

---

### 启动客户端

#### GUI 客户端（推荐）
- **Windows**: 双击 `ChatClient.exe`
- **macOS/Linux**: 运行 `python chat_gui.py`

#### 命令行客户端
```bash
python chat_client_simple.py
```

**功能：**
- 现代化图形界面
- 头像显示
- 微信风格消息气泡
- 跨平台系统字体

---

## 📋 首次设置

### 步骤 1：连接服务器

1. **从下拉菜单选择服务器地址：**
   - `127.0.0.1` - 本地（用于测试）
   - `10.168.1.232` - 局域网 IP
   - `26.186.93.195` - 远程 IP

2. **点击"连接"按钮**

### 步骤 2：注册账户

1. 点击"注册"选项卡
2. 输入**用户名**和**密码**
3. 点击"注册"按钮

**示例：**
- 用户名: `alice`
- 密码: `password123`

### 步骤 3：登录

1. 输入您的用户名和密码
2. 点击"登录"按钮

**成功消息：**
```
[Auth] 登录成功！欢迎，alice！
```

---

## 💬 基本使用

### 发送消息（群聊）

只需输入消息并按 **Enter** 键。

所有在线用户都会收到您的消息。

**示例：**
```
您: 大家好！
```

### 添加好友

1. 点击"好友"选项卡
2. 在输入框中输入用户名
3. 点击"添加好友"按钮

**或使用命令：**
```bash
/add alice
```

### 接受好友请求

当有人添加您时：

**方法 1：点击弹窗**
- 将出现一个对话框
- 点击"接受"或"拒绝"

**方法 2：使用命令**
```bash
/accept alice
```

### 私聊

添加好友后：

1. 从列表中选择好友
2. 输入您的消息
3. 按 Enter 键

**或使用命令：**
```bash
/msg alice 你好 Alice！
```

---

## 🌐 网络配置

### 查找您的 IP 地址

#### Windows
```cmd
ipconfig
```
查找"IPv4 地址"（例如 192.168.1.100）

#### macOS/Linux
```bash
ifconfig | grep "inet "
```

### 配置防火墙

#### Windows（开放端口 9999）
```cmd
netsh advfirewall firewall add rule name="Chat Server" dir=in action=allow protocol=TCP localport=9999 profile=any
```

#### macOS
```bash
# 创建防火墙规则
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/bin/python3
```

---

## 📖 命令参考

### 账户命令
| 命令 | 说明 |
|------|------|
| `/register <用户> <密码>` | 注册新账户 |
| `/login <用户> <密码>` | 登录账户 |

### 好友命令
| 命令 | 说明 |
|------|------|
| `/add <用户名>` | 发送好友请求 |
| `/accept <用户名>` | 接受好友请求 |
| `/reject <用户名>` | 拒绝好友请求 |
| `/remove <用户名>` | 删除好友 |
| `/friends` | 显示好友列表 |

### 聊天命令
| 命令 | 说明 |
|------|------|
| `/msg <用户> <文本>` | 发送私聊消息 |
| `/users` | 显示在线用户 |

### 文件上传（仅 chat_client_simple.py）
| 命令 | 说明 |
|------|------|
| `/file <路径>` | 上传文件 |

---

## 🎯 常见使用场景

### 场景 1：局域网聚会聊天

**服务器（主机）：**
```bash
python chat_server.py
```

**客户端 1（Alice）：**
1. 运行 `python chat_gui.py`
2. 连接到主机的局域网 IP（如 `10.168.1.232`）
3. 注册并登录

**客户端 2（Bob）：**
1. 运行 `python chat_gui.py`
2. 连接到相同的局域网 IP
3. 注册并登录
4. 添加 Alice 为好友
5. 开始聊天！

---

### 场景 2：私人对话

**Alice:**
```bash
/add bob
```

**Bob:**
```bash
/accept alice
```

**现在双方可以：**
```bash
/msg bob 这是一条私人消息！
```

---

## 🛠️ 从源码构建

### 环境要求
```bash
pip install PyQt5 pyinstaller
```

### 构建可执行文件

#### Windows
```bash
pyinstaller --onefile --noconsole --name ChatClient chat_gui.py
```

#### macOS/Linux
```bash
pyinstaller --onefile --windowed --name ChatClient chat_gui.py
```

**输出：** `dist/ChatClient.exe` (Windows) 或 `dist/ChatClient` (macOS)

---

## 🔧 故障排除

### 问题：无法连接到服务器

**解决方案：**
1. 检查服务器是否运行：
   ```bash
   python chat_server.py
   ```

2. 验证 IP 地址正确

3. 检查防火墙设置 - 允许端口 9999

4. 尝试连接 `127.0.0.1` 进行本地测试

---

### 问题：GUI 客户端启动崩溃

**解决方案：**
1. 安装 PyQt5：
   ```bash
   pip install PyQt5
   ```

2. 检查杀毒软件是否阻止应用

3. 以管理员身份运行（Windows）

---

### 问题：好友请求不工作

**解决方案：**
1. 确保两个用户都在线
2. 检查用户名拼写
3. 使用 `/friends` 验证好友已添加

---

### 问题：文件上传失败

**解决方案：**
1. 使用 `chat_client_simple.py`（不是 `chat_gui.py`）
2. 检查文件路径正确
3. 保持文件小于 10MB

---

## 📊 系统要求

### 服务器
- **操作系统**: Windows、macOS 或 Linux
- **Python**: 3.8 或更高版本
- **内存**: 最低 512MB
- **网络**: 开放端口 9999

### 客户端
- **操作系统**: Windows 10+、macOS 10.13+ 或 Linux
- **内存**: 最低 256MB
- **磁盘**: 100MB 用于可执行文件

---

## 🎓 使用技巧

### 技巧 1：快速启动服务器
创建批处理文件（Windows）或 shell 脚本（macOS/Linux）：
```batch
@echo off
python chat_server.py
pause
```

### 技巧 2：自动接受好友
启用"自动接受"复选框可自动接受所有好友请求。

### 技巧 3：检查网络状态
使用 GUI 中的网络诊断工具测试连接。

### 技巧 4：语言切换
按 `Ctrl+L` 切换英文和中文（仅命令行客户端）。

---

## 📞 获取帮助

- **文档**: 查看 [README.md](README.md)
- **版本历史**: 查看 [CHANGELOG.md](CHANGELOG.md)
- **问题反馈**: 在 GitHub Issues 报告问题

---

## 🎉 准备好了！

现在就可以在局域网上和朋友聊天了！

**版本**: v1.4.0
**状态**: 稳定
**最后更新**: 2026-05-02

---

[⬆ 返回顶部](#-聊天系统---快速开始指南)
