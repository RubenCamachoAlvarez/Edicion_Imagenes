import socket

class SocketServidor(socket.socket):

    def __init__(self, direccion_IPv4, puerto_IPv4):

        self.datos_conexion = (direccion_IPv4, puerto_IPv4)


    def iniciar_servidor(self):

        self.bind(self.datos_conexion)

        self.listen()


    def escuchar_clientes:

        pass
