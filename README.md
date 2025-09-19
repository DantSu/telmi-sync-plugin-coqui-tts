# Coqui TTS plugin for Telmi Sync

## Install

```shell
conda create -n coqui python=3.10 -y
conda activate coqui
pip install torch==2.2.2+cu118 torchaudio==2.2.2+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install TTS==0.22.0
pip install transformers==4.39.3
pip install pyinstaller
```

## Compile

```shell
pyinstaller --onefile --collect-all TTS --collect-all trainer --collect-all inflect --collect-all gruut --collect-all jamo --hidden-import numba --add-data "models/xtts_v2;models/xtts_v2" main.py
```
## Config

```file:config.txt
speaker=Ana Florence
language=fr
```

## How exe file works ?

With multiple JSON separated by new line (\n) in STDIN.

```json
{"text": "C'est une très belle journée pour Zény la fée magique des océans.", "output_file": ".\\test.wav"}
{"text": "Deuxième phrase, plutôt essayer de mettre d'autres accents comme celui là.", "output_file": ".\\test2.wav"}
```

## List of speakers

- Aaron Dreschner
- Abrahan Mack
- Adde Michal
- Alexandra Hisakawa
- Alison Dietlinde
- Alma María
- Ana Florence
- Andrew Chipper
- Annmarie Nele
- Asya Anara
- Badr Odhiambo
- Baldur Sanjin +
- Barbora MacLean
- Brenda Stern
- Camilla Holmström
- Chandra MacFarland
- Claribel Dervla
- Craig Gutsy
- Daisy Studious 
- Damian Black +
- Damjan Chapman
- Dionisio Schuyler
- Eugenio Mataracı
- Ferran Simen
- Filip Traverse
- Gilberto Mathias
- Gitta Nikolina
- Gracie Wise
- Henriette Usha
- Ige Behringer
- Ilkin Urbano
- Kazuhiko Atallah
- Kumar Dahl
- Lidiya Szekeres
- Lilya Stainthorpe
- Ludvig Milivoj
- Luis Moray
- Maja Ruoho
- Marcos Rudaski
- Narelle Moon
- Nova Hogarth
- Royston Min
- Rosemary Okafor
- Sofia Hellen
- Suad Qasim
- Szofi Granger
- Tammie Ema
- Tammy Grit
- Tanja Adelina
- Torcull Diarmuid
- Uta Obando
- Viktor Eka
- Viktor Menelaos
- Vjollca Johnnie
- Wulf Carlevaro +
- Xavier Hayasaka
- Zacharie Aimilios
- Zofija Kendrick

Listen voice here : https://www.youtube.com/watch?v=5lpHq68Yd38