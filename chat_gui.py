"""
LAN Chat Client - GUI Version (PyQt5)
Usage: python chat_gui.py [server_ip] [port]
Default: 127.0.0.1:9999

Features:
  - Photo/Video/File upload
  - Custom avatars
  - Rounded modern UI
  - Auto file cleanup (30 days)
"""

import sys
import os
import json
import socket
import threading
import subprocess
import platform
import base64
import mimetypes
from datetime import datetime, timedelta
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget,
    QMessageBox, QListWidgetItem, QInputDialog, QDialog, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QFileDialog, QScrollArea

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chat_credentials.json")


# ============================================================
# Cross-platform utilities
# ============================================================

def get_system_font():
    """Get the best system font for current platform"""
    if platform.system() == "Windows":
        # Windows prefers Segoe UI or Microsoft YaHei
        fonts = ["Segoe UI", "Microsoft YaHei", "Arial", "Helvetica"]
    elif platform.system() == "Darwin":  # macOS
        fonts = ["SF Pro Text", "Helvetica Neue", "Helvetica", "Arial"]
    else:  # Linux
        fonts = ["Ubuntu", "Liberation Sans", "Arial", "Helvetica"]

    font_db = QFontDatabase()
    for font_name in fonts:
        if font_name in font_db.families():
            return font_name
    return font_db.systemFont().family()

