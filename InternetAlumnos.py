#!/usr/bin/env python3

import sys
import getpass
from FirewallServer import FirewallServer
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QRadioButton,
                             QDesktopWidget)
# Variable global donde se guardará la conexión con el Firewall
global fw1


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InternetAlumnos")
        self.setFixedSize(400, 200)

        layout = QGridLayout()

        label_info = QLabel('<font size="5"> Introduce tu usuario/contraseña </font>')
        layout.addWidget(label_info, 0, 0, 1, 3)

        label_username = QLabel('<font size="4"> Usuario: </font>')

        self.edit_username = QLineEdit()
        usuario = getpass.getuser()
        self.edit_username.setText(usuario)

        layout.addWidget(label_username, 2, 0, 1, 1)
        layout.addWidget(self.edit_username, 2, 1, 1, 2)

        label_password = QLabel('<font size="4"> Password: </font>')
        self.edit_password = QLineEdit()
        self.edit_password.setPlaceholderText('Introduce tu password...')
        self.edit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 3, 0, 1, 1)
        layout.addWidget(self.edit_password, 3, 1, 1, 2)

        self.label_error = QLabel('')
        layout.addWidget(self.label_error, 4, 1, 1, 2)

        button_login = QPushButton('Login')
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login, 5, 2, 1, 1)
        layout.setRowMinimumHeight(2, 55)

        self.center()
        self.setLayout(layout)

    def center(self):
        # Geometry of the main window
        qr = self.frameGeometry()

        # Center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # Move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # Top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def login(self):
        # Si obtenemos reglas del firewall estamos bien autenticados
        global fw1
        fw1 = FirewallServer(self.edit_username.text(), self.edit_password.text())
        reglas_fw = fw1.obtener_reglas_fw()
        if reglas_fw is None:
            self.label_error.setText('<i><font size="3" color="red"> Error en la conexión. </font></i>')
        else:
            self.form_main = InternetAlumnos(reglas_fw)
            self.form_main.show()
            self.hide()


class InternetAlumnos(QWidget):
    def __init__(self, reglas_fw):
        super().__init__()
        self.reglas_fw = reglas_fw
        self.setWindowTitle("InternetAlumnos")
        self.setFixedSize(400, 200)

        layout = QGridLayout()

        self.radio_activar = QRadioButton('Activar Internet a los alumnos.')
        self.radio_bloquear = QRadioButton('Bloquear Internet a los alumnos.')

        self.radio_activar.toggled.connect(self.activar_fw)
        self.radio_bloquear.toggled.connect(self.bloquear_fw)

        layout.addWidget(self.radio_activar, 1, 1, 1, 3)
        layout.addWidget(self.radio_bloquear, 2, 1, 1, 3)

        # Si obtenemos reglas vacías el el acceso a Internet está ACTIVADO
        if not reglas_fw:
            self.label_estado = QLabel(
                '<font size="4"> Alumnos con Internet: <font color="green"> ACTIVADO </font></font>')
            self.radio_activar.setChecked(True)
        else:
            self.label_estado = QLabel(
                '<font size="4"> Alumnos con Internet: <font color="red"> BLOQUEADO </font> </font>')
            self.radio_bloquear.setChecked(True)

        layout.addWidget(self.label_estado, 0, 0, 1, 5)

        button_salir = QPushButton('Salir')
        button_salir.clicked.connect(self.salir)
        layout.addWidget(button_salir, 3, 4, 1, 1)
        layout.setRowMinimumHeight(2, 55)

        self.center()
        self.setLayout(layout)

    def activar_fw(self):
        fw1.activar_internet()
        self.label_estado.setText('<font size="4"> Alumnos con Internet: <font color="green"> ACTIVADO </font></font>')

    def bloquear_fw(self):
        fw1.bloquear_internet()
        self.label_estado.setText('<font size="4"> Alumnos con Internet: <font color="red"> BLOQUEADO </font> </font>')

    def salir(self):
        fw1.salir()
        self.close()

    def center(self):
        # Geometry of the main window
        qr = self.frameGeometry()

        # Center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # Move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # Top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form_login = Login()
    form_login.show()

    sys.exit(app.exec_())
