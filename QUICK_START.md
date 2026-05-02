# 🚀 Chat System - Quick Start Guide

## 📥 Installation

### For Windows Users
1. Download `ChatClient.exe` from the [Releases](../../releases) page
2. Double-click to run - no Python installation needed!

### For macOS Users
1. Download from [Releases](../../releases) or build manually
2. See "Build from Source" section below

### For Developers

#### Automatic Installation (Recommended)

**Windows:**
```cmd
install.bat
```

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

#### Manual Installation
```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Start the Server

```bash
python chat_server.py
```

The server will start on port **9999** by default.

**Output:**
```
========================================
   LAN Chat System Server v1.4.0
========================================

Server started on 0.0.0.0:9999
Waiting for connections...
```

---

### Start the Client

#### GUI Client (Recommended)
- **Windows**: Double-click `ChatClient.exe`
- **macOS/Linux**: Run `python chat_gui.py`

#### Command Line Client
```bash
python chat_client_simple.py
```

**Features:**
- Modern graphical interface
- Avatar display
- WeChat-style message bubbles
- Cross-platform system fonts

---

## 📋 First Time Setup

### Step 1: Connect to Server

1. **Select Server Address** from the dropdown:
   - `127.0.0.1` - Localhost (for testing)
   - `10.168.1.232` - LAN IP
   - `26.186.93.195` - Remote IP

2. **Click "Connect"** button

### Step 2: Register Account

1. Click "Register" tab
2. Enter your **Username** and **Password**
3. Click "Register" button

**Example:**
- Username: `alice`
- Password: `password123`

### Step 3: Login

1. Enter your username and password
2. Click "Login" button

**Success message:**
```
[Auth] Login successful! Welcome, alice!
```

---

## 💬 Basic Usage

### Send Message (Group Chat)

Simply type your message and press **Enter**.

All online users will receive your message.

**Example:**
```
You: Hello everyone!
```

### Add Friends

1. Click the "Friends" tab
2. Enter username in the input box
3. Click "Add Friend" button

**Or use command:**
```bash
/add alice
```

### Accept Friend Requests

When someone adds you:

**Method 1: Click Popup**
- A dialog will appear
- Click "Accept" or "Reject"

**Method 2: Use Command**
```bash
/accept alice
```

### Private Message

After adding friends:

1. Select friend from the list
2. Type your message
3. Press Enter

**Or use command:**
```bash
/msg alice Hello Alice!
```

---

## 🌐 Network Configuration

### Find Your IP Address

#### Windows
```cmd
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

#### macOS/Linux
```bash
ifconfig | grep "inet "
```

### Configure Firewall

#### Windows (Allow Port 9999)
```cmd
netsh advfirewall firewall add rule name="Chat Server" dir=in action=allow protocol=TCP localport=9999 profile=any
```

#### macOS
```bash
# Create firewall rule
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/bin/python3
```

---

## 📖 Command Reference

### Account Commands
| Command | Description |
|---------|-------------|
| `/register <user> <pass>` | Register new account |
| `/login <user> <pass>` | Login to account |

### Friend Commands
| Command | Description |
|---------|-------------|
| `/add <username>` | Send friend request |
| `/accept <username>` | Accept friend request |
| `/reject <username>` | Reject friend request |
| `/remove <username>` | Remove friend |
| `/friends` | Show friend list |

### Chat Commands
| Command | Description |
|---------|-------------|
| `/msg <user> <text>` | Send private message |
| `/users` | Show online users |

### File Upload (chat_client_simple.py only)
| Command | Description |
|---------|-------------|
| `/file <path>` | Upload file |

---

## 🎯 Common Use Cases

### Scenario 1: LAN Party Chat

**Server (Host):**
```bash
python chat_server.py
```

**Client 1 (Alice):**
1. Run `python chat_gui.py`
2. Connect to host's LAN IP (e.g., `10.168.1.232`)
3. Register and login

**Client 2 (Bob):**
1. Run `python chat_gui.py`
2. Connect to same LAN IP
3. Register and login
4. Add Alice as friend
5. Start chatting!

---

### Scenario 2: Private Conversation

**Alice:**
```bash
/add bob
```

**Bob:**
```bash
/accept alice
```

**Now both can:**
```bash
/msg bob This is a private message!
```

---

## 🛠️ Build from Source

### Prerequisites
```bash
pip install PyQt5 pyinstaller
```

### Build Executable

#### Windows
```bash
pyinstaller --onefile --noconsole --name ChatClient chat_gui.py
```

#### macOS/Linux
```bash
pyinstaller --onefile --windowed --name ChatClient chat_gui.py
```

**Output:** `dist/ChatClient.exe` (Windows) or `dist/ChatClient` (macOS)

---

## 🔧 Troubleshooting

### Problem: Cannot connect to server

**Solutions:**
1. Check if server is running:
   ```bash
   python chat_server.py
   ```

2. Verify IP address is correct

3. Check firewall settings - allow port 9999

4. Try connecting to `127.0.0.1` for local testing

---

### Problem: GUI client crashes on startup

**Solutions:**
1. Install PyQt5:
   ```bash
   pip install PyQt5
   ```

2. Check if antivirus is blocking the application

3. Run as administrator (Windows)

---

### Problem: Friend request not working

**Solutions:**
1. Make sure both users are online
2. Check username spelling
3. Use `/friends` to verify friend was added

---

### Problem: File upload fails

**Solutions:**
1. Use `chat_client_simple.py` (not `chat_gui.py`)
2. Check file path is correct
3. Keep files under 10MB

---

## 📊 System Requirements

### Server
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum
- **Network**: Open port 9999

### Client
- **OS**: Windows 10+, macOS 10.13+, or Linux
- **RAM**: 256MB minimum
- **Disk**: 100MB for executable

---

## 🎓 Tips and Tricks

### Tip 1: Quick Server Start
Create a batch file (Windows) or shell script (macOS/Linux):
```batch
@echo off
python chat_server.py
pause
```

### Tip 2: Auto-Accept Friends
Enable "Auto-accept" checkbox to automatically accept all friend requests.

### Tip 3: Check Network Status
Use the network diagnostic tool in GUI to test connection.

### Tip 4: Language Switch
Press `Ctrl+L` to toggle between English and Chinese (command-line client only).

---

## 📞 Getting Help

- **Documentation**: See [README.md](README.md)
- **Version History**: See [CHANGELOG.md](CHANGELOG.md)
- **Issues**: Report bugs on GitHub Issues

---

## 🎉 You're Ready!

Start chatting with your friends on LAN now!

**Version**: v1.4.0
**Status**: Stable
**Last Updated**: 2026-05-02

---

[⬆ Back to Top](#-chat-system---quick-start-guide)