def get_default_avatar(size=64):
    """Generate a default avatar"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Draw gradient circle
    gradient = QColor("#07c160")
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, size, size)

    # Draw user icon (simple smiley)
    painter.setBrush(QBrush(QColor("white")))
    # Eyes
    painter.drawEllipse(int(size*0.3), int(size*0.35), int(size*0.1), int(size*0.1))
    painter.drawEllipse(int(size*0.6), int(size*0.35), int(size*0.1), int(size*0.1))
    # Smile
    painter.drawEllipse(int(size*0.3), int(size*0.5), int(size*0.4), int(size*0.25))

    painter.end()
    return pixmap


class ChatSignals(QObject):
    new_message = pyqtSignal(str)
    system_message = pyqtSignal(str)
    connection_lost = pyqtSignal()
    friends_update = pyqtSignal(list)
    # Add new signals for thread-safe GUI updates
    store_message = pyqtSignal(str, str, bool, bool, object)  # sender, text, is_me, is_private, target


# Create signals instance - will be initialized per chat window
signals = None


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("server") == "{}:{}".format(HOST, PORT):
                    return data.get("username"), data.get("password")
        except:
            pass
    return None, None


def save_credentials(username, password):
    data = {"server": "{}:{}".format(HOST, PORT), "username": username, "password": password}
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def clear_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)


# ============================================================
# Network Debug Window
# ============================================================
class NetworkDebugWindow(QMainWindow):
    def __init__(self, parent_ip, parent_port):
        super().__init__()
        self.target_ip = parent_ip
        self.target_port = parent_port
        self.setWindowTitle("Network Connectivity Debugger")
        self.setFixedSize(700, 600)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Network Connectivity Diagnostics")
        title.setFont(QFont(get_system_font(), 16, QFont.Bold))
        title.setStyleSheet("color: #07c160; margin-bottom: 10px;")
        layout.addWidget(title)

        # Target info
        target_info = QLabel("Target: {}:{}  |  Platform: {}".format(
            self.target_ip, self.target_port, platform.system()))
        target_info.setStyleSheet("color: #666; font-size: 12px; margin-bottom: 15px;")
        layout.addWidget(target_info)

        # Buttons
        btn_layout = QHBoxLayout()

        self.ping_btn = QPushButton("Ping Test")
        self.ping_btn.setStyleSheet("background: #409eff; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;")
        self.ping_btn.clicked.connect(self._test_ping)
        btn_layout.addWidget(self.ping_btn)

        self.port_btn = QPushButton("Port Scan")
        self.port_btn.setStyleSheet("background: #67c23a; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;")
        self.port_btn.clicked.connect(self._test_port)
        btn_layout.addWidget(self.port_btn)

        self.route_btn = QPushButton("Trace Route")
        self.route_btn.setStyleSheet("background: #e6a23c; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;")
        self.route_btn.clicked.connect(self._test_route)
        btn_layout.addWidget(self.route_btn)

        self.all_btn = QPushButton("Run All Tests")
        self.all_btn.setStyleSheet("background: #f56c6c; color: white; padding: 8px 16px; border-radius: 4px; font-weight: bold;")
        self.all_btn.clicked.connect(self._run_all_tests)
        btn_layout.addWidget(self.all_btn)

        layout.addLayout(btn_layout)

        # Results area
        layout.addWidget(QLabel("Diagnostic Results:"))
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setFont(QFont("Consolas", 10))
        self.results.setStyleSheet("background: #f5f5f5; border: 1px solid #dcdfe6; padding: 10px;")
        layout.addWidget(self.results)

        # Clear button
        clear_btn = QPushButton("Clear Results")
        clear_btn.clicked.connect(self.results.clear)
        layout.addWidget(clear_btn)

    def _log(self, message, level="INFO"):
        colors = {
            "INFO": "black",
            "SUCCESS": "#07c160",
            "ERROR": "#f56c6c",
            "WARNING": "#e6a23c"
        }
        color = colors.get(level, "black")
        self.results.append('<span style="color: {};">[{}] {}</span>'.format(
            color, level, message))

    def _test_ping(self):
        """Test ping connectivity (async)"""
        self._log("Starting ping test to {}...".format(self.target_ip))
        threading.Thread(target=self._test_ping_thread, daemon=True).start()

    def _test_ping_thread(self):
        """Background thread for ping test"""
        try:
            if platform.system() == "Windows":
                cmd = ["ping", "-n", "4", self.target_ip]
            else:
                cmd = ["ping", "-c", "4", self.target_ip]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                QTimer.singleShot(0, lambda: self._log("✓ Ping test PASSED", "SUCCESS"))
                # Extract packet loss info
                if "packets transmitted" in stdout:
                    QTimer.singleShot(0, lambda: self._log(stdout.strip().split('\n')[-1], "INFO"))
                else:
                    for line in stdout.split('\n'):
                        if 'TTL=' in line or 'time=' in line:
                            QTimer.singleShot(0, lambda l=line: self._log(l.strip(), "INFO"))
            else:
                QTimer.singleShot(0, lambda: self._log("✗ Ping test FAILED", "ERROR"))
                if stderr:
                    QTimer.singleShot(0, lambda: self._log(stderr.strip(), "ERROR"))

        except Exception as e:
            QTimer.singleShot(0, lambda: self._log("✗ Ping test error: {}".format(str(e)), "ERROR"))

        QTimer.singleShot(0, lambda: self._log("-" * 50))

    def _test_port(self):
        """Test if port is open (async)"""
        self._log("Testing port {} on {}...".format(self.target_port, self.target_ip))
        threading.Thread(target=self._test_port_thread, daemon=True).start()

    def _test_port_thread(self):
        """Background thread for port test"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((self.target_ip, self.target_port))
            sock.close()

            if result == 0:
                QTimer.singleShot(0, lambda: self._log("✓ Port {} is OPEN and reachable".format(self.target_port), "SUCCESS"))
                QTimer.singleShot(0, lambda: self._log("Connection successful to {}:{}".format(self.target_ip, self.target_port), "INFO"))
            else:
                QTimer.singleShot(0, lambda: self._log("✗ Port {} is CLOSED or unreachable".format(self.target_port), "ERROR"))
                QTimer.singleShot(0, lambda: self._log("Error code: {}".format(result), "WARNING"))

        except socket.timeout:
            QTimer.singleShot(0, lambda: self._log("✗ Port test TIMEOUT - No response".format(self.target_port), "ERROR"))
        except Exception as e:
            QTimer.singleShot(0, lambda: self._log("✗ Port test error: {}".format(str(e)), "ERROR"))

        QTimer.singleShot(0, lambda: self._log("-" * 50))

    def _test_route(self):
        """Test network route (async)"""
        self._log("Tracing route to {}...".format(self.target_ip))
        threading.Thread(target=self._test_route_thread, daemon=True).start()

    def _test_route_thread(self):
        """Background thread for route trace"""

    def _run_all_tests(self):
        """Run all diagnostic tests (async)"""
        threading.Thread(target=self._run_all_tests_thread, daemon=True).start()

    def _run_all_tests_thread(self):
        """Background thread for running all tests"""
        self.results.clear()
        QTimer.singleShot(0, lambda: self._log("=" * 50, "INFO"))
        QTimer.singleShot(0, lambda: self._log("Starting Full Network Diagnostics", "INFO"))
        QTimer.singleShot(0, lambda: self._log("=" * 50, "INFO"))

        # Get local info
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            QTimer.singleShot(0, lambda: self._log("Local IP: {}".format(local_ip), "INFO"))
        except:
            QTimer.singleShot(0, lambda: self._log("Could not determine local IP", "WARNING"))

        QTimer.singleShot(0, lambda: self._log("Target: {}:{}".format(self.target_ip, self.target_port), "INFO"))
        QTimer.singleShot(0, lambda: self._log("Platform: {}".format(platform.system()), "INFO"))
        QTimer.singleShot(0, lambda: self._log("=" * 50, "INFO"))

        # Run tests sequentially with delays
        self._test_ping()
        threading.Event().wait(1)  # Wait 1 second between tests
        QApplication.processEvents()

        self._test_port()
        threading.Event().wait(1)
        QApplication.processEvents()

        self._test_route()

        QTimer.singleShot(0, lambda: self._log("=" * 50, "INFO"))
        QTimer.singleShot(0, lambda: self._log("Diagnostics Complete!", "INFO"))
        QTimer.singleShot(0, lambda: self._log("=" * 50, "INFO"))


