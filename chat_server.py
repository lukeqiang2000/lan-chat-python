"""
LAN Chat Server
Usage: python chat_server.py [port]
Default port: 9999

Features:
  - Account registration & login (hashed passwords)
  - Friend system: add/accept/reject/remove
  - Private chat (friends only): /msg <user> <message>
  - Group chat (broadcast)
  - Forward, history, online users
"""

import socket
import threading
import sys
import json
import os
import hashlib

HOST = "10.168.1.232"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

clients = {}  # {conn: username}
lock = threading.Lock()
message_history = []
msg_id_counter = 0

# Account system
ACCOUNTS_FILE = "chat_accounts.json"
FRIENDS_FILE = "chat_friends.json"
accounts = {}         # {username: {"password_hash": str, "salt": str}}
friends_db = {}       # {username: set(of friend usernames)}
pending_requests = {} # {username: set(of requester usernames)}


def next_id():
    global msg_id_counter
    msg_id_counter += 1
    return msg_id_counter


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return h, salt


def load_data():
    global accounts, friends_db
    # Load accounts
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                accounts = json.load(f)
        except:
            accounts = {}
    # Load friends
    if os.path.exists(FRIENDS_FILE):
        try:
            with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                friends_db = {k: set(v) for k, v in data.items()}
        except:
            friends_db = {}


def save_accounts():
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)


def save_friends():
    data = {k: list(v) for k, v in friends_db.items()}
    with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def are_friends(u1, u2):
    return u2 in friends_db.get(u1, set())


def add_friend_pair(u1, u2):
    friends_db.setdefault(u1, set()).add(u2)
    friends_db.setdefault(u2, set()).add(u1)
    save_friends()


def remove_friend_pair(u1, u2):
    friends_db.get(u1, set()).discard(u2)
    friends_db.get(u2, set()).discard(u1)
    save_friends()


def get_friends(username):
    return sorted(friends_db.get(username, set()))


def get_conn(username):
    with lock:
        for c, u in clients.items():
            if u == username:
                return c
    return None


def online_users():
    with lock:
        return [u for u in clients.values() if u]


def broadcast(data, skip_conn=None):
    with lock:
        for c in list(clients.keys()):
            if c != skip_conn:
                try:
                    c.sendall(data)
                except:
                    c.close()
                    clients.pop(c, None)


def send_to(target, data):
    with lock:
        for c, u in clients.items():
            if u == target:
                try:
                    c.sendall(data)
                    return True
                except:
                    return False
    return False


def recv_line(conn):
    """Receive one line from client."""
    data = conn.recv(4096)
    if not data:
        return None
    return data.decode("utf-8").strip()


