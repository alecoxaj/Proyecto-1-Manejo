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
    QPushButton,
    QColorDialog,
    QFileDialog,
    QMessageBox
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

from configuracion import (
    cargar_configuracion,
    guardar_configuracion
)


class VentanaSettings(QDialog):
    def __init__(self, configuracion):
        super().__init__()

        self.configuracion = configuracion.copy()

        self.setFixedSize(500, 480)

        self.nombre_usuario = QLineEdit()

        self.tema = QComboBox()

        self.idioma = QComboBox()
        self.idioma.addItem("Español", "es-ES")
        self.idioma.addItem("English", "en-US")

        self.tamano_fuente = QSpinBox()
        self.tamano_fuente.setRange(8, 40)

        self.boton_color_menu = QPushButton()
        self.boton_color_menu.clicked.connect(
            self.seleccionar_color_menu
        )

        self.boton_color_letra = QPushButton()
        self.boton_color_letra.clicked.connect(
            self.seleccionar_color_letra
        )

        self.boton_foto = QPushButton()
        self.boton_foto.clicked.connect(
            self.seleccionar_foto
        )

        self.ruta_foto = QLabel()

        self.boton_guardar = QPushButton()
        self.boton_guardar.clicked.connect(
            self.guardar
        )

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

        self.setLayout(self.formulario)

        self.cargar_datos()

        self.idioma.currentIndexChanged.connect(
            self.actualizar_textos
        )

        self.actualizar_textos()

    def cargar_datos(self):
        self.nombre_usuario.setText(
            self.configuracion["nombre_usuario"]
        )

        idioma_actual = self.configuracion["idioma"]

        indice_idioma = self.idioma.findData(
            idioma_actual
        )

        if indice_idioma >= 0:
            self.idioma.setCurrentIndex(
                indice_idioma
            )

        self.tamano_fuente.setValue(
            self.configuracion["tamano_fuente"]
        )

        self.color_menu = self.configuracion[
            "color_barra_menu"
        ]

        self.color_letra = self.configuracion[
            "color_letra"
        ]

        self.foto_perfil = self.configuracion[
            "foto_perfil"
        ]

        if self.foto_perfil:
            self.ruta_foto.setText(
                os.path.basename(
                    self.foto_perfil
                )
            )

        self.actualizar_textos()

    def actualizar_textos(self):
        idioma = self.idioma.currentData()

        tema_actual = self.tema.currentData()

        self.tema.blockSignals(True)
        self.tema.clear()

        if idioma == "en-US":
            self.setWindowTitle("Settings")

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

            self.tema.addItem(
                "Light",
                "Claro"
            )

            self.tema.addItem(
                "Dark",
                "Oscuro"
            )

            self.boton_guardar.setText(
                "Save settings"
            )

            if not self.foto_perfil:
                self.boton_foto.setText(
                    "Select picture"
                )

        else:
            self.setWindowTitle("Configuración")

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

            self.tema.addItem(
                "Claro",
                "Claro"
            )

            self.tema.addItem(
                "Oscuro",
                "Oscuro"
            )

            self.boton_guardar.setText(
                "Guardar configuración"
            )

            if not self.foto_perfil:
                self.boton_foto.setText(
                    "Seleccionar foto"
                )

        indice_tema = self.tema.findData(
            tema_actual
        )

        if indice_tema < 0:
            indice_tema = self.tema.findData(
                self.configuracion["tema_interfaz"]
            )

        if indice_tema >= 0:
            self.tema.setCurrentIndex(
                indice_tema
            )

        self.tema.blockSignals(False)

        self.boton_color_menu.setText(
            self.color_menu
        )

        self.boton_color_letra.setText(
            self.color_letra
        )

    def seleccionar_color_menu(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_menu = color.name()

            self.boton_color_menu.setText(
                self.color_menu
            )

    def seleccionar_color_letra(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_letra = color.name()

            self.boton_color_letra.setText(
                self.color_letra
            )

    def seleccionar_foto(self):
        idioma = self.idioma.currentData()

        if idioma == "en-US":
            titulo = "Select profile picture"
            filtro = "Images (*.png *.jpg *.jpeg)"
        else:
            titulo = "Seleccionar foto de perfil"
            filtro = "Imágenes (*.png *.jpg *.jpeg)"

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            titulo,
            "",
            filtro
        )

        if archivo:
            self.foto_perfil = archivo

            self.ruta_foto.setText(
                os.path.basename(archivo)
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
        nueva_configuracion = {
            "nombre_usuario":
                self.nombre_usuario.text(),

            "tema_interfaz":
                self.tema.currentData(),

            "idioma":
                self.idioma.currentData(),

            "tamano_fuente":
                self.tamano_fuente.value(),

            "color_barra_menu":
                self.color_menu,

            "color_letra":
                self.color_letra,

            "foto_perfil":
                self.foto_perfil
        }

        correcto, error = guardar_configuracion(
            nueva_configuracion
        )

        idioma = self.idioma.currentData()

        if correcto:
            self.configuracion = nueva_configuracion

            if idioma == "en-US":
                titulo = "Settings"
                mensaje = "Your settings were saved successfully."
            else:
                titulo = "Configuración"
                mensaje = "Tu configuración se guardó correctamente."

            QMessageBox.information(
                self,
                titulo,
                mensaje
            )

            self.accept()

        else:
            if idioma == "en-US":
                titulo = "Error"
            else:
                titulo = "Error"

            QMessageBox.critical(
                self,
                titulo,
                error
            )

    def cargar_datos(self):
        self.nombre_usuario.setText(
            self.configuracion["nombre_usuario"]
        )

        self.tema.setCurrentText(
            self.configuracion["tema_interfaz"]
        )

        indice_idioma = self.idioma.findData(
            self.configuracion["idioma"]
        )

        if indice_idioma >= 0:
            self.idioma.setCurrentIndex(
                indice_idioma
            )

        self.tamano_fuente.setValue(
            self.configuracion["tamano_fuente"]
        )

        self.color_menu = self.configuracion[
            "color_barra_menu"
        ]

        self.color_letra = self.configuracion[
            "color_letra"
        ]

        self.foto_perfil = self.configuracion[
            "foto_perfil"
        ]

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

    def seleccionar_color_menu(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_menu = color.name()

            self.boton_color_menu.setText(
                self.color_menu
            )

    def seleccionar_color_letra(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_letra = color.name()

            self.boton_color_letra.setText(
                self.color_letra
            )

    def seleccionar_foto(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar foto de perfil",
            "",
            "Imágenes (*.png *.jpg *.jpeg)"
        )

        if archivo:
            self.foto_perfil = archivo

            self.ruta_foto.setText(
                os.path.basename(archivo)
            )

    def guardar(self):
        nueva_configuracion = {
            "nombre_usuario":
                self.nombre_usuario.text(),

            "tema_interfaz":
                self.tema.currentText(),

            "idioma":
                self.idioma.currentData(),

            "tamano_fuente":
                self.tamano_fuente.value(),

            "color_barra_menu":
                self.color_menu,

            "color_letra":
                self.color_letra,

            "foto_perfil":
                self.foto_perfil
        }

        correcto, error = guardar_configuracion(
            nueva_configuracion
        )

        if correcto:
            self.configuracion = nueva_configuracion

            QMessageBox.information(
                self,
                "Configuración",
                "La configuración se guardó correctamente."
            )

            self.accept()

        else:
            QMessageBox.critical(
                self,
                "Error",
                error
            )


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.configuracion, self.error_carga = (
            cargar_configuracion()
        )

        self.setWindowTitle(
            "Gestión de Configuración de Usuario"
        )

        self.resize(900, 550)

        self.crear_menu()
        self.crear_interfaz()

        self.aplicar_configuracion()

        if self.error_carga:
            QTimer.singleShot(
                200,
                self.mostrar_error_carga
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
            self.configuracion
        )

        resultado = ventana.exec()

        if resultado == QDialog.DialogCode.Accepted:
            self.configuracion = (
                ventana.configuracion
            )

            self.aplicar_configuracion()

    def aplicar_configuracion(self):
        tema = self.configuracion[
            "tema_interfaz"
        ]

        color_menu = self.configuracion[
            "color_barra_menu"
        ]

        tamano = self.configuracion[
            "tamano_fuente"
        ]

        if tema == "Oscuro":
            fondo = "#202124"
            controles = "#303134"
            borde = "#5f6368"

            # Texto general
            color_letra = "#ffffff"

            # Texto de la barra del menú
            color_texto_menu = "#000000"

        else:
            fondo = "#ffffff"
            controles = "#f5f5f5"
            borde = "#cccccc"

            # Texto general
            color_letra = "#000000"

            # Texto de la barra del menú
            color_texto_menu = "#000000"

        estilo = f"""
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

            QLineEdit,
            QComboBox,
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

            QMenuBar {{
                background-color: {color_menu};
                color: {color_texto_menu};
            }}

            QMenuBar::item {{
                color: {color_texto_menu};
                padding: 6px 10px;
            }}

            QMenuBar::item:selected {{
                background-color: #d6d6d6;
                color: #000000;
            }}

            QMenu {{
                background-color: {controles};
                color: {color_letra};
            }}

            QMenu::item:selected {{
                background-color: #505050;
            }}
        """

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
                "Utilice Settings para modificar "
                "las preferencias del usuario."
            )

    def actualizar_foto(self):
        ruta = self.configuracion[
            "foto_perfil"
        ]

        if ruta and os.path.exists(ruta):
            imagen = QPixmap(ruta)

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
        QMessageBox.warning(
            self,
            "Configuración",
            self.error_carga
        )


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec())