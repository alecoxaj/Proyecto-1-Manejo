import json
import os
import shutill

ARCHIVO_CONFIG = "config.json"
ARCHIVO_TEMPORAL = "config.tmp"
ARCHIVO_RESPALD0 = "config.bak"

CONFIGURACION_PREDETERMINADA = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "Claro",
    "idioma": "es-ES",
    "tamano_fuente": 14,
    "color_barra_menu": "#f0f0f0",
    "color_letra": "#000000",
    "foto_perfil": ""
}


