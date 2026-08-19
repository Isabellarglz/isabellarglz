from pathlib import Path
import base64


# ============================================================
# RUTAS
# ============================================================

# Carpeta raíz del proyecto
ROOT = Path(__file__).resolve().parent.parent

# Carpeta de assets
ASSETS = ROOT / "assets"

# Fuente
FONT_PATH = ASSETS / "fonts" / "JetBrainsMono-Medium.ttf"

# Imagen del stack
TECH_STACK = ASSETS / "tech-stack.png"

# SVG de salida
OUTPUT = ASSETS / "stack.svg"


# ============================================================
# CONSTANTES DE DISEÑO
# ============================================================

SVG_WIDTH = 900
SVG_HEIGHT = 120

# Dimensiones del TECH STACK
TECH_WIDTH = 900

RECT_HEIGHT = 120
RECT_Y = 0
CORNER_RADIUS = 18

# Posición del título
TITLE_Y = 25

# Dimensiones de la imagen
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 110

# Posición horizontal de la imagen
IMAGE_X = (TECH_WIDTH - IMAGE_WIDTH) / 2

# Posición vertical de la imagen
IMAGE_Y = 25


# ============================================================
# CONVERTIR IMAGEN A BASE64
# ============================================================

def image_to_base64(image_path: Path) -> str:
    """
    Convierte una imagen PNG a Base64 para
    incrustarla directamente dentro del SVG.
    """

    if not image_path.exists():
        raise FileNotFoundError(
            f"No se encontró la imagen: {image_path}"
        )

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    return encoded


# ============================================================
# CONVERTIR FUENTE A BASE64
# ============================================================

def font_to_base64(font_path: Path) -> str:
    """
    Convierte la fuente TTF a Base64 para
    incrustarla directamente dentro del SVG.
    """

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

    # --------------------------------------------------------
    # Convertir imagen y fuente a Base64
    # --------------------------------------------------------

    tech_image = image_to_base64(TECH_STACK)
    font_data = font_to_base64(FONT_PATH)


    # --------------------------------------------------------
    # Crear SVG
    # --------------------------------------------------------

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
>

    <!-- ================================================== -->
    <!-- DEFINITIONS                                        -->
    <!-- ================================================== -->

    <defs>

        <!-- ================================================== -->
        <!-- JETBRAINS MONO FONT                               -->
        <!-- ================================================== -->

        <style>
            @font-face {{
                font-family: "JetBrains Mono";
                src: url("data:font/ttf;base64,{font_data}") format("truetype");
                font-weight: 500;
                font-style: normal;
            }}
        </style>


        <!-- ================================================== -->
        <!-- TECH STACK CLIP                                   -->
        <!-- ================================================== -->

        <clipPath id="techClip">

            <rect
                x="0"
                y="{RECT_Y}"
                width="{TECH_WIDTH}"
                height="{RECT_HEIGHT}"
                rx="{CORNER_RADIUS}"
            />

        </clipPath>

    </defs>


    <!-- ================================================== -->
    <!-- TECH STACK LINES                                   -->
    <!-- ================================================== -->

    <!-- Línea superior -->

    <line
        x1="0"
        y1="{RECT_Y}"
        x2="{TECH_WIDTH}"
        y2="{RECT_Y}"
        stroke="#515151"
        stroke-width="2"
    />


    <!-- Línea inferior -->

    <line
        x1="0"
        y1="119"
        x2="{TECH_WIDTH}"
        y2="119"
        stroke="#515151"
        stroke-width="2"
    />


    <!-- ================================================== -->
    <!-- TECH STACK TITLE                                   -->
    <!-- ================================================== -->

    <text
        x="{TECH_WIDTH / 2}"
        y="{TITLE_Y}"
        text-anchor="middle"
        dominant-baseline="middle"
        fill="#FFFFFF"
        stroke="#000000"
        stroke-width="2"
        paint-order="stroke fill"
        font-family="JetBrains Mono"
        font-size="15"
        font-weight="600"
        font-style="normal"
        letter-spacing="6"
    >
        TECH STACK
    </text>


    <!-- ================================================== -->
    <!-- TECH STACK IMAGE                                   -->
    <!-- ================================================== -->

    <image
        x="{IMAGE_X}"
        y="{IMAGE_Y}"
        width="{IMAGE_WIDTH}"
        height="{IMAGE_HEIGHT}"
        preserveAspectRatio="none"
        href="data:image/png;base64,{tech_image}"
        clip-path="url(#techClip)"
    />


</svg>
'''


    # ========================================================
    # GUARDAR SVG
    # ========================================================

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )


    # ========================================================
    # MENSAJE
    # ========================================================

    print("✓ SVG generado correctamente:")
    print(f"  {OUTPUT}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_svg()