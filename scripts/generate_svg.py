import json
import base64
from pathlib import Path


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).parent.parent

CONFIG_PATH = ROOT / "config" / "config.json"

OUTPUT_PATH = ROOT / "assets" / "typing.svg"

FONT_PATH = ROOT / "assets" / "fonts" / "Oswald-SemiBold.ttf"


# ============================================================
# LEER CONFIGURACIÓN
# ============================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = json.load(file)


banner = config["banner"]
name = config["name"]
headline = config["headline"]
cursor = config["cursor"]
gradient_colors = config["gradient"]


# ============================================================
# LEER E INCRUSTAR LA FUENTE OSWALD
# ============================================================

with open(FONT_PATH, "rb") as font_file:
    font_data = base64.b64encode(
        font_file.read()
    ).decode("utf-8")


# ============================================================
# GENERAR UNA FRASE ANIMADA
# ============================================================

def generate_typing_text(
    text,
    x,
    y,
    font_size,
    appear_start,
    disappear_start,
    cycle_duration
):

    typing_speed = 0.08
    deleting_speed = 0.08

    total_letters = len(text)

    letters = []

    for index, character in enumerate(text):

        if character == " ":
            character = "&#160;"

        # Momento en que aparece esta letra
        appear_time = (
            appear_start
            + index * typing_speed
        )

        # Momento en que desaparece esta letra
        disappear_time = (
            disappear_start
            + (total_letters - 1 - index)
            * deleting_speed
        )

        # Convertimos los tiempos a porcentajes
        appear_key = (
            appear_time
            / cycle_duration
        )

        disappear_key = (
            disappear_time
            / cycle_duration
        )

        letter = f'''
        <tspan opacity="0">{character}<animate
            attributeName="opacity"
            values="0;1;1;0"
            keyTimes="0;{appear_key};{disappear_key};1"
            dur="{cycle_duration}s"
            calcMode="discrete"
            repeatCount="indefinite"/>
        </tspan>'''

        letters.append(letter)

    return f'''
    <text
        x="{x}"
        y="{y}"
        font-size="{font_size}"
        font-family="Oswald"
        font-weight="600"
        fill="url(#gradient)">

        {"".join(letters)}

    </text>
    '''


# ============================================================
# GENERAR SVG
# ============================================================

