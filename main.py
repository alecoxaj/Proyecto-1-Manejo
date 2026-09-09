import sys
import os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QAbstractSpinBox,
    QPushButton,
    QColorDialog,
    QFileDialog,
    QMessageBox
)

from PySide6.QtGui import QPixmap

from PySide6.QtCore import (
    Qt,
    QTimer
)

from configuracion import (
    cargar_configuracion,
    guardar_configuracion
)


def color_predeterminado_tema(tema):
    if tema == "Oscuro":
        return "#ffffff"

    return "#000000"


def color_fue_personalizado(configuracion):
    if "color_letra_personalizado" in configuracion:
        return configuracion[
            "color_letra_personalizado"
        ]

    color = configuracion.get(
        "color_letra",
        ""
    ).lower()

    if color not in (
        "",
        "#000000",
        "#ffffff"
    ):
        return True

    return False


def crear_estilo(
    tema,
    color_menu,
    color_letra,
    tamano
):
    if tema == "Oscuro":
        fondo = "#202124"
        controles = "#303134"
        borde = "#5f6368"

        fondo_lista = "#303134"
        texto_lista = "#ffffff"

        seleccion_lista = "#505050"
        texto_seleccion = "#ffffff"

        fondo_menu = "#303134"
        texto_menu = "#ffffff"

    else:
        fondo = "#ffffff"
        controles = "#f5f5f5"
        borde = "#cccccc"

        fondo_lista = "#ffffff"
        texto_lista = "#000000"

        seleccion_lista = "#d6d6d6"
        texto_seleccion = "#000000"

        fondo_menu = "#ffffff"
        texto_menu = "#000000"

    return f"""
        QMainWindow {{
            background-color: {fondo};
        }}

        QDialog {{
            background-color: {fondo};
        }}

        QLabel {{
            color: {color_letra};
            font-size: {tamano}px;
        }}

        QLineEdit {{
            background-color: {controles};
            color: {color_letra};
            border: 1px solid {borde};
            padding: 5px;
        }}

        QComboBox {{
            background-color: {controles};
            color: {color_letra};
            border: 1px solid {borde};
            padding: 5px;
        }}

        QSpinBox {{
            background-color: {controles};
            color: {color_letra};
            border: 1px solid {borde};
            padding: 5px;
        }}

        QPushButton {{
            background-color: {controles};
            color: {color_letra};
            border: 1px solid {borde};
            padding: 6px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {fondo_lista};
            color: {texto_lista};
            selection-background-color: {seleccion_lista};
            selection-color: {texto_seleccion};
            border: 1px solid {borde};
            outline: none;
        }}

        QMenuBar {{
            background-color: {color_menu};
            color: #000000;
        }}

        QMenuBar::item {{
            background-color: transparent;
            color: #000000;
            padding: 6px 10px;
        }}

        QMenuBar::item:selected {{
            background-color: #d6d6d6;
            color: #000000;
        }}

        QMenu {{
            background-color: {fondo_menu};
            color: {texto_menu};
        }}

        QMenu::item {{
            background-color: transparent;
            color: {texto_menu};
            padding: 6px 25px;
        }}

        QMenu::item:selected {{
            background-color: {seleccion_lista};
            color: {texto_seleccion};
        }}
    """


