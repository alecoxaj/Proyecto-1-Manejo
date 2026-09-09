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
    "foto_perfil": ""
}

def cargar_configuracion():
    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, dict):
            raise ValueError("Formato de configuración inválido")

        configuracion = CONFIGURACION_PREDETERMINADA.copy()

        configuracion.update(datos)

        return configuracion, None

    except FileNotFoundError:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "No existe un archivo de configuración. "
            "Se utilizarán valores predeterminados."
        )

    except (json.JSONDecodeError, ValueError):
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "El archivo de configuración está corrupto o "
            "tiene un formato inválido. "
            "Se utilizarán valores predeterminados."
        )

    except PermissionError:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            "No se tienen permisos para leer el archivo "
            "de configuración. "
            "Se utilizarán valores predeterminados."
        )

    except OSError as error:
        return (
            CONFIGURACION_PREDETERMINADA.copy(),
            f"Error al leer la configuración: {error}"
        )

def guardar_configuracion(configuracion):
    try:
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

            os.fsync(archivo.fileno())

        if os.path.exists(ARCHIVO_CONFIG):
            shutil.copy2(
                ARCHIVO_CONFIG,
                ARCHIVO_RESPALDO
            )

        os.replace(
            ARCHIVO_TEMPORAL,
            ARCHIVO_CONFIG
        )

        return True, None

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
        if os.path.exists(ARCHIVO_TEMPORAL):
            os.remove(ARCHIVO_TEMPORAL)

    except OSError:
        pass



