from pathlib import Path
import base64


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

ASSETS = ROOT / "assets"

FONT_PATH = ASSETS / "fonts" / "JetBrainsMono-Medium.ttf"

OUTPUT = ASSETS / "connect.svg"


# ============================================================
# CONFIGURACIÓN
# ============================================================

SVG_WIDTH = 900
SVG_HEIGHT = 50

FONT_SIZE = 20
FONT_WEIGHT = 500


# ============================================================
# FUENTE A BASE64
# ============================================================

def font_to_base64(font_path: Path) -> str:

    if not font_path.exists():
        raise FileNotFoundError(
            f"No se encontró la fuente: {font_path}"
        )

    encoded = base64.b64encode(
        font_path.read_bytes()
    ).decode("utf-8")

    return encoded


# ============================================================
# GENERAR SVG
# ============================================================

def generate_svg():

    font_data = font_to_base64(FONT_PATH)

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

    <defs>

        <style>
            @font-face {{
                font-family: "JetBrains Mono";
                src: url("data:font/ttf;base64,{font_data}") format("truetype");
                font-weight: {FONT_WEIGHT};
                font-style: normal;
            }}
        </style>

    </defs>


    <text
        x="{SVG_WIDTH / 2}"
        y="{SVG_HEIGHT / 2}"
        text-anchor="middle"
        dominant-baseline="middle"
        fill="#FFFFFF"
        stroke="#000000"
        stroke-width="2"
        paint-order="stroke fill"
        font-family="JetBrains Mono"
        font-size="{FONT_SIZE}"
        font-weight="{FONT_WEIGHT}"
        font-style="normal"
        letter-spacing="1"
    >
        🌐 CONECTA CONMIGO
    </text>


</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print("✓ Connect SVG generado correctamente:")
    print(f"  {OUTPUT}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_svg()
    