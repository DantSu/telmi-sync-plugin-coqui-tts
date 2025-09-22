import socket
import json
import os
import sys
import time
import threading
import torch
import signal
from TTS.api import TTS

HOST = "127.0.0.1"
PORT = 8765
TIMEOUT = 600

last_activity = time.time()

if hasattr(sys, "_MEIPASS"):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_path, "models", "xtts_v2")
tts = TTS(
    model_path=model_path,
    config_path=os.path.join(model_path, "config.json"),
    progress_bar=False
).to("cuda" if torch.cuda.is_available() else "cpu")


def watchdog():
    global last_activity
    while True:
        time.sleep(30)
        if time.time() - last_activity > TIMEOUT:
            os.kill(os.getpid(), signal.SIGTERM)


threading.Thread(target=watchdog, daemon=True).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Serveur TTS en écoute sur {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(65536).decode("utf-8")
            if not data:
                continue
            try:
                obj = json.loads(data)
                tts.tts_to_file(text=obj["text"],
                                file_path=obj["output_file"],
                                speaker=obj["speaker"],
                                language=obj["language"])
                conn.sendall(b"Coqui TTS : Files created")

            except Exception as e:
                conn.sendall(f"ERROR: {e}".encode("utf-8"))

            last_activity = time.time()