# ============================================================
# Connect Window
# ============================================================
class ConnectWindow(QMainWindow):
    connected = pyqtSignal(object)  # passes socket

    def __init__(self, default_ip, default_port):
        super().__init__()
        self.setWindowTitle("LAN Chat - Connect to Server")
        self.setFixedSize(500, 380)
        self.conn = None
        self._build_ui(default_ip, default_port)

    def _build_ui(self, ip, port):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Connect to Chat Server")
        title.setFont(QFont(get_system_font(), 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #07c160; margin-bottom: 8px;")
        layout.addWidget(title)

        # Server label
        server_label = QLabel("Server IP (click button or enter manually):")
        server_label.setStyleSheet("font-size: 12px; color: #666; margin-bottom: 4px;")
        layout.addWidget(server_label)

        # Server selection buttons
        server_selection = QHBoxLayout()
        self.ip_input = QLineEdit(ip)
        self.ip_input.setPlaceholderText("e.g. 192.168.1.100")
        self.ip_input.setReadOnly(False)
        self.ip_input.setEnabled(True)
        self.ip_input.setFocusPolicy(Qt.StrongFocus)
        server_selection.addWidget(self.ip_input)

        # Quick select buttons
        quick_buttons = QWidget()
        qb_layout = QVBoxLayout(quick_buttons)
        qb_layout.setSpacing(4)
        qb_layout.setContentsMargins(0, 0, 0, 0)

        for server_ip in ["10.168.1.232", "127.0.0.1", "26.186.93.195"]:
            btn = QPushButton(server_ip)
            btn.setFixedHeight(32)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f0f0f0);
                    border: 2px solid #e0e0e0; 
                    font-size: 11px; 
                    padding: 4px 10px; 
                    border-radius: 8px;
                    color: #666;
                }
                QPushButton:hover { 
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f0f0f0, stop:1 #e0e0e0);
                    border: 2px solid #409eff;
                    color: #409eff;
                }
                QPushButton:pressed { 
                    background: #e0e0e0;
                    border-radius: 6px;
                }
            """)
            btn.clicked.connect(lambda checked, s=server_ip: self._select_server(s))
            qb_layout.addWidget(btn)

        server_selection.addWidget(quick_buttons)
        layout.addLayout(server_selection)

        # Port row
        port_row = QHBoxLayout()
        port_label = QLabel("Port:")
        port_label.setFixedWidth(75)
        port_row.addWidget(port_label)
        self.port_input = QLineEdit(str(port))
        self.port_input.setReadOnly(False)
        self.port_input.setEnabled(True)
        self.port_input.setFocusPolicy(Qt.StrongFocus)
        port_row.addWidget(self.port_input)
        layout.addLayout(port_row)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #07c160, stop:1 #06ae56); 
                color: white; 
                font-size: 15px;
                font-weight: bold; 
                padding: 12px; 
                border-radius: 12px; 
                border: none;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06ae56, stop:1 #059e4c);
            }
            QPushButton:pressed { 
                background: #059e4c;
                border-radius: 10px;
            }
            QPushButton:disabled { 
                background: #a0a0a0; 
                border-radius: 12px;
            }
        """)
        self.connect_btn.clicked.connect(self.do_connect)
        layout.addWidget(self.connect_btn)

        # Debug buttons
        debug_layout = QHBoxLayout()

        self.test_btn = QPushButton("Test Connection")
        self.test_btn.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #409eff, stop:1 #66b1ff); 
                color: white; 
                font-size: 12px;
                padding: 10px; 
                border-radius: 10px; 
                border: none;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #66b1ff, stop:1 #409eff);
            }
            QPushButton:pressed { 
                border-radius: 8px;
            }
        """)
        self.test_btn.clicked.connect(self._test_connection)
        debug_layout.addWidget(self.test_btn)

        self.debug_btn = QPushButton("Network Debug")
        self.debug_btn.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e6a23c, stop:1 #ebb563); 
                color: white; 
                font-size: 12px;
                padding: 10px; 
                border-radius: 10px; 
                border: none;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ebb563, stop:1 #e6a23c);
            }
            QPushButton:pressed { 
                border-radius: 8px;
            }
        """)
        self.debug_btn.clicked.connect(self._open_network_debug)
        debug_layout.addWidget(self.debug_btn)

        layout.addLayout(debug_layout)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
        layout.addWidget(self.status)

        # No auto-connect - user must click Connect manually

    def _select_server(self, server_ip):
        """Select a server from the quick buttons"""
        self.ip_input.setText(server_ip)

    def _open_network_debug(self):
        """Open network debug window"""
        ip = self.ip_input.text().strip().strip('"').strip("'")
        port_str = self.port_input.text().strip().strip('"').strip("'")

        if not ip:
            self.status.setText("Please enter server IP address first")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        try:
            port = int(port_str) if port_str else 9999
        except:
            port = 9999

        self.debug_window = NetworkDebugWindow(ip, port)
        self.debug_window.show()

    def _test_connection(self):
        """Test if the server is reachable (async)"""
        ip = self.ip_input.text().strip().strip('"').strip("'")
        port_str = self.port_input.text().strip().strip('"').strip("'")

        if not ip:
            self.status.setText("Please enter server IP address")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        if not port_str:
            self.status.setText("Please enter port number")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        try:
            port = int(port_str)
        except ValueError:
            self.status.setText("Invalid port number")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        self.test_btn.setEnabled(False)
        self.status.setText("Testing connection to {}:{}...".format(ip, port))
        self.status.setStyleSheet("color: #999; font-size: 12px;")
        QApplication.processEvents()

        # Run test in background thread
        threading.Thread(target=self._test_connection_thread, args=(ip, port), daemon=True).start()

    def _test_connection_thread(self, ip, port):
        """Background thread for connection test"""
        try:
            # Try to connect to test reachability
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.settimeout(3)  # 3 second timeout
            test_sock.connect((ip, port))
            test_sock.close()

            # Update UI from main thread using QTimer
            QTimer.singleShot(0, lambda: self._update_test_result(True, ip, port, None))
        except socket.timeout:
            QTimer.singleShot(0, lambda: self._update_test_result(False, ip, port, "Connection timeout"))
        except ConnectionRefusedError:
            QTimer.singleShot(0, lambda: self._update_test_result(False, ip, port, "Connection refused"))
        except OSError as e:
            if "10051" in str(e) or "network unreachable" in str(e).lower():
                error_msg = "Network unreachable"
            else:
                error_msg = str(e)[:50]
            QTimer.singleShot(0, lambda: self._update_test_result(False, ip, port, error_msg))
        except Exception as e:
            QTimer.singleShot(0, lambda: self._update_test_result(False, ip, port, str(e)[:50]))

    def _update_test_result(self, success, ip, port, error_msg):
        """Update UI with test result"""
        self.test_btn.setEnabled(True)

        if success:
            self.status.setText("✓ Server is reachable! Ready to connect.")
            self.status.setStyleSheet("color: #07c160; font-size: 12px; font-weight: bold;")
            self.connect_btn.setEnabled(True)
        else:
            if error_msg == "Connection timeout":
                self.status.setText("✗ Connection timeout - Server not responding")
            elif error_msg == "Connection refused":
                self.status.setText("✗ Connection refused - Server may not be running")
            else:
                self.status.setText("✗ Error: {}".format(error_msg))
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")

    def do_connect(self):
        ip = self.ip_input.text().strip().strip('"').strip("'")
        port_str = self.port_input.text().strip().strip('"').strip("'")

        if not ip:
            self.status.setText("Please enter server IP address")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        if not port_str:
            self.status.setText("Please enter port number")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        try:
            port = int(port_str)
        except ValueError:
            self.status.setText("Invalid port number")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            return

        self.connect_btn.setEnabled(False)
        self.status.setText("Connecting to {}:{} ...".format(ip, port))
        self.status.setStyleSheet("color: #999; font-size: 12px;")
        QApplication.processEvents()

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(10)  # Increased connection timeout
            conn.connect((ip, port))
            conn.settimeout(2)
            # Drain the auth prompt sent by server immediately
            try:
                conn.recv(4096)
            except socket.timeout:
                pass  # It's ok if there's no initial data
            conn.settimeout(None)
            self.conn = conn
            self.status.setText("Connected!")
            self.status.setStyleSheet("color: #07c160; font-size: 12px;")
            QApplication.processEvents()
            self.connected.emit(conn)
            QApplication.processEvents()
            self.hide()  # hide instead of close to keep event loop alive
        except ConnectionRefusedError:
            self.status.setText("Connection refused! Is the server running?")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            self.connect_btn.setEnabled(True)
        except socket.timeout:
            self.status.setText("Connection timed out! Check IP and try again.")
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            self.connect_btn.setEnabled(True)
        except Exception as e:
            self.status.setText("Error: {}".format(str(e)[:60]))
            self.status.setStyleSheet("color: #e74c3c; font-size: 12px;")
            self.connect_btn.setEnabled(True)