class VentanaSettings(QDialog):
    def __init__(
        self,
        configuracion,
        parent=None
    ):
        super().__init__(parent)

        self.configuracion = configuracion.copy()

        self.color_menu = self.configuracion[
            "color_barra_menu"
        ]

        self.color_personalizado = (
            color_fue_personalizado(
                self.configuracion
            )
        )

        if self.color_personalizado:
            self.color_letra = (
                self.configuracion[
                    "color_letra"
                ]
            )

        else:
            self.color_letra = (
                color_predeterminado_tema(
                    self.configuracion[
                        "tema_interfaz"
                    ]
                )
            )

        self.foto_perfil = self.configuracion[
            "foto_perfil"
        ]

        self.setFixedSize(
            520,
            500
        )

        self.nombre_usuario = QLineEdit()

        self.tema = QComboBox()

        self.idioma = QComboBox()

        self.tamano_fuente = QSpinBox()

        self.tamano_fuente.setRange(
            8,
            40
        )

        self.tamano_fuente.setSingleStep(
            1
        )

        self.tamano_fuente.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.UpDownArrows
        )

        self.tamano_fuente.setMinimumWidth(
            120
        )

        self.boton_color_menu = QPushButton()

        self.boton_color_letra = QPushButton()

        self.boton_foto = QPushButton()

        self.boton_guardar = QPushButton()

        self.ruta_foto = QLabel()

        self.etiqueta_nombre = QLabel()
        self.etiqueta_tema = QLabel()
        self.etiqueta_idioma = QLabel()
        self.etiqueta_fuente = QLabel()
        self.etiqueta_color_menu = QLabel()
        self.etiqueta_color_letra = QLabel()
        self.etiqueta_foto = QLabel()

        self.formulario = QFormLayout()

        self.formulario.addRow(
            self.etiqueta_nombre,
            self.nombre_usuario
        )

        self.formulario.addRow(
            self.etiqueta_tema,
            self.tema
        )

        self.formulario.addRow(
            self.etiqueta_idioma,
            self.idioma
        )

        self.formulario.addRow(
            self.etiqueta_fuente,
            self.tamano_fuente
        )

        self.formulario.addRow(
            self.etiqueta_color_menu,
            self.boton_color_menu
        )

        self.formulario.addRow(
            self.etiqueta_color_letra,
            self.boton_color_letra
        )

        self.formulario.addRow(
            self.etiqueta_foto,
            self.boton_foto
        )

        self.formulario.addRow(
            "",
            self.ruta_foto
        )

        self.formulario.addRow(
            self.boton_guardar
        )

        self.setLayout(
            self.formulario
        )

        self.cargar_datos()

        self.idioma.currentIndexChanged.connect(
            self.cambiar_idioma
        )

        self.tema.currentIndexChanged.connect(
            self.cambiar_tema
        )

        self.boton_color_menu.clicked.connect(
            self.seleccionar_color_menu
        )

        self.boton_color_letra.clicked.connect(
            self.seleccionar_color_letra
        )

        self.boton_foto.clicked.connect(
            self.seleccionar_foto
        )

        self.boton_guardar.clicked.connect(
            self.guardar
        )

    def cargar_datos(self):
        self.nombre_usuario.setText(
            self.configuracion[
                "nombre_usuario"
            ]
        )

        self.tamano_fuente.setValue(
            self.configuracion[
                "tamano_fuente"
            ]
        )

        idioma = self.configuracion[
            "idioma"
        ]

        tema = self.configuracion[
            "tema_interfaz"
        ]

        self.configurar_comboboxes(
            idioma,
            tema
        )

        self.traducir_settings(
            idioma
        )

        self.boton_color_menu.setText(
            self.color_menu
        )

        self.boton_color_letra.setText(
            self.color_letra
        )

        if self.foto_perfil:
            self.ruta_foto.setText(
                os.path.basename(
                    self.foto_perfil
                )
            )

    def configurar_comboboxes(
        self,
        idioma,
        tema
    ):
        self.idioma.blockSignals(
            True
        )

        self.tema.blockSignals(
            True
        )

        self.idioma.clear()
        self.tema.clear()

        if idioma == "en-US":
            self.idioma.addItem(
                "Spanish",
                "es-ES"
            )

            self.idioma.addItem(
                "English",
                "en-US"
            )

            self.tema.addItem(
                "Light",
                "Claro"
            )

            self.tema.addItem(
                "Dark",
                "Oscuro"
            )

        else:
            self.idioma.addItem(
                "Español",
                "es-ES"
            )

            self.idioma.addItem(
                "Inglés",
                "en-US"
            )

            self.tema.addItem(
                "Claro",
                "Claro"
            )

            self.tema.addItem(
                "Oscuro",
                "Oscuro"
            )

        indice_idioma = (
            self.idioma.findData(
                idioma
            )
        )

        if indice_idioma >= 0:
            self.idioma.setCurrentIndex(
                indice_idioma
            )

        indice_tema = (
            self.tema.findData(
                tema
            )
        )

        if indice_tema >= 0:
            self.tema.setCurrentIndex(
                indice_tema
            )

        self.idioma.blockSignals(
            False
        )

        self.tema.blockSignals(
            False
        )

    def traducir_settings(
        self,
        idioma
    ):
        if idioma == "en-US":
            self.setWindowTitle(
                "Settings"
            )

            self.etiqueta_nombre.setText(
                "Username:"
            )

            self.etiqueta_tema.setText(
                "Interface theme:"
            )

            self.etiqueta_idioma.setText(
                "Language:"
            )

            self.etiqueta_fuente.setText(
                "Font size:"
            )

            self.etiqueta_color_menu.setText(
                "Menu bar color:"
            )

            self.etiqueta_color_letra.setText(
                "Text color:"
            )

            self.etiqueta_foto.setText(
                "Profile picture:"
            )

            self.boton_guardar.setText(
                "Save settings"
            )

            if self.foto_perfil:
                self.boton_foto.setText(
                    "Picture selected"
                )

            else:
                self.boton_foto.setText(
                    "Select picture"
                )

        else:
            self.setWindowTitle(
                "Configuración"
            )

            self.etiqueta_nombre.setText(
                "Nombre de usuario:"
            )

            self.etiqueta_tema.setText(
                "Tema de interfaz:"
            )

            self.etiqueta_idioma.setText(
                "Idioma:"
            )

            self.etiqueta_fuente.setText(
                "Tamaño de fuente:"
            )

            self.etiqueta_color_menu.setText(
                "Color de la barra de menú:"
            )

            self.etiqueta_color_letra.setText(
                "Color de letra:"
            )

            self.etiqueta_foto.setText(
                "Foto de perfil:"
            )

            self.boton_guardar.setText(
                "Guardar configuración"
            )

            if self.foto_perfil:
                self.boton_foto.setText(
                    "Foto seleccionada"
                )

            else:
                self.boton_foto.setText(
                    "Seleccionar foto"
                )

    def cambiar_idioma(
        self,
        indice=None
    ):
        idioma = self.idioma.currentData()

        tema = self.tema.currentData()

        if idioma is None:
            return

        if tema is None:
            tema = "Claro"

        self.configurar_comboboxes(
            idioma,
            tema
        )

        self.traducir_settings(
            idioma
        )

    def cambiar_tema(
        self,
        indice=None
    ):
        tema = self.tema.currentData()

        if tema is None:
            return

        if not self.color_personalizado:
            self.color_letra = (
                color_predeterminado_tema(
                    tema
                )
            )

            self.boton_color_letra.setText(
                self.color_letra
            )

    def seleccionar_color_menu(self):
        color = QColorDialog.getColor(
            parent=self
        )

        if color.isValid():
            self.color_menu = (
                color.name()
            )

            self.boton_color_menu.setText(
                self.color_menu
            )

    def seleccionar_color_letra(self):
        color = QColorDialog.getColor(
            parent=self
        )

        if color.isValid():
            self.color_letra = (
                color.name()
            )

            self.color_personalizado = True

            self.boton_color_letra.setText(
                self.color_letra
            )

    def seleccionar_foto(self):
        idioma = self.idioma.currentData()

        if idioma == "en-US":
            titulo = (
                "Select profile picture"
            )

            filtro = (
                "Images (*.png *.jpg *.jpeg)"
            )

        else:
            titulo = (
                "Seleccionar foto de perfil"
            )

            filtro = (
                "Imágenes (*.png *.jpg *.jpeg)"
            )

        archivo, _ = (
            QFileDialog.getOpenFileName(
                self,
                titulo,
                "",
                filtro
            )
        )

        if archivo:
            self.foto_perfil = archivo

            self.ruta_foto.setText(
                os.path.basename(
                    archivo
                )
            )

            if idioma == "en-US":
                self.boton_foto.setText(
                    "Picture selected"
                )

            else:
                self.boton_foto.setText(
                    "Foto seleccionada"
                )

    def guardar(self):
        idioma = self.idioma.currentData()

        tema = self.tema.currentData()

        if not self.color_personalizado:
            self.color_letra = (
                color_predeterminado_tema(
                    tema
                )
            )

        nueva_configuracion = {
            "nombre_usuario":
                self.nombre_usuario.text(),

            "tema_interfaz":
                tema,

            "idioma":
                idioma,

            "tamano_fuente":
                self.tamano_fuente.value(),

            "color_barra_menu":
                self.color_menu,

            "color_letra":
                self.color_letra,

            "color_letra_personalizado":
                self.color_personalizado,

            "foto_perfil":
                self.foto_perfil
        }

        correcto, error = (
            guardar_configuracion(
                nueva_configuracion
            )
        )

        if correcto:
            self.configuracion = (
                nueva_configuracion
            )

            estilo = crear_estilo(
                nueva_configuracion[
                    "tema_interfaz"
                ],
                nueva_configuracion[
                    "color_barra_menu"
                ],
                nueva_configuracion[
                    "color_letra"
                ],
                nueva_configuracion[
                    "tamano_fuente"
                ]
            )

            QApplication.instance().setStyleSheet(
                estilo
            )

            if idioma == "en-US":
                titulo = "Settings"

                mensaje = (
                    "Your settings were "
                    "saved successfully."
                )

            else:
                titulo = "Configuración"

                mensaje = (
                    "Tu configuración se "
                    "guardó correctamente."
                )

            QMessageBox.information(
                self,
                titulo,
                mensaje
            )

            self.accept()

        else:
            self.mostrar_error_guardado(
                error
            )

    def mostrar_error_guardado(
        self,
        error
    ):
        idioma = self.idioma.currentData()

        texto_error = str(error).lower()

        sin_permiso = (
            error == "sin_permiso_escritura"
            or "permiso" in texto_error
            or "permission" in texto_error
        )

        if idioma == "en-US":
            if sin_permiso:
                mensaje = (
                    "You don't have permission "
                    "to save the settings."
                )

            else:
                mensaje = (
                    "We couldn't save "
                    "your settings."
                )

        else:
            if sin_permiso:
                mensaje = (
                    "No tienes permisos para "
                    "guardar la configuración."
                )

            else:
                mensaje = (
                    "No pudimos guardar "
                    "tu configuración."
                )

        QMessageBox.critical(
            self,
            "Error",
            mensaje
        )


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.configuracion, self.error_carga = (
            cargar_configuracion()
        )

        self.preparar_color_texto()

        self.resize(
            900,
            550
        )

        self.crear_menu()

        self.crear_interfaz()

        self.aplicar_configuracion()

        if self.error_carga:
            QTimer.singleShot(
                200,
                self.mostrar_error_carga
            )

    def preparar_color_texto(self):
        personalizado = (
            color_fue_personalizado(
                self.configuracion
            )
        )

        self.configuracion[
            "color_letra_personalizado"
        ] = personalizado

        if not personalizado:
            self.configuracion[
                "color_letra"
            ] = color_predeterminado_tema(
                self.configuracion[
                    "tema_interfaz"
                ]
            )

    def crear_menu(self):
        barra = self.menuBar()

        self.menu_archivo = barra.addMenu(
            "Archivo"
        )

        self.menu_edicion = barra.addMenu(
            "Edición"
        )

        self.menu_ver = barra.addMenu(
            "Ver"
        )

        self.accion_settings = barra.addAction(
            "Settings"
        )

        self.accion_nuevo = (
            self.menu_archivo.addAction(
                "Nuevo"
            )
        )

        self.accion_abrir = (
            self.menu_archivo.addAction(
                "Abrir"
            )
        )

        self.menu_archivo.addSeparator()

        self.accion_salir = (
            self.menu_archivo.addAction(
                "Salir"
            )
        )

        self.accion_copiar = (
            self.menu_edicion.addAction(
                "Copiar"
            )
        )

        self.accion_pegar = (
            self.menu_edicion.addAction(
                "Pegar"
            )
        )

        self.accion_actualizar = (
            self.menu_ver.addAction(
                "Actualizar"
            )
        )

        self.accion_settings.triggered.connect(
            self.abrir_settings
        )

        self.accion_salir.triggered.connect(
            self.close
        )

    def crear_interfaz(self):
        self.titulo = QLabel()

        self.titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.saludo = QLabel()

        self.saludo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.descripcion = QLabel()

        self.descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.foto = QLabel()

        self.foto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.foto.setFixedSize(
            150,
            150
        )

        layout = QVBoxLayout()

        layout.addStretch()

        layout.addWidget(
            self.titulo
        )

        layout.addWidget(
            self.saludo
        )

        layout.addWidget(
            self.foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.descripcion
        )

        layout.addStretch()

        contenedor = QWidget()

        contenedor.setLayout(
            layout
        )

        self.setCentralWidget(
            contenedor
        )

    def abrir_settings(self):
        ventana = VentanaSettings(
            self.configuracion,
            self
        )

        resultado = ventana.exec()

        if (
            resultado
            == QDialog.DialogCode.Accepted
        ):
            self.configuracion = (
                ventana.configuracion
            )

            self.aplicar_configuracion()

    def aplicar_configuracion(self):
        personalizado = (
            self.configuracion.get(
                "color_letra_personalizado",
                False
            )
        )

        if not personalizado:
            self.configuracion[
                "color_letra"
            ] = color_predeterminado_tema(
                self.configuracion[
                    "tema_interfaz"
                ]
            )

        estilo = crear_estilo(
            self.configuracion[
                "tema_interfaz"
            ],
            self.configuracion[
                "color_barra_menu"
            ],
            self.configuracion[
                "color_letra"
            ],
            self.configuracion[
                "tamano_fuente"
            ]
        )

        QApplication.instance().setStyleSheet(
            estilo
        )

        self.actualizar_idioma()

        self.actualizar_foto()

    def actualizar_idioma(self):
        idioma = self.configuracion[
            "idioma"
        ]

        nombre = self.configuracion[
            "nombre_usuario"
        ]

        if idioma == "en-US":
            self.setWindowTitle(
                "User Settings Management"
            )

            self.menu_archivo.setTitle(
                "File"
            )

            self.menu_edicion.setTitle(
                "Edit"
            )

            self.menu_ver.setTitle(
                "View"
            )

            self.accion_nuevo.setText(
                "New"
            )

            self.accion_abrir.setText(
                "Open"
            )

            self.accion_salir.setText(
                "Exit"
            )

            self.accion_copiar.setText(
                "Copy"
            )

            self.accion_pegar.setText(
                "Paste"
            )

            self.accion_actualizar.setText(
                "Refresh"
            )

            self.accion_settings.setText(
                "Settings"
            )

            self.titulo.setText(
                "User Settings Management"
            )

            self.saludo.setText(
                f"Welcome, {nombre}"
            )

            self.descripcion.setText(
                "Use Settings to modify "
                "your preferences."
            )

        else:
            self.setWindowTitle(
                "Gestión de Configuración de Usuario"
            )

            self.menu_archivo.setTitle(
                "Archivo"
            )

            self.menu_edicion.setTitle(
                "Edición"
            )

            self.menu_ver.setTitle(
                "Ver"
            )

            self.accion_nuevo.setText(
                "Nuevo"
            )

            self.accion_abrir.setText(
                "Abrir"
            )

            self.accion_salir.setText(
                "Salir"
            )

            self.accion_copiar.setText(
                "Copiar"
            )

            self.accion_pegar.setText(
                "Pegar"
            )

            self.accion_actualizar.setText(
                "Actualizar"
            )

            self.accion_settings.setText(
                "Settings"
            )

            self.titulo.setText(
                "Gestión de Configuración de Usuario"
            )

            self.saludo.setText(
                f"Bienvenido, {nombre}"
            )

            self.descripcion.setText(
                "Utiliza Settings para modificar "
                "tus preferencias."
            )

    def actualizar_foto(self):
        ruta = self.configuracion[
            "foto_perfil"
        ]

        if (
            ruta
            and os.path.exists(ruta)
        ):
            imagen = QPixmap(
                ruta
            )

            imagen = imagen.scaled(
                140,
                140,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.foto.setPixmap(
                imagen
            )

        else:
            self.foto.clear()

    def mostrar_error_carga(self):
        idioma = self.configuracion[
            "idioma"
        ]

        texto_error = str(
            self.error_carga
        ).lower()

        if idioma == "en-US":
            titulo = "Settings"

            if (
                self.error_carga == "archivo_ausente"
                or "no existe" in texto_error
            ):
                mensaje = (
                    "No settings file was found. "
                    "Default values will be used."
                )

            elif (
                self.error_carga == "archivo_corrupto"
                or "corrupt" in texto_error
                or "inválido" in texto_error
                or "invalido" in texto_error
            ):
                mensaje = (
                    "Your settings file is corrupted "
                    "or has an invalid format. "
                    "Default values will be used."
                )

            elif (
                self.error_carga == "sin_permiso_lectura"
                or "permiso" in texto_error
            ):
                mensaje = (
                    "You don't have permission to "
                    "read the settings file. "
                    "Default values will be used."
                )

            else:
                mensaje = (
                    "We couldn't read your settings. "
                    "Default values will be used."
                )

        else:
            titulo = "Configuración"

            if (
                self.error_carga == "archivo_ausente"
                or "no existe" in texto_error
            ):
                mensaje = (
                    "No encontramos un archivo de "
                    "configuración. Usaremos los "
                    "valores predeterminados."
                )

            elif (
                self.error_carga == "archivo_corrupto"
                or "corrupt" in texto_error
                or "inválido" in texto_error
                or "invalido" in texto_error
            ):
                mensaje = (
                    "Tu archivo de configuración está "
                    "corrupto o tiene un formato inválido. "
                    "Usaremos los valores predeterminados."
                )

            elif (
                self.error_carga == "sin_permiso_lectura"
                or "permiso" in texto_error
            ):
                mensaje = (
                    "No tienes permisos para leer el "
                    "archivo de configuración. "
                    "Usaremos los valores predeterminados."
                )

            else:
                mensaje = (
                    "No pudimos leer tu configuración. "
                    "Usaremos los valores predeterminados."
                )

        QMessageBox.warning(
            self,
            titulo,
            mensaje
        )


app = QApplication(
    sys.argv
)

ventana = VentanaPrincipal()

ventana.show()

sys.exit(
    app.exec()
)