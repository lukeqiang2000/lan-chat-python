# 📝 Chat System Changelog

## Project Information
- **Project Name**: LAN Chat System
- **Current Version**: v1.4.0
- **Last Updated**: 2026-05-02
- **Status**: Stable
- **Platform Support**: Windows, macOS, Linux

---

## 🎉 Version History

### v1.4.0 (2026-05-02)

**New Features:**
- ✨ **Auto-Accept Friend Requests**
  - Added "Auto-accept" checkbox
  - Automatically accept all incoming friend requests
  - Toggle between manual/auto mode anytime
  - System notification on status change

**Improvements:**
- 🔧 Optimized friend request handling logic
- 🎨 Improved user interface layout
- 📝 Enhanced documentation

**Files Updated:**
- `chat_gui.py` - Added auto-accept functionality
- `ChatClient.exe` - Rebuilt package

---

### v1.3.0 (2026-05-01)

**New Features:**
- ✨ **GUI Friend Request Handling**
  - Auto-popup friend request dialog
  - Accept/Reject/Decide Later buttons
  - Beautiful gradient button design
  - Auto-send corresponding commands

**UI Upgrade:**
- 🎨 **Cross-Platform System Fonts**
  - Windows: Segoe UI / Microsoft YaHei
  - macOS: SF Pro Text / Helvetica Neue
  - Linux: Ubuntu / Liberation Sans
  - Auto-detect best system font

- 💬 **Modern Chat Layout**
  - Other's messages: Left side + round avatar + white bubble
  - Your messages: Right side + green bubble (WeChat style)
  - Avatar display: 40px circle with first letter
  - 18px rounded bubble design

- 🎨 **Rounded UI Design**
  - All buttons 8-12px rounded corners
  - Gradient color buttons
  - Soft shadow effects
  - Modern color scheme

**Bug Fixes:**
- ✅ Fixed GUI client crash issue
- ✅ Fixed QFontDatabase method error
- ✅ Optimized thread safety issues

**Files Updated:**
- `chat_gui.py` - UI and functionality upgrade
- `ChatClient.exe` - Rebuilt package

---

### v1.2.0 (2026-05-01)

**Network Diagnostics:**
- ✨ **Connection Test** - 3-second quick server reachability test
- ✨ **Full Diagnostic Tools** - Ping/Port Scan/Traceroute
- ✨ **One-Click Diagnostics** - Auto-run all tests

**Technical Improvements:**
- 🔧 **Async Execution** - Network tests don't block UI
- ✅ **Multi-threading** - Background thread for network operations
- ✅ **Real-time Updates** - Safe UI updates using QTimer

**New Files:**
- `open_firewall_simple.bat` - Firewall configuration
- `close_firewall_simple.bat` - Close port
- `network_diagnostics_guide.md` - Detailed documentation
- `quick_diagnostic_guide.txt` - Troubleshooting guide

---

### v1.1.0 (2026-05-01)

**Feature Completion:**
- ✨ **Friend System** - Complete add/accept/reject functionality
- ✨ **Private Chat** - One-on-one private messaging
- ✨ **Group Chat** - Multi-user group conversations
- ✨ **Message History** - View chat history
- ✨ **Online Users** - View online user list

**File Upload:**
- ✨ **File Upload Client** - `chat_client_simple.py`
- ✨ **Base64 Encoding Transfer** - Image/video/file support

**Cross-Platform Support:**
- ✨ **GitHub Actions** - Automatic Mac version building
- ✨ **Cross-Platform Fonts** - Windows/Mac/Linux universal
- ✨ **One-Click Build Scripts** - `build_windows.bat`, `build_mac.sh`

---

### v1.0.0 (2026-05-01)

**Core Features Release:**
- ✨ **User System** - Registration/Login/Authentication
- ✨ **Friend System** - Add/Accept/Reject friends
- ✨ **Chat Features** - Group chat/Private chat
- ✨ **GUI Interface** - PyQt5 graphical interface
- ✨ **Command Line Client** - English/Chinese language toggle

