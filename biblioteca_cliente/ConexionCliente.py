import socket

import os

import re

class ConexionCliente(socket.socket):

    
    regex = re.compile("^([0-9]{1,3}\\.){1,3}[0-9]{1,3}$")


    def __init__(self, direccion_IPv4_servidor, puerto_servidor, ruta_imagen):


        super().__init__(socket.AF_INET, socket.SOCK_STREAM)


        if not isinstance(direccion_IPv4_servidor, str):

            raise TypeError("La direccion IPv4 del servidor debe de ser especificada como un string.")

        elif ConexionCliente.regex.match(direccion_IPv4_servidor) == None:

            raise ValueError("La direccion IP proporcionada debe de ser una direccion IPv4.")

        elif not isinstance(puerto_servidor, int):

            raise TypeError("El puerto del servidor debe de ser especifico como un entero")

        elif not 1 <= puerto_servidor <= 65535:

            raise ValueError("El valor del puerto TCP del servidor solo puede estar en el rango de [1, 65535]")

        elif not isinstance(ruta_imagen, str):

            raise TypeError("La ruta de la imagen debe de ser especificada como un string.")

        elif not os.path.exists(ruta_imagen):

            raise ValueError("La ruta especificada no existen dentro del sistema de archivo del sistema.")

        elif not os.path.isfile(ruta_imagen):

            raise ValueError("La ruta especificada no hace referencia a un archivo.")

        else:

            octetos = direccion_IPv4_servidor.split(".")

            for octeto in octetos:

                if int(octeto) > 255:

                    raise ValueError("Los octetos de la direccion IPv4 no pueden ser mayores a 255.")


        self.datos_conexion = (direccion_IPv4_servidor, puerto_servidor)

        self.ruta_imagen = ruta_imagen

        self.bytes_imagen = None

        self.numero_bytes_imagen = None

    
    def cargar_imagen(self):

        with open(self.ruta_imagen, "rb") as fichero_imagen:

            self.bytes_imagen = fichero_imagen.read()

            self.numero_bytes_imagen = len(self.bytes_imagen)

        print(f"Numeros de bytes que tiene la imagen, {self.numero_bytes_imagen}")


    def establecer_conexion(self):

        self.connect(self.datos_conexion)


    def enviar_imagen(self):

        #Se podran enviar imagen de maximo 2^32 bits.

        if self.bytes_imagen != None and self.numero_bytes_imagen != None:

            #Debido a que solo se pueden enviar imagen con un tamaño maximo de 2^32 bits, todos los posibles tamaños de imagen se pueden
            #representar mediante 4 bytes. Por ende, los primeros 4 bytes que enviaremos al servidor indicaran el tamaño en bytes de la
            #imagen que sera enviada posterior a eso.

            
            #Representamos de manera binaria el tamaño de la imagen en un maximo de 4 bytes, con un formto Big Endian.

            dimension_imagen = self.numero_bytes_imagen.to_bytes(4, "big")

            #La razon del uso de la representacion Big Endian se sustenta en que el protocolo TCP específica de manera rigurosa
            #que la transferencia de datos que sean integrados en multiples bytes debe de realizarse en este tipo de endianess.

            
            #Enviamos los primeros 4 bytes al servidor indicandole el tamaño de la imagen que recibira inmediatamente despues.

            self.sendall(dimension_imagen)

            #Enviamos todos los bytes que conforman al servidor para su procesamiento.

            print("Inciando")

            resultado = self.sendall(self.bytes_imagen)


            print("Finalizado envio")


            print(f"Numero de bytes transferidos: {len(self.bytes_imagen)}", resultado)


    def recibir_imagen_procesada(self):

        bytes_nueva_imagen = bytes()

        bytes_recibidos = 0

        while bytes_recibidos < self.numero_bytes_imagen:

            bytes_nueva_imagen += self.recv(self.numero_bytes_imagen)

            bytes_recibidos = len(bytes_nueva_imagen)

            print(f"Bytes recibidos desde el servidor: {bytes_recibidos}")


    def guardar_imagen_procesada(self, bytes_nueva_imagen):

        with open(self.ruta_imagen + ".mod", "wb") as nueva_imagen:

            nueva_imagen.write(bytes_nueva_imagen)


    def cerrar_conexion(self):


        self.close()
