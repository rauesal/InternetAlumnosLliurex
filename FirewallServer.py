import subprocess
from ComandoSSH import ComandoSSH


def obtener_ip_profe():
    # Obtener IP con la que se accede a Internet "ip r get 1 | head -1 | cut -d' ' -f7"
    obtener_ip = subprocess.run(["ip r get 1 | head -1 | cut -d' ' -f7"], shell=True, stdout=subprocess.PIPE,
                                universal_newlines=True)
    ip_profe = obtener_ip.stdout.strip()
    return ip_profe


def obtener_ip_server():
    # Obtener IP del servidor "ip r | grep ^default | cut -d' ' -f3"
    obtener_gateway = subprocess.run(["ip r | grep ^default | cut -d' ' -f3"], shell=True, stdout=subprocess.PIPE,
                                     universal_newlines=True)
    ip_server = obtener_gateway.stdout.strip()
    return ip_server


def obtener_vlan():
    # Obtener la VLAN de la red
    vlan = obtener_ip_profe().split(".")[2]
    return vlan


class FirewallServer:
    def __init__(self, usuario, password):
        self._usuario = usuario
        self._password = password
        self._servidor = obtener_ip_server()
        self._ip_profe = obtener_ip_profe()
        self._vlan = obtener_vlan()
        self._cmd = None
        self._reglas_fw = []

    def obtener_reglas_fw(self):
        # Obtenemos las reglas de nuestra VLAN
        comando = f"sudo iptables -S | grep 'InternetAlumnos:RED{self._vlan}'"

        self._cmd = ComandoSSH(self._servidor, self._usuario, self._password, comando)
        self._cmd.conectar()
        self._reglas_fw = self._cmd.ejecutar()
        return self._reglas_fw

    def bloquear_internet(self):
        # Las reglas con "iptables -I" se insertan al principio.
        permitir_profe = f"sudo iptables -I FORWARD -s {self._ip_profe}/32 -p tcp -m comment --comment " \
                         f"InternetAlumnos:RED{self._vlan} -j ACCEPT "
        bloquear_red = f"sudo iptables -I FORWARD -s {self._ip_profe}/24 -p tcp -m comment --comment " \
                       f"InternetAlumnos:RED{self._vlan} -j DROP "
        self._cmd.comando = bloquear_red
        self._cmd.ejecutar()
        self._cmd.comando = permitir_profe
        self._cmd.ejecutar()

    def activar_internet(self):
        # Obtenemos las reglas de nuestra VLAN y las eliminamos
        self.obtener_reglas_fw()
        for regla in self._reglas_fw:
            regla = regla.replace("-A FORWARD", "-D FORWARD")
            self._cmd.comando = f"sudo iptables {regla}"
            self._cmd.ejecutar()

    def salir(self):
        # Cerramos la conexión con el servidor
        self._cmd.cerrar()