def handle_client(conn, addr):
    username = None
    try:
        # --- Authentication phase ---
        while True:
            conn.sendall(b"[Auth] Choose: /register <user> <pass>  |  /login <user> <pass>\n")
            line = recv_line(conn)
            if line is None:
                return

            if line.startswith("/register "):
                parts = line.split(None, 2)
                if len(parts) < 3:
                    conn.sendall(b"[Auth] Usage: /register <username> <password>\n")
                    continue
                user = parts[1].strip()
                pwd = parts[2].strip()
                if not user or not pwd:
                    conn.sendall(b"[Auth] Username and password cannot be empty.\n")
                    continue
                if len(pwd) < 4:
                    conn.sendall(b"[Auth] Password too short (min 4 characters).\n")
                    continue
                if user in accounts:
                    conn.sendall("[Auth] Username '{}' already exists. Try /login.\n".format(user).encode("utf-8"))
                    continue
                # Check if already logged in elsewhere
                with lock:
                    for c, u in clients.items():
                        if u == user:
                            conn.sendall("[Auth] User '{}' is already online.\n".format(user).encode("utf-8"))
                            break
                    else:
                        ph, salt = hash_password(pwd)
                        accounts[user] = {"password_hash": ph, "salt": salt}
                        save_accounts()
                        friends_db.setdefault(user, set())
                        username = user
                        with lock:
                            clients[conn] = username
                        conn.sendall("[Auth] Registered successfully! Logged in as '{}'.\n".format(user).encode("utf-8"))
                        print("[+] {} registered and joined ({})".format(user, addr))
                        break
                continue

            elif line.startswith("/login "):
                parts = line.split(None, 2)
                if len(parts) < 3:
                    conn.sendall(b"[Auth] Usage: /login <username> <password>\n")
                    continue
                user = parts[1].strip()
                pwd = parts[2].strip()
                if user not in accounts:
                    conn.sendall("[Auth] User '{}' not found. /register to create account.\n".format(user).encode("utf-8"))
                    continue
                # Check already online
                with lock:
                    for c, u in clients.items():
                        if u == user and c != conn:
                            conn.sendall("[Auth] User '{}' is already online from another session.\n".format(user).encode("utf-8"))
                            break
                    else:
                        # Not online, verify password
                        ph, _ = hash_password(pwd, accounts[user]["salt"])
                        if ph != accounts[user]["password_hash"]:
                            conn.sendall(b"[Auth] Wrong password.\n")
                            continue
                        username = user
                        clients[conn] = username
                        conn.sendall("[Auth] Login successful! Logged in as '{}'.\n".format(user).encode("utf-8"))
                        print("[+] {} logged in ({})".format(user, addr))
                        break
                continue

            else:
                conn.sendall(b"[Auth] Please register or login first.\n")
                continue

        # --- Chat phase ---
        broadcast("[System] {} joined the chat\n".format(username).encode("utf-8"), conn)

        welcome = (
            "[System] Welcome, {}!\n"
            "[System] Commands:\n"
            "  /msg <user> <text>    - private message (friends only)\n"
            "  /add <user>           - send friend request\n"
            "  /accept <user>        - accept friend request\n"
            "  /reject <user>        - reject friend request\n"
            "  /friends              - list your friends\n"
            "  /requests             - list pending requests\n"
            "  /remove <user>        - remove friend\n"
            "  /forward <id> <user>  - forward message\n"
            "  /history              - view message history\n"
            "  /users                - list online users\n"
            "  /logout               - logout and disconnect\n"
            "  Otherwise: broadcast to everyone\n"
        ).format(username)
        conn.sendall(welcome.encode("utf-8"))

        pending = pending_requests.get(username, set())
        if pending:
            conn.sendall("[System] Pending friend requests from: {}\n".format(", ".join(sorted(pending))).encode("utf-8"))

        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode("utf-8").strip()
            if not text:
                continue

            # /logout
            if text == "/logout":
                conn.sendall(b"[System] Logged out. Goodbye!\n")
                print("[-] {} logged out".format(username))
                break

            # --- Friend commands ---

            if text.startswith("/add "):
                target = text.split(None, 1)[1].strip()
                if target == username:
                    conn.sendall(b"[System] Cannot add yourself.\n")
                    continue
                if are_friends(username, target):
                    conn.sendall("[System] Already friends with {}.\n".format(target).encode("utf-8"))
                    continue
                if target not in accounts:
                    conn.sendall("[System] User '{}' does not exist.\n".format(target).encode("utf-8"))
                    continue
                pending_requests.setdefault(target, set()).add(username)
                conn.sendall("[System] Friend request sent to {}.\n".format(target).encode("utf-8"))
                tc = get_conn(target)
                if tc:
                    tc.sendall("[System] {} sent you a friend request! /accept {} or /reject {}\n".format(username, username, username).encode("utf-8"))
                continue

            if text.startswith("/accept "):
                requester = text.split(None, 1)[1].strip()
                if requester not in pending_requests.get(username, set()):
                    conn.sendall("[System] No pending request from {}.\n".format(requester).encode("utf-8"))
                    continue
                pending_requests[username].discard(requester)
                add_friend_pair(username, requester)
                conn.sendall("[System] You are now friends with {}!\n".format(requester).encode("utf-8"))
                rc = get_conn(requester)
                if rc:
                    rc.sendall("[System] {} accepted your friend request!\n".format(username).encode("utf-8"))
                continue

            if text.startswith("/reject "):
                requester = text.split(None, 1)[1].strip()
                if requester not in pending_requests.get(username, set()):
                    conn.sendall("[System] No pending request from {}.\n".format(requester).encode("utf-8"))
                    continue
                pending_requests[username].discard(requester)
                conn.sendall("[System] Rejected friend request from {}.\n".format(requester).encode("utf-8"))
                rc = get_conn(requester)
                if rc:
                    rc.sendall("[System] {} rejected your friend request.\n".format(username).encode("utf-8"))
                continue

            if text == "/friends":
                flist = get_friends(username)
                if flist:
                    conn.sendall("[System] Your friends: {}\n".format(", ".join(flist)).encode("utf-8"))
                else:
                    conn.sendall(b"[System] No friends yet. /add <user> to add!\n")
                continue

            if text == "/requests":
                pending = pending_requests.get(username, set())
                if pending:
                    conn.sendall("[System] Pending requests from: {}\n".format(", ".join(sorted(pending))).encode("utf-8"))
                else:
                    conn.sendall(b"[System] No pending friend requests.\n")
                continue

            if text.startswith("/remove "):
                target = text.split(None, 1)[1].strip()
                if are_friends(username, target):
                    remove_friend_pair(username, target)
                    conn.sendall("[System] Removed {} from friends.\n".format(target).encode("utf-8"))
                    tc = get_conn(target)
                    if tc:
                        tc.sendall("[System] {} removed you from friends.\n".format(username).encode("utf-8"))
                else:
                    conn.sendall("[System] {} is not your friend.\n".format(target).encode("utf-8"))
                continue

            # --- Chat commands ---

            if text.startswith("/msg "):
                parts = text.split(None, 2)
                if len(parts) < 3:
                    conn.sendall(b"[System] Usage: /msg <user> <message>\n")
                    continue
                target = parts[1].strip()
                body = parts[2].strip()
                if not are_friends(username, target):
                    conn.sendall("[System] You must be friends with {} first! /add {} to send request.\n".format(target, target).encode("utf-8"))
                    continue
                mid = next_id()
                with lock:
                    message_history.append({"id": mid, "sender": username, "text": body, "type": "private", "to": target})
                ok = send_to(target, "[Private from {}] (#{}) {}\n".format(username, mid, body).encode("utf-8"))
                if ok:
                    conn.sendall("[Private to {}] (#{}) {}\n".format(target, mid, body).encode("utf-8"))
                    print("  #{} [Private] {} -> {}: {}".format(mid, username, target, body))
                else:
                    conn.sendall("[System] {} is offline.\n".format(target).encode("utf-8"))
                continue

            if text.startswith("/forward "):
                parts = text.split(None, 2)
                if len(parts) < 3:
                    conn.sendall(b"[System] Usage: /forward <msg_id> <user|all>\n")
                    continue
                try:
                    fid = int(parts[1])
                    target = parts[2].strip()
                except ValueError:
                    conn.sendall(b"[System] Invalid message id.\n")
                    continue
                original = None
                for m in message_history:
                    if m["id"] == fid:
                        original = m
                        break
                if not original:
                    conn.sendall("[System] Message #{} not found.\n".format(fid).encode("utf-8"))
                    continue
                if target != "all" and not are_friends(username, target):
                    conn.sendall("[System] You must be friends with {} to forward.\n".format(target).encode("utf-8"))
                    continue
                fwd = "[Forwarded from {} (#{})] {}\n".format(original["sender"], original["id"], original["text"]).encode("utf-8")
                if target == "all":
                    broadcast(fwd, conn)
                    conn.sendall("[System] Forwarded msg #{} to everyone.\n".format(fid).encode("utf-8"))
                else:
                    ok = send_to(target, fwd)
                    if ok:
                        conn.sendall("[System] Forwarded msg #{} to {}.\n".format(fid, target).encode("utf-8"))
                    else:
                        conn.sendall("[System] User '{}' not found.\n".format(target).encode("utf-8"))
                continue

            if text == "/history":
                if not message_history:
                    conn.sendall(b"[System] No messages yet.\n")
                else:
                    lines = ["--- History ---"]
                    for m in message_history[-50:]:
                        if m["type"] == "private":
                            lines.append("  #{} [{} -> {}] {}".format(m["id"], m["sender"], m["to"], m["text"]))
                        else:
                            lines.append("  #{} [{}] {}".format(m["id"], m["sender"], m["text"]))
                    lines.append("--- End ---")
                    conn.sendall("\n".join(lines).encode("utf-8") + b"\n")
                continue

            if text == "/users":
                users = online_users()
                conn.sendall("[System] Online: {}\n".format(", ".join(users)).encode("utf-8"))
                continue

            # Normal broadcast
            mid = next_id()
            with lock:
                message_history.append({"id": mid, "sender": username, "text": text, "type": "group", "to": "all"})
            msg = "[{}] (#{}) {}\n".format(username, mid, text).encode("utf-8")
            print("  #{} {}: {}".format(mid, username, text))
            broadcast(msg, conn)
            conn.sendall("[You] (#{}) {}\n".format(mid, text).encode("utf-8"))

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        pass
    finally:
        with lock:
            uname = clients.pop(conn, username or "Unknown")
        if uname:
            print("[-] {} disconnected".format(uname))
            broadcast("[System] {} left the chat\n".format(uname).encode("utf-8"))
        conn.close()


def main():
    try:
        load_data()
    except Exception as e:
        print("[Error] Failed to load data: {}".format(e))
        print("[System] Starting with empty databases...")
        global accounts, friends_db
        accounts = {}
        friends_db = {}

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = "127.0.0.1"

        print("=" * 50)
        print("  Chat server started")
        print("  Local IP: {}".format(local_ip))
        print("  Port: {}".format(PORT))
        print("  Client cmd: python chat_client.py {} {}".format(local_ip, PORT))
        print("=" * 50)

        while True:
            try:
                conn, addr = server.accept()
                with lock:
                    clients[conn] = ""
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
            except KeyboardInterrupt:
                print("\nServer shutting down")
                break

        server.close()
    except Exception as e:
        print("[FATAL ERROR] Server crashed: {}".format(e))
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
