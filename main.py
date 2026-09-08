import sys

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

class VentanaSettings(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(450, 400)

        self.color_menu = "#FFFFFF"
        self.color_letra = "#000000"
        self.foto_perfil = ""

        self.nombre_usuario = QLineEdit()

        self.tema = QComboBox()
        self.tema.addItems(["Claro", "Oscuro"])

        self.idioma = QComboBox()
        self.idioma.addItems(["es-ES", "en-US"])

        self.tamano_fuente = QSpinBox()
        self.tamano_fuente.setRange(8, 40)
        self.tamano_fuente.setValue(14)

        self.boton_color_menu = QPushButton("Seleccionar color")
        self.boton_color_menu.clicked.connect(
            self.seleccionar_color_menu
        )

        self.boton_color_letra = QPushButton("Seleccionar color")
        self.boton_color_letra.clicked.connect(
            self.seleccionar_color_letra
        )

        self.boton_foto = QPushButton("Seleccionar foto")
        self.boton_foto.clicked.connect(
            self.seleccionar_foto
        )

        self.boton_guardar = QPushButton("Guardar configuración")
        self.boton_guardar.clicked.connect(
            self.guardar_configuracion
        )

        formulario = QFormLayout()

        formulario.addRow(
            "Nombre de usuario:",
            self.nombre_usuario
        )

        formulario.addRow(
            "Tema de interfaz:",
            self.tema
        )

        formulario.addRow(
            "Idioma:",
            self.idioma
        )

        formulario.addRow(
            "Tamaño de fuente:",
            self.tamano_fuente
        )

        formulario.addRow(
            "Color barra de menú:",
            self.boton_color_menu
        )

        formulario.addRow(
            "Color de letra:",
            self.boton_color_letra
        )

        formulario.addRow(
            "Foto de perfil:",
            self.boton_foto
        )

        formulario.addRow(
            self.boton_guardar
        )

        self.setLayout(formulario)

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
            self.boton_foto.setText("Foto seleccionada")