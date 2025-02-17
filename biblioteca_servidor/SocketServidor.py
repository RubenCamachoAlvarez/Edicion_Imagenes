import socket

import threading

class SocketServidor(socket.socket):

    def __init__(self, direccion_IPv4, puerto_IPv4):

        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        self.datos_conexion = (direccion_IPv4, puerto_IPv4)


    def iniciar_servidor(self):

        self.bind(self.datos_conexion)

        self.listen()


    def atender_cliente(self, indice, conexion_cliente, direccion_puerto_cliente):

        print(f"INICIO CLIENTE {indice}")

        bytes_imagen = bytes()

        numero_bytes = conexion_cliente.recv(4)

        numero_bytes = int.from_bytes(numero_bytes, "big")

        print(f"{indice} -> Tamaño de la imagen que se va a recibir: {numero_bytes}")

        numero_bytes_recibidos = 0

        while numero_bytes_recibidos < numero_bytes: 

            bytes_imagen += conexion_cliente.recv(numero_bytes)

            numero_bytes_recibidos = len(bytes_imagen)

            print(f"{indice} -> Numero de bytes que conforman la imagen: {numero_bytes_recibidos}")

        conexion_cliente.sendall(bytes_imagen)

        conexion_cliente.close()

        print(f"FIN CLIENTE {indice}")


    def escuchar_clientes(self):

        try:

            indice = 0

            while True:

                conexion_cliente, direccion_puerto_cliente = self.accept()


                hilo_conexion = threading.Thread(target=self.atender_cliente, args=(indice, conexion_cliente, direccion_puerto_cliente))

                hilo_conexion.start()


                indice += 1

        except KeyboardInterrupt:

            pass


        finally:

            self.close()


