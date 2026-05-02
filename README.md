# 🗨️ LAN Chat System

A cross-platform local area network chat application with modern GUI, supporting Windows and macOS.

![Version](https://img.shields.io/badge/version-1.4.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Features

- 💬 **Real-time Chat** - Group chat and private messaging
- 👥 **Friend System** - Add, accept, and manage friends
- 🎨 **Modern GUI** - WeChat-style interface with avatars and bubbles
- 🌐 **LAN Communication** - Works over local network
- 📁 **File Upload** - Share images, videos, and files
- 🔐 **User Authentication** - Secure registration and login
- 🌏 **Bilingual** - Support for English and Chinese
- 🚀 **Cross-Platform** - Windows and macOS support

---

## 📥 Quick Start

### For Users

#### Windows
1. Download `dist_client/ChatClient.exe`
2. Double-click to run (no Python installation needed)

#### macOS
1. Download from GitHub Releases
2. Or build manually (see Developer section)

---

## 🚀 For Developers

### Automatic Installation (Recommended)

**Windows:**
```cmd
# Double-click to run
install.bat
```

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check if Python is installed
- ✅ Upgrade pip to the latest version
- ✅ Install PyQt5
- ✅ Install PyInstaller
- ✅ Verify installation

### Manual Installation

```bash
pip install PyQt5 pyinstaller
```

### Start Server

```bash
python chat_server.py
```

Server runs on port **9999** by default.

### Start Client

#### GUI Client (Recommended)
```bash
python chat_gui.py
```

#### File Upload Client
```bash
python chat_client_simple.py
```

---

## 📸 Screenshots

### Modern Chat Interface
- WeChat-style message bubbles
- Circular avatars
- Gradient buttons
- Cross-platform system fonts

### Key Features
- Auto-accept friend requests
- Network diagnostics tools
- Automatic server restart
- One-click build and package

---

## 🌐 Network Configuration

### Default Ports
- **Server Port**: 9999

### Server Addresses
- **Localhost**: 127.0.0.1
- **LAN**: Your local IP (e.g., 10.168.1.232)
- **Remote**: Your public IP

### Firewall Setup

#### Windows
```cmd
netsh advfirewall firewall add rule name="Chat Server" dir=in action=allow protocol=TCP localport=9999 profile=any
```

#### macOS/Linux
```bash
# Allow port 9999
sudo pfctl -e
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Chinese documentation |
| `QUICK_START.md` | Quick start guide |
| `CHANGELOG.md` | Version history |
| `功能总结.txt` | Feature summary (Chinese) |
| `好友邀请处理指南.txt` | Friend system guide (Chinese) |

---

## 🛠️ Build from Source

### Windows

```bash
# Install dependencies
pip install PyQt5 pyinstaller

# Build executable
pyinstaller --onefile --noconsole --name ChatClient chat_gui.py

# Output in dist/ChatClient.exe
```

### macOS

```bash
# Install dependencies
pip3 install PyQt5 pyinstaller

# Build app
pyinstaller --onefile --windowed --name ChatClient chat_gui.py

# Output in dist/ChatClient
```

---

## 📖 Usage Guide

### Registration & Login

1. Select server address
2. Click "Register" to create account
3. Enter username and password
4. Click "Login" to sign in

### Adding Friends

1. Use `/add <username>` to send friend request
2. Other user accepts with `/accept <username>`
3. Start private chatting with `/msg <username> <message>`

### Commands

| Command | Description |
|---------|-------------|
| `/add <user>` | Send friend request |
| `/accept <user>` | Accept friend request |
| `/reject <user>` | Reject friend request |
| `/friends` | Show friend list |
| `/msg <user> <text>` | Private message |
| `/users` | Show online users |

---

## 🎯 System Requirements

### Server
- Python 3.8+
- PyQt5
- 512MB RAM minimum

### Client
- **Windows**: Windows 10/11
- **macOS**: macOS 10.13+
- **RAM**: 256MB minimum
- **Disk**: 100MB for executable

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is for learning and personal use only.

---

## 🆘 Troubleshooting

### Cannot connect to server
- Check if server is running: `python chat_server.py`
- Verify IP address is correct
- Ensure firewall allows port 9999

### GUI crashes on startup
- Install PyQt5: `pip install PyQt5`
- Check antivirus software

### File upload fails
- Use `chat_client_simple.py`
- Check file size (< 10MB recommended)
- Verify file path is correct

---

## 📞 Support

For issues and questions:
- Check documentation in `dist_client/`
- Review `QUICK_START.md` for setup guide
- See `CHANGELOG.md` for version info

---

## 🎉 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

- **v1.4.0** - Auto-accept friend requests
- **v1.3.0** - Modern WeChat-style UI
- **v1.2.0** - Network diagnostics tools
- **v1.1.0** - Cross-platform support
- **v1.0.0** - Initial release

---

**Made with ❤️ for LAN communication**

[⬆ Back to Top](#-lan-chat-system)