def generate_svg():

    # ========================================================
    # TEXTOS
    # ========================================================

    first_text = headline["texts"][0]

    second_text = headline["texts"][1]


    # ========================================================
    # VELOCIDADES
    # ========================================================

    typing_speed = 0.08
    deleting_speed = 0.08


    # ========================================================
    # TIEMPO DE ESCRITURA DE LA PRIMERA FRASE
    # ========================================================

    first_typing_time = (
        (len(first_text) - 1)
        * typing_speed
    )


    # ========================================================
    # TIEMPO DE ESCRITURA DE LA SEGUNDA FRASE
    # ========================================================

    second_typing_time = (
        (len(second_text) - 1)
        * typing_speed
    )


    # ========================================================
    # 1 SEGUNDO ENTRE LAS DOS FRASES
    # ========================================================

    second_start = (
        first_typing_time
        + 1.0
    )


    # ========================================================
    # 2 SEGUNDOS CON LAS DOS FRASES COMPLETAS
    # ========================================================

    disappear_start = (
        second_start
        + second_typing_time
        + 4.0
    )


    # ========================================================
    # TIEMPO DE BORRADO
    # ========================================================

    first_delete_time = (
        len(first_text)
        * deleting_speed
    )

    second_delete_time = (
        len(second_text)
        * deleting_speed
    )

    delete_duration = max(
        first_delete_time,
        second_delete_time
    )


    # ========================================================
    # DURACIÓN TOTAL DEL CICLO
    # ========================================================

    cycle_duration = (
        disappear_start
        + delete_duration
    )


    # ========================================================
    # PRIMERA FRASE
    # ========================================================

    first_headline = generate_typing_text(
        first_text,
        headline["x"],
        headline["y"],
        headline["size"],
        appear_start=0,
        disappear_start=disappear_start,
        cycle_duration=cycle_duration
    )


    # ========================================================
    # SEGUNDA FRASE
    # ========================================================

    second_headline = generate_typing_text(
        second_text,
        headline["x"],
        headline["y"] + 35,
        headline["size"],
        appear_start=second_start,
        disappear_start=disappear_start,
        cycle_duration=cycle_duration
    )


    # ========================================================
    # CURSOR DE LA PRIMERA FRASE
    # ========================================================

    first_x = headline["x"]

    first_y = headline["y"]

    first_total_letters = len(first_text)


    # ========================================================
    # ANCHO DE LA PRIMERA FRASE
    # ========================================================

    first_text_width = 555


    # ========================================================
    # POSICIONES DEL CURSOR 1
    # ========================================================

    cursor_positions = []

    cursor_times = []


    for index in range(first_total_letters):

        position = (
            first_x
            + first_text_width
            * (index + 1)
            / first_total_letters
        )

        cursor_positions.append(
            str(position)
        )

        cursor_times.append(
            str(
                (index * typing_speed)
                / cycle_duration
            )
        )


    # ========================================================
    # CURSOR 1 AL FINAL
    # ========================================================

    final_cursor_position = (
        first_x
        + first_text_width
    )


    cursor_positions.append(
        str(final_cursor_position)
    )


    cursor_times.append(
        str(
            disappear_start
            / cycle_duration
        )
    )


    # ========================================================
    # CURSOR 1
    # ========================================================

    cursor_mobile = f'''
    <text
        x="{cursor_positions[0]}"
        y="{first_y}"
        font-size="{headline["size"]}"
        font-family="Oswald"
        font-weight="600"
        fill="url(#gradient)">

        |

        <animate
            attributeName="x"
            values="{";".join(cursor_positions)}"
            keyTimes="{";".join(cursor_times)}"
            dur="{cycle_duration}s"
            calcMode="discrete"
            repeatCount="indefinite"/>

        <animate
            attributeName="opacity"
            values="1;1;0;0"
            keyTimes="
                0;
                {first_typing_time / cycle_duration};
                {first_typing_time / cycle_duration};
                1
            "
            dur="{cycle_duration}s"
            calcMode="discrete"
            repeatCount="indefinite"/>

    </text>
    '''


    # ========================================================
    # CURSOR DE LA SEGUNDA FRASE
    # ========================================================

    second_x = headline["x"]

    second_y = headline["y"] + 35

    second_total_letters = len(second_text)


    # ========================================================
    # ANCHO DE LA SEGUNDA FRASE
    # ========================================================

    second_text_width = 415


    # ========================================================
    # POSICIONES DEL CURSOR
    # ========================================================

    second_cursor_positions = []

    second_cursor_times = []


    # ========================================================
    # CURSOR AL INICIO
    # ========================================================

    second_cursor_positions.append(
        str(second_x)
    )

    second_cursor_times.append(
        "0"
    )


    # ========================================================
    # AVANZAR LETRA POR LETRA
    # ========================================================

    for index in range(second_total_letters):

        position = (
            second_x
            + second_text_width
            * (index + 1)
            / second_total_letters
        )

        time = (
            second_start
            + index * typing_speed
        )

        second_cursor_positions.append(
            str(position)
        )

        second_cursor_times.append(
            str(
                time / cycle_duration
            )
        )


    # ========================================================
    # MANTENERSE AL FINAL
    # ========================================================

    second_cursor_positions.append(
        str(
            second_x + second_text_width
        )
    )

    second_cursor_times.append(
        str(
            disappear_start
            / cycle_duration
        )
    )


    # ========================================================
    # CURSOR 2
    # ========================================================

    second_cursor_mobile = f'''
    <text
        x="{second_x}"
        y="{second_y}"
        font-size="{headline["size"]}"
        font-family="Oswald"
        font-weight="600"
        fill="url(#gradient)"
        opacity="0">

        |

        <animate
            attributeName="x"
            values="{";".join(second_cursor_positions)}"
            keyTimes="{";".join(second_cursor_times)}"
            dur="{cycle_duration}s"
            calcMode="discrete"
            repeatCount="indefinite"/>

        <animate
            attributeName="opacity"
            values="0;1;1;0"
            keyTimes="
                0;
                {second_start / cycle_duration};
                {disappear_start / cycle_duration};
                1
            "
            dur="{cycle_duration}s"
            calcMode="discrete"
            repeatCount="indefinite"/>

    </text>
    '''


    # ========================================================
    # CREAR SVG
    # ========================================================

    svg = f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{banner["width"]}"
    height="{banner["height"]}"
    viewBox="0 0 {banner["width"]} {banner["height"]}">

    <defs>

        <!-- ================================================== -->
        <!-- FUENTE OSWALD SEMIBOLD -->
        <!-- ================================================== -->

        <style>
            @font-face {{
                font-family: "Oswald";
                font-style: normal;
                font-weight: 600;
                src: url("data:font/ttf;base64,{font_data}")
                     format("truetype");
            }}
        </style>


        <!-- ================================================== -->
        <!-- DEGRADADO -->
        <!-- ================================================== -->

        <linearGradient
            id="gradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="0%">

            <stop
                offset="0%"
                stop-color="{gradient_colors[0]}"/>

            <stop
                offset="50%"
                stop-color="{gradient_colors[1]}"/>

            <stop
                offset="100%"
                stop-color="{gradient_colors[2]}"/>

        </linearGradient>

    </defs>


    <!-- ================================================== -->
    <!-- NOMBRE -->
    <!-- ================================================== -->

    <text
        x="{name["x"]}"
        y="{name["y"]}"
        font-size="{name["size"]}"
        font-family="Oswald"
        font-weight="600"
        fill="url(#gradient)">

        {name["text"]}

    </text>


    <!-- ================================================== -->
    <!-- PRIMERA FRASE -->
    <!-- ================================================== -->

    {first_headline}


    <!-- ================================================== -->
    <!-- SEGUNDA FRASE -->
    <!-- ================================================== -->

    {second_headline}


    <!-- ================================================== -->
    <!-- CURSOR PRIMERA FRASE -->
    <!-- ================================================== -->

    {cursor_mobile}


    <!-- ================================================== -->
    <!-- CURSOR SEGUNDA FRASE -->
    <!-- ================================================== -->

    {second_cursor_mobile}


</svg>
'''


    # ========================================================
    # GUARDAR SVG
    # ========================================================

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(svg)


# ============================================================
# EJECUTAR
# ============================================================

generate_svg()