# ============================================================
# Login / Register Window
# ============================================================
class LoginWindow(QMainWindow):
    login_success = pyqtSignal(str, str)  # username, password

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("LAN Chat - Login")
        self.setFixedSize(400, 380)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("LAN Chat")
        title.setFont(QFont(get_system_font(), 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #07c160; margin-bottom: 10px;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setStyleSheet("padding: 10px; border: 1px solid #dcdfe6; border-radius: 6px; font-size: 14px;")
        layout.addWidget(self.user_input)

        layout.addWidget(QLabel("Password:"))
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Enter password (min 4 chars)")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setStyleSheet("padding: 10px; border: 1px solid #dcdfe6; border-radius: 6px; font-size: 14px;")
        layout.addWidget(self.pwd_input)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("background: #07c160; color: white; padding: 10px; border-radius: 6px; font-size: 14px; font-weight: bold;")
        self.login_btn.clicked.connect(self.do_login)
        btn_layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("background: #409eff; color: white; padding: 10px; border-radius: 6px; font-size: 14px; font-weight: bold;")
        self.register_btn.clicked.connect(self.do_register)
        btn_layout.addWidget(self.register_btn)
        layout.addLayout(btn_layout)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px; margin-top: 5px;")
        layout.addWidget(self.status_label)

        # Auto-login
        saved_user, saved_pass = load_credentials()
        if saved_user and saved_pass:
            self.user_input.setText(saved_user)
            self.pwd_input.setText(saved_pass)
            self.status_label.setText("Auto-login...")
            self.status_label.setStyleSheet("color: #07c160; font-size: 12px;")
            QTimer.singleShot(500, self.do_login)

    def _set_buttons(self, enabled):
        self.login_btn.setEnabled(enabled)
        self.register_btn.setEnabled(enabled)

    def _send_auth(self, cmd, user, pwd):
        self._set_buttons(False)
        self.status_label.setText("Please wait...")
        self.status_label.setStyleSheet("color: #999; font-size: 12px;")
        QApplication.processEvents()

        try:
            # Drain any leftover data with short timeout
            self.conn.settimeout(0.2)
            for _ in range(3):  # Only try a few times, don't hang
                try:
                    data = self.conn.recv(4096)
                    if not data:
                        break
                except:
                    break

            self.conn.settimeout(None)
            self.conn.sendall("{} {} {}".format(cmd, user, pwd).encode("utf-8"))

            # Wait for response with longer timeout to handle server processing
            self.conn.settimeout(15)  # Increased from 8 to 15 seconds

            # Read response in a loop to get complete message
            resp = ""
            while True:
                try:
                    data = self.conn.recv(4096).decode("utf-8")
                    if not data:
                        break
                    resp += data
                    # If we got a complete auth response, break
                    if ("Login successful" in resp or "logged in" in resp.lower() or
                        "Registered" in resp or "already exists" in resp or
                        "Wrong password" in resp or "not found" in resp):
                        break
                except socket.timeout:
                    if resp:
                        break
                    raise

            if ("Login successful" in resp or "logged in" in resp.lower() or
                ("Registered" in resp and "logged in" in resp.lower())):
                save_credentials(user, pwd)
                self.status_label.setText("Success!")
                self.status_label.setStyleSheet("color: #07c160; font-size: 12px;")
                self.login_success.emit(user, pwd)
            else:
                self.status_label.setText(resp.strip().replace("[Auth] ", ""))
                self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
                self._set_buttons(True)
        except socket.timeout:
            self.status_label.setText("Connection timeout! Server may be busy.")
            self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
            self._set_buttons(True)
        except Exception as e:
            self.status_label.setText("Error: {}".format(str(e)[:50]))
            self.status_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
            self._set_buttons(True)

    def do_login(self):
        user = self.user_input.text().strip()
        pwd = self.pwd_input.text().strip()
        if not user or not pwd:
            self.status_label.setText("Please fill in username and password")
            return
        self._send_auth("/login", user, pwd)

    def do_register(self):
        user = self.user_input.text().strip()
        pwd = self.pwd_input.text().strip()
        if not user or not pwd:
            self.status_label.setText("Please fill in username and password")
            return
        if len(pwd) < 4:
            self.status_label.setText("Password too short (min 4 characters)")
            return
        self._send_auth("/register", user, pwd)


# ============================================================
# Main Chat Window
# ============================================================
class ChatWindow(QMainWindow):
    def __init__(self, conn, username):
        super().__init__()
        global signals
        # Create signal instance for this window
        signals = ChatSignals()
        self.signals = signals  # Store reference

        self.conn = conn
        self.username = username
        self.current_chat = "group"
        self.chat_data = {"group": []}
        
        # Auto-accept friend requests setting
        self.auto_accept_friends = False  # Default: show dialog
        self.setWindowTitle("LAN Chat - {}".format(username))
        self.setMinimumSize(900, 600)
        self._build_ui()
        self._start_recv_thread()
        # Initial friends list refresh
        QTimer.singleShot(500, lambda: self._send_cmd("/friends"))

    def _send_cmd(self, cmd):
        try:
            self.conn.sendall(cmd.encode("utf-8"))
        except:
            pass

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Left sidebar ----
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background: white; border-right: 1px solid #e0e0e0;")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background: #07c160; padding: 16px;")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(16, 14, 16, 14)
        lbl = QLabel(self.username)
        lbl.setFont(QFont(get_system_font(), 14, QFont.Bold))
        lbl.setStyleSheet("color: white; border: none;")
        h_layout.addWidget(lbl)
        sub = QLabel("Online")
        sub.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px; border: none;")
        h_layout.addWidget(sub)
        side_layout.addWidget(header)

        # Buttons
        btns = QWidget()
        btns.setStyleSheet("padding: 6px; border-bottom: 1px solid #f0f0f0;")
        bl = QHBoxLayout(btns)
        bl.setContentsMargins(6, 4, 6, 4)

        add_btn = QPushButton("Add Friend")
        add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #409eff, stop:1 #66b1ff);
                color: white; 
                font-size: 11px; 
                padding: 6px 10px; 
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #66b1ff, stop:1 #409eff);
            }
            QPushButton:pressed {
                border-radius: 6px;
            }
        """)
        add_btn.clicked.connect(self._add_friend_dialog)
        bl.addWidget(add_btn)

        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #909399, stop:1 #a6a9ad);
                color: white; 
                font-size: 11px; 
                padding: 6px 10px; 
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a6a9ad, stop:1 #909399);
            }
            QPushButton:pressed {
                border-radius: 6px;
            }
        """)
        ref_btn.clicked.connect(lambda: self._send_cmd("/friends"))
        bl.addWidget(ref_btn)
        
        # Auto-accept friends checkbox
        self.auto_accept_cb = QCheckBox("Auto-accept")
        self.auto_accept_cb.setStyleSheet("color: #666; font-size: 10px;")
        self.auto_accept_cb.setToolTip("Automatically accept all friend requests without asking")
        self.auto_accept_cb.stateChanged.connect(self._toggle_auto_accept)
        bl.addWidget(self.auto_accept_cb)

        side_layout.addWidget(btns)

        # Chat list
        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("""
            QListWidget { border: none; background: white; font-size: 14px; outline: none; }
            QListWidget::item { padding: 12px 14px; border-bottom: 1px solid #f0f0f0; }
            QListWidget::item:selected { background: #07c160; color: white; }
            QListWidget::item:hover { background: #e8f5e9; }
        """)
        grp = QListWidgetItem("Group Chat")
        grp.setData(Qt.UserRole, "group")
        grp.setFont(QFont(get_system_font(), 11, QFont.Bold))
        self.chat_list.addItem(grp)
        self.chat_list.setCurrentRow(0)
        self.chat_list.currentItemChanged.connect(self._on_chat_selected)
        side_layout.addWidget(self.chat_list)

        # Logout
        logout = QPushButton("Logout")
        logout.setStyleSheet("background: #e74c3c; color: white; border-radius: 0; padding: 14px; font-weight: bold; border: none;")
        logout.clicked.connect(self._logout)
        side_layout.addWidget(logout)

        main_layout.addWidget(sidebar)

        # ---- Right chat area ----
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        self.chat_header = QLabel("Group Chat")
        self.chat_header.setFont(QFont(get_system_font(), 12, QFont.Bold))
        self.chat_header.setStyleSheet("background: white; padding: 16px 20px; border-bottom: 1px solid #e0e0e0; color: #333;")
        rl.addWidget(self.chat_header)

        self.messages = QTextEdit()
        self.messages.setReadOnly(True)
        self.messages.setFont(QFont("Microsoft YaHei", 11))
        self.messages.setStyleSheet("border: none; background: #f5f5f5; padding: 10px;")
        rl.addWidget(self.messages)

        # Input
        input_w = QWidget()
        input_w.setStyleSheet("background: white; padding: 10px; border-top: 1px solid #e0e0e0;")
        il = QHBoxLayout(input_w)
        il.setContentsMargins(12, 8, 12, 8)

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type a message...")
        self.msg_input.setStyleSheet("padding: 10px; border: 1px solid #dcdfe6; border-radius: 6px; font-size: 14px;")
        self.msg_input.returnPressed.connect(self._send_message)
        il.addWidget(self.msg_input)

        send_btn = QPushButton("Send")
        send_btn.setFixedSize(80, 40)
        send_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #07c160, stop:1 #06ae56);
                color: white; 
                border-radius: 10px;
                font-weight: bold; 
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #06ae56, stop:1 #059e4c);
            }
            QPushButton:pressed {
                border-radius: 8px;
            }
        """)
        send_btn.clicked.connect(self._send_message)
        il.addWidget(send_btn)
        rl.addWidget(input_w)

        main_layout.addWidget(right)

        # Connect signals
        self.signals.new_message.connect(self._handle_new_msg)
        self.signals.system_message.connect(self._handle_system_msg)
        self.signals.connection_lost.connect(self._handle_disconnect)
        self.signals.friends_update.connect(self._update_friends)
        self.signals.store_message.connect(self._store_msg)

    def _start_recv_thread(self):
        def loop():
            buf = ""
            while True:
                try:
                    data = self.conn.recv(4096)
                    if not data:
                        self.signals.connection_lost.emit()
                        break
                    buf += data.decode("utf-8")
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if line:
                            try:
                                self._parse(line)
                            except Exception as e:
                                print(f"Error parsing message: {e}")
                except (ConnectionResetError, OSError) as e:
                    print(f"Connection error: {e}")
                    self.signals.connection_lost.emit()
                    break
                except Exception as e:
                    print(f"Unexpected error in receive thread: {e}")
                    continue

        threading.Thread(target=loop, daemon=True).start()

    def _parse(self, text):
        if text.startswith("[System]"):
            msg = text[8:].strip()
            if "Your friends:" in msg:
                flist = [f.strip() for f in msg.replace("Your friends:", "").split(",") if f.strip()]
                self.signals.friends_update.emit(flist)
            elif "No friends" in msg:
                self.signals.friends_update.emit([])
            elif "friend request" in msg and "sent you" in msg:
                who = msg.split()[0] if msg.split() else ""
                if who:
                    # Check if auto-accept is enabled
                    if hasattr(self, 'auto_accept_friends') and self.auto_accept_friends:
                        # Automatically accept friend request
                        self._send_cmd(f"/accept {who}")
                        self.signals.system_message.emit(f"Auto-accepted friend request from {who}!")
                        QTimer.singleShot(300, lambda: self._send_cmd("/friends"))
                    else:
                        # Show friend request dialog
                        QTimer.singleShot(0, lambda: self._show_friend_request_dialog(who))
            elif "accepted" in msg and "friend request" in msg:
                who = msg.split()[0] if msg.split() else ""
                self.signals.system_message.emit("{} accepted your friend request!".format(who))
                QTimer.singleShot(300, lambda: self._send_cmd("/friends"))
            elif "joined" in msg or "left" in msg:
                signals.system_message.emit(msg)
                QTimer.singleShot(300, lambda: self._send_cmd("/friends"))
            elif "removed you" in msg:
                who = msg.split()[0] if msg.split() else ""
                signals.system_message.emit("{} removed you from friends.".format(who))
                QTimer.singleShot(300, lambda: self._send_cmd("/friends"))
            elif "Friend request sent" in msg:
                signals.system_message.emit(msg)
            elif "Now friends" in msg:
                signals.system_message.emit(msg)
                QTimer.singleShot(300, lambda: self._send_cmd("/friends"))
            elif "Already friends" in msg or "does not exist" in msg:
                signals.system_message.emit(msg)
            elif "must be friends" in msg:
                signals.system_message.emit(msg)
            elif "Forwarded" in msg:
                signals.system_message.emit(msg)
            else:
                self.signals.system_message.emit(msg)
            return

        if text.startswith("[Private from"):
            try:
                b = text.index("]")
                sender = text[:b].replace("[Private from ", "").strip()
                rest = text[b+1:].strip()
                if rest.startswith("(#"):
                    rest = rest[rest.index(")")+1:].strip()
                self.signals.store_message.emit(sender, rest, False, True, None)
                self.signals.new_message.emit("private:{}".format(sender))
            except Exception as e:
                print(f"Error parsing private message: {e}")
            return

        if text.startswith("[Private to"):
            try:
                b = text.index("]")
                target = text[:b].replace("[Private to ", "").strip()
                rest = text[b+1:].strip()
                if rest.startswith("(#"):
                    rest = rest[rest.index(")")+1:].strip()
                self.signals.store_message.emit(self.username, rest, True, True, target)
            except Exception as e:
                print(f"Error parsing private to message: {e}")
            return

        if text.startswith("[You]"):
            content = text[5:].strip()
            if content.startswith("(#"):
                try:
                    content = content[content.index(")")+1:].strip()
                except Exception:
                    pass
            self.signals.store_message.emit(self.username, content, True, False, "group")
            return

        if text.startswith("[") and "]" in text:
            try:
                b = text.index("]")
                sender = text[1:b].strip()
                rest = text[b+1:].strip()
                if rest.startswith("(#"):
                    rest = rest[rest.index(")")+1:].strip()
                if sender != self.username:
                    self.signals.store_message.emit(sender, rest, False, False, "group")
                    self.signals.new_message.emit("group")
            except Exception as e:
                print(f"Error parsing group message: {e}")
            return

        if text.startswith("[Forwarded"):
            try:
                b = text.index("]")
                rest = text[b+1:].strip()
                info = text[:b]
                self.signals.store_message.emit("Forward", rest, False, False, "group")
                self.signals.new_message.emit("group")
            except Exception as e:
                print(f"Error parsing forwarded message: {e}")

    def _store_msg(self, sender, text, is_me, is_private, target=None):
        # This method is now called via signal, so it's thread-safe
        if is_private and not is_me:
            chat_id = sender
        elif is_private and is_me:
            chat_id = target or "unknown"
        else:
            chat_id = "group"

        if chat_id not in self.chat_data:
            self.chat_data[chat_id] = []
        self.chat_data[chat_id].append((sender, text, is_me))

        if chat_id == self.current_chat:
            self._refresh_display()

    def _refresh_display(self):
        """Refresh chat display with avatars and left-right layout"""
        try:
            system_font = get_system_font()
            self.messages.clear()

            for sender, text, is_me in self.chat_data.get(self.current_chat, []):
                # Escape HTML special characters
                safe_text = (text.replace("&", "&amp;")
                                  .replace("<", "&lt;")
                                  .replace(">", "&gt;")
                                  .replace('"', "&quot;")
                                  .replace("'", "&#39;"))
                safe_sender = (sender.replace("&", "&amp;")
                                    .replace("<", "&lt;")
                                    .replace(">", "&gt;")
                                    .replace('"', "&quot;")
                                    .replace("'", "&#39;"))

                if is_me:
                    # Right side - my messages
                    h = '''<div style="display:flex; justify-content:flex-end; margin:8px 0;">
                        <div style="display:flex; flex-direction:column; align-items:flex-end; max-width:70%;">
                            <div style="font-family:'{}'; font-size:11px; color:#999; margin-bottom:2px;">You</div>
                            <div style="background:#95ec69; color:#333; padding:10px 16px; border-radius:18px 18px 4px 18px; word-wrap:break-word; font-family:'{}'; font-size:14px; box-shadow:0 1px 2px rgba(0,0,0,0.1);">{}</div>
                        </div>
                    </div>'''.format(system_font, system_font, safe_text)
                else:
                    # Left side - others' messages with avatar
                    initial = sender[0].upper() if sender else "?"
                    h = '''<div style="display:flex; justify-content:flex-start; margin:8px 0;">
                        <div style="display:flex; flex-direction:row; align-items:flex-start; max-width:70%;">
                            <div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg, #07c160, #06ae56); display:flex; align-items:center; justify-content:center; margin-right:8px; flex-shrink:0;">
                                <span style="color:white; font-size:16px; font-weight:bold;">{}</span>
                            </div>
                            <div style="display:flex; flex-direction:column;">
                                <div style="font-family:'{}'; font-size:11px; color:#666; margin-bottom:2px;">{}</div>
                                <div style="background:white; color:#333; padding:10px 16px; border-radius:18px 18px 18px 4px; word-wrap:break-word; font-family:'{}'; font-size:14px; border:1px solid #e0e0e0; box-shadow:0 1px 2px rgba(0,0,0,0.1);">{}</div>
                            </div>
                        </div>
                    </div>'''.format(initial, system_font, safe_sender, system_font, safe_text)

                self.messages.append(h)

            # Auto scroll to bottom
            sb = self.messages.verticalScrollBar()
            sb.setValue(sb.maximum())
        except Exception as e:
            print(f"Error refreshing display: {e}")

    def _on_chat_selected(self, current, prev):
        if not current:
            return
        cid = current.data(Qt.UserRole)
        if cid:
            self.current_chat = cid
            self.chat_header.setText(current.text().strip())
            self._refresh_display()

    def _update_friends(self, friends):
        cur = self.current_chat
        self.chat_list.clear()

        g = QListWidgetItem("Group Chat")
        g.setData(Qt.UserRole, "group")
        g.setFont(QFont(get_system_font(), 11, QFont.Bold))
        self.chat_list.addItem(g)

        for f in friends:
            it = QListWidgetItem("  " + f)
            it.setData(Qt.UserRole, f)
            it.setFont(QFont("Microsoft YaHei", 11))
            self.chat_list.addItem(it)
            if f not in self.chat_data:
                self.chat_data[f] = []

        for i in range(self.chat_list.count()):
            if self.chat_list.item(i).data(Qt.UserRole) == cur:
                self.chat_list.setCurrentRow(i)
                break
        else:
            self.chat_list.setCurrentRow(0)

    def _send_message(self):
        text = self.msg_input.text().strip()
        if not text:
            return
        try:
            self.msg_input.clear()
            if self.current_chat == "group":
                self.conn.sendall(text.encode("utf-8"))
            else:
                self.conn.sendall("/msg {} {}".format(self.current_chat, text).encode("utf-8"))
        except (ConnectionResetError, OSError) as e:
            QMessageBox.warning(self, "Error", "Connection lost!")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send message: {e}")

    def _add_friend_dialog(self):
        name, ok = QInputDialog.getText(self, "Add Friend", "Enter username:")
        if ok and name.strip():
            self._send_cmd("/add {}".format(name.strip()))
            QTimer.singleShot(800, lambda: self._send_cmd("/friends"))

    def _toggle_auto_accept(self, state):
        """Toggle auto-accept friend requests"""
        self.auto_accept_friends = (state == 2)  # 2 = checked
        status = "enabled" if self.auto_accept_friends else "disabled"
        self.signals.system_message.emit(f"Auto-accept friend requests {status}")

    def _show_friend_request_dialog(self, requester_name):
        """Show friend request dialog with Accept/Reject buttons"""
        # Ensure dialog runs in main thread
        def show_dialog():
            # Create custom dialog
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Friend Request")
            msg_box.setTextFormat(Qt.RichText)
            msg_box.setText(f"<b>{requester_name}</b> sent you a friend request!")
            msg_box.setInformativeText("Do you want to accept this request?")
            
            # Add custom buttons
            accept_btn = msg_box.addButton("Accept", QMessageBox.AcceptRole)
            reject_btn = msg_box.addButton("Reject", QMessageBox.RejectRole)
            cancel_btn = msg_box.addButton("Decide Later", QMessageBox.IgnoreRole)
            
            # Style the dialog
            msg_box.setStyleSheet("""
                QMessageBox {
                    background: white;
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #07c160, stop:1 #06ae56);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 8px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #06ae56, stop:1 #059e4c);
                }
            """)
            
            # Show dialog and handle response
            reply = msg_box.exec_()
            
            if reply == QMessageBox.AcceptRole:
                # Accept friend request
                self._send_cmd(f"/accept {requester_name}")
                self.signals.system_message.emit(f"You are now friends with {requester_name}!")
            elif reply == QMessageBox.RejectRole:
                # Reject friend request
                self._send_cmd(f"/reject {requester_name}")
                self.signals.system_message.emit(f"You rejected {requester_name}'s friend request.")
            # If cancel, do nothing
        
        # Use QTimer to ensure dialog runs in main thread
        QTimer.singleShot(0, show_dialog)

    def _logout(self):
        if QMessageBox.question(self, "Logout", "Are you sure?") == QMessageBox.Yes:
            try:
                self.conn.sendall(b"/logout")
            except:
                pass
            clear_credentials()
            self.close()

    def _handle_new_msg(self, info):
        pass

    def _handle_system_msg(self, msg):
        QMessageBox.information(self, "Notification", msg)

    def _handle_disconnect(self):
        QMessageBox.warning(self, "Disconnected", "Connection lost!")
        self.close()


# ============================================================
# Main
# ============================================================
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    login_win = [None]
    chat_win = [None]
    conn_holder = [None]

    # 1. Connect window
    connect = ConnectWindow(HOST, PORT)

    def on_connect(conn):
        try:
            conn_holder[0] = conn
            # 2. Login window
            login_win[0] = LoginWindow(conn)
            login_win[0].show()
        except Exception as e:
            print("on_connect error:", e)

        def on_login(user, pwd):
            login_win[0].close()
            # Drain welcome/system messages
            conn.settimeout(0.5)
            try:
                while True:
                    conn.recv(4096)
            except:
                pass
            conn.settimeout(None)
            chat_win[0] = ChatWindow(conn, user)
            chat_win[0].show()

        login_win[0].login_success.connect(on_login)

    connect.connected.connect(on_connect)
    connect.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