**File List:**
- `chat_server.py` - Server program
- `chat_gui.py` - GUI client
- `chat_client.py` - Command line client
- `test_chat.bat` - Test script

---

## 🚀 Download and Installation

### Windows Users:
1. Download `ChatClient.exe` from Releases
2. Double-click to run, no Python installation needed

### Mac Users:
1. Visit project GitHub repository
2. Run GitHub Actions to auto-build
3. Download Mac version

### Developers:
1. Clone repository
2. Install dependencies: `pip install PyQt5 pyinstaller`
3. Run: `python chat_server.py`

---

## 📊 Version Comparison

| Version | Main Features | Highlights |
|---------|---------------|------------|
| v1.4.0 | Auto-accept friends | Smart friend management |
| v1.3.0 | Modern UI | WeChat-style interface |
| v1.2.0 | Diagnostic tools | Network troubleshooting |
| v1.1.0 | Cross-platform | Mac auto-build |
| v1.0.0 | Core features | Basic chat functionality |

---

## 🔧 Utility Scripts

### Server Tools:
- `auto_restart_server.py` - Server auto-restart
- `chat_server.py` - Server program

### Build Tools:
- `auto_rebuild.py` - Auto packaging script (Python)
- `quick_build.bat` - Quick build (Windows)
- `build_windows.bat` - Windows packaging
- `build_mac.sh` - Mac packaging

### Firewall Tools:
- `open_firewall_simple.bat` - Open port 9999
- `close_firewall_simple.bat` - Close port 9999

---

## 📚 Full Documentation

### User Documentation:
- `QUICK_START.md` - Quick start guide
- `README.md` - Project overview

### Technical Documentation:
- `功能总结.txt` - Feature summary
- Server restart and build guide

### Feature Documentation:
- `好友邀请处理指南.txt` - Friend system guide
- `好友自动同意功能说明.txt` - Auto-accept feature guide
- File upload guide
- Network configuration guide
- UI upgrade guide
- File cleanup report

---

## 🎯 Main Feature List

### Core Features:
- ✅ User registration/login
- ✅ Friend system (add/accept/reject/remove)
- ✅ Group chat (broadcast messages)
- ✅ Private chat (one-on-one)
- ✅ Message history
- ✅ Online user list

### Advanced Features:
- ✅ **Auto-accept friends** (v1.4 new) ⭐
- ✅ Network diagnostic tools
- ✅ Server auto-restart
- ✅ Auto build and package
- ✅ Cross-platform support

### UI Features:
- ✅ Modern design
- ✅ Cross-platform system fonts
- ✅ Round avatar display
- ✅ WeChat-style chat bubbles
- ✅ Gradient color buttons

---

## 🐛 Fixed Issues

- ✅ GUI client crash issue
- ✅ Button click lag issue
- ✅ Thread safety issues
- ✅ QFontDatabase compatibility
- ✅ Encoding garbled text issues
- ✅ Firewall script garbled text

---

## 🎁 Usage Recommendations

### Daily Use:
1. Server: Run with auto-restart enabled
2. Client: Double-click `ChatClient.exe`
3. Check "Auto-accept" for automatic friend acceptance

### Development & Maintenance:
1. Run `quick_build.bat` after code changes
2. Or use `auto_rebuild.py` for auto packaging
3. Update distribution package

### Troubleshooting:
1. Check corresponding feature documentation
2. Use network diagnostic tools
3. Check log files

---

## 📞 Technical Support

- **Server**: chat_server.py
- **Client**: chat_gui.py (GUI), chat_client.py (Command Line)
- **File Upload**: chat_client_simple.py
- **Auto Restart**: auto_restart_server.py
- **Auto Build**: auto_rebuild.py, quick_build.bat

---

**Current Version: v1.4.0**
**Status: Stable and Available**
**Last Updated: 2026-05-02**

🎉 Thanks for using the Chat System!
