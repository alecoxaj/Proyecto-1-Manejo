import json
import os
import shutil


ARCHIVO_CONFIG = "config.json"
ARCHIVO_TEMPORAL = "config.tmp"
ARCHIVO_RESPALDO = "config.bak"


CONFIGURACION_PREDETERMINADA = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "Claro",
    "idioma": "es-ES",
    "tamano_fuente": 14,
    "color_barra_menu": "#f0f0f0",
    "color_letra": "#000000",
    "color_letra_personalizado": False,
    "foto_perfil": ""
}


def validar_color(color):
    if not isinstance(color, str):
        return False

    if len(color) != 7:
        return False

    if not color.startswith("#"):
        return False

    try:
        int(color[1:], 16)
        return True

    except ValueError:
        return False


def validar_configuracion(configuracion):
    if not isinstance(configuracion, dict):
        raise ValueError(
            "La configuración debe ser un objeto."
        )

    if not isinstance(
        configuracion["nombre_usuario"],
        str
    ):
        raise ValueError(
            "El nombre de usuario es inválido."
        )

    if configuracion["tema_interfaz"] not in (
        "Claro",
        "Oscuro"
    ):
        raise ValueError(
            "El tema de interfaz es inválido."
        )

    if configuracion["idioma"] not in (
        "es-ES",
        "en-US"
    ):
        raise ValueError(
            "El idioma es inválido."
        )

    if type(
        configuracion["tamano_fuente"]
    ) is not int:
        raise ValueError(
            "El tamaño de fuente es inválido."
        )

    if not (
        8
        <= configuracion["tamano_fuente"]
        <= 40
    ):
        raise ValueError(
            "El tamaño de fuente debe estar "
            "entre 8 y 40."
        )

    if not validar_color(
        configuracion["color_barra_menu"]
    ):
        raise ValueError(
            "El color de la barra de menú "
            "es inválido."
        )

    if not validar_color(
        configuracion["color_letra"]
    ):
        raise ValueError(
            "El color de letra es inválido."
        )

    if not isinstance(
        configuracion[
            "color_letra_personalizado"
        ],
        bool
    ):
        raise ValueError(
            "El estado del color personalizado "
            "es inválido."
        )

    if not isinstance(
        configuracion["foto_perfil"],
        str
    ):
        raise ValueError(
            "La ruta de la foto de perfil "
            "es inválida."
        )


def cargar_configuracion():
    try:
        with open(
            ARCHIVO_CONFIG,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )

        if not isinstance(datos, dict):
            raise ValueError(
                "Formato de configuración inválido."
            )

        configuracion = (
            CONFIGURACION_PREDETERMINADA.copy()
        )

        configuracion.update(
            datos
        )

        validar_configuracion(
            configuracion
        )

        return (
            configuracion,
            None
        )

    except FileNotFoundError:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "No existe un archivo de configuración. "
            "Se utilizarán valores predeterminados."
        )

    except (
        json.JSONDecodeError,
        ValueError,
        KeyError,
        TypeError
    ):
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "El archivo de configuración está "
            "corrupto o tiene un formato inválido. "
            "Se utilizarán valores predeterminados."
        )

    except PermissionError:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "No se tienen permisos para leer "
            "el archivo de configuración. "
            "Se utilizarán valores predeterminados."
        )

    except OSError as error:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            f"Error al leer la configuración: {error}"
        )


def guardar_configuracion(configuracion):
    try:
        validar_configuracion(
            configuracion
        )

        with open(
            ARCHIVO_TEMPORAL,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                configuracion,
                archivo,
                ensure_ascii=False,
                indent=4
            )

            archivo.flush()

            os.fsync(
                archivo.fileno()
            )

        if os.path.exists(
            ARCHIVO_CONFIG
        ):
            shutil.copy2(
                ARCHIVO_CONFIG,
                ARCHIVO_RESPALDO
            )

        os.replace(
            ARCHIVO_TEMPORAL,
            ARCHIVO_CONFIG
        )

        return (
            True,
            None
        )

    except (
        ValueError,
        KeyError,
        TypeError
    ) as error:

        eliminar_temporal()

        return (
            False,
            f"La configuración contiene "
            f"datos inválidos: {error}"
        )

    except PermissionError:
        eliminar_temporal()

        return (
            False,
            "No se tienen permisos para escribir "
            "el archivo de configuración."
        )

    except OSError as error:
        eliminar_temporal()

        return (
            False,
            f"Error al guardar la configuración: {error}"
        )


def eliminar_temporal():
    try:
        if os.path.exists(
            ARCHIVO_TEMPORAL
        ):
            os.remove(
                ARCHIVO_TEMPORAL
            )

    except OSError:
        pass