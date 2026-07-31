import json
from pathlib import Path


# Ruta hasta la carpeta raíz del proyecto
ROOT = Path(__file__).parent.parent

# Ruta al archivo de configuración
CONFIG_PATH = ROOT / "config" / "config.json"

# Abre el archivo
with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = json.load(file)

print(config)
