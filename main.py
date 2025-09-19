import sys
import io
import os
import json
import torch
from TTS.api import TTS

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

if hasattr(sys, "_MEIPASS"):
    base_path = sys._MEIPASS
    exe_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(base_path, "models", "xtts_v2")
tts = TTS(
    model_path=model_path,
    config_path=os.path.join(model_path, "config.json"),
    progress_bar=False
).to("cuda" if torch.cuda.is_available() else "cpu")

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


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            text = obj["text"]
            output_file = obj["output_file"]
            tts.tts_to_file(text=text, file_path=output_file, language=language, speaker=speaker)

        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
