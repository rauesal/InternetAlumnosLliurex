import paramiko


class ComandoSSH:
    def __init__(self, servidor, usuario, password, comando):
        self._servidor = servidor
        self._usuario = usuario
        self._password = password
        self._comando = comando
        self._cliente = None

    @property
    def comando(self):
        return self._comando

    @comando.setter
    def comando(self, comando):
        self._comando = comando

    def conectar(self):
        try:
            # Conectamos por ssh
            self._cliente = paramiko.SSHClient()
            self._cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._cliente.load_system_host_keys()
            self._cliente.connect(hostname=self._servidor, username=self._usuario, password=self._password)
        except Exception as e:
            print(f'Error en la conexión: {e}')
            self._cliente.close()
            return "error"

    def ejecutar(self):
        try:
            self._cliente.invoke_shell()
            try:
                # Ejecutamos el comando remoto
                stdin, stdout, stderr = self._cliente.exec_command(self._comando, bufsize=-1, timeout=5,
                                                                   get_pty=True,
                                                                   environment=None)
                # Devolvemos una lista con cada linea de la salida
                salida = []
                for line in iter(stdout.readline, ""):
                    # print(line, end="")
                    salida.append(line.rstrip())
                return salida
            except Exception as e:
                print(f'Error al ejecutar el comando: {e}')

        except Exception as e:
            print(f'Error en la conexión por ssh: {e}')

    def cerrar(self):
        self._cliente.close()
