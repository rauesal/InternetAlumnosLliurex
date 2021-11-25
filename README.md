# InternetAlumnosLliurex
Aplicación para controlar el acceso a Internet de los alumnos en el modelo de centro inteligente de Conselleria de Valencia con Lliurex.

Requisitos: tener algún usuario/grupo en el servidor de aula que puede modificar iptables con sudo sin contraseña.

Ejemplo para dar permiso a todos los profesores:
  sudo visudo
    "%teachers ALL=NOPASSWD:/sbin/iptables"
