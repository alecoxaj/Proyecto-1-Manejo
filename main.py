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

    def guardar_configuracion(self):
        QMessageBox.information(
            self,
            "Configuración",
            "Configuración preparada para guardar."
        )

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Gestión de Configuración de Usuario"
        )

        self.resize(900, 550)

        self.crear_menu()
        self.crear_interfaz()

    def crear_menu(self):
        barra = self.menuBar()

        menu_archivo = barra.addMenu("Archivo")
        menu_edicion = barra.addMenu("Edición")
        menu_ver = barra.addMenu("Ver")

        accion_settings = barra.addAction("Settings")

        menu_archivo.addAction("Nuevo")
        menu_archivo.addAction("Abrir")
        menu_archivo.addSeparator()

        accion_salir = menu_archivo.addAction("Salir")

        menu_edicion.addAction("Copiar")
        menu_edicion.addAction("Pegar")

        menu_ver.addAction("Actualizar")

        accion_settings.triggered.connect(
            self.abrir_settings
        )

        accion_salir.triggered.connect(
            self.close
        )

    def crear_interfaz(self):
        titulo = QLabel(
            "Gestión de Configuración de Usuario"
        )

        titulo.setStyleSheet(
            "font-size: 26px;"
            "font-weight: bold;"
        )

        texto = QLabel(
            "Utilice la opción Settings para modificar "
            "la configuración del usuario."
        )

        layout = QVBoxLayout()

        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(texto)
        layout.addStretch()

        contenedor = QWidget()

        contenedor.setLayout(layout)

        self.setCentralWidget(contenedor)

