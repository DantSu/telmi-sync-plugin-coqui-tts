import sys
import io
import socket
import json
import subprocess
import time
import os

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

HOST = "127.0.0.1"
PORT = 8765

if hasattr(sys, "_MEIPASS"):
    exe_path = os.path.dirname(sys.executable)
else:
    exe_path = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(exe_path, "tts-config.txt")
speaker = "Ana Florence"
language = "fr"

if os.path.exists(config_file):
    with open(config_file, encoding="utf-8") as f:
        for config_line in f:
            config_line = config_line.strip()
            if config_line.startswith("#") or "=" not in config_line:
                continue
            key, value = config_line.split("=", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "speaker":
                speaker = value
            elif key == "language":
                language = value


def is_server_running():
    try:
        with socket.create_connection((HOST, PORT), timeout=1):
            return True
    except (ConnectionRefusedError, socket.timeout):
        return False


def start_server():
    if hasattr(sys, "_MEIPASS"):
        exe_dir = os.path.dirname(sys.executable)
        server_path = os.path.join(exe_dir, "coquiserver.exe")
        subprocess.Popen([server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(script_dir, "coquiserver.py")
        subprocess.Popen([sys.executable, server_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for _ in range(40):
        if is_server_running():
            return True
        time.sleep(0.5)
    return False


def main():
    if not is_server_running():
        print("Serveur not started, launching...")
        if not start_server():
            print("Unable to launch the server.", file=sys.stderr)
            sys.exit(1)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            obj.update({
                "speaker": speaker,
                "language": language
            })
            with socket.create_connection((HOST, PORT)) as sock:
                sock.sendall(json.dumps(obj).encode("utf-8"))
                resp = sock.recv(1024).decode("utf-8")
                print(resp)
        except Exception as e:
            print(f"Erreur côté client: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
