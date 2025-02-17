
from biblioteca_cliente.ConexionCliente import ConexionCliente

import threading

def crear_cliente(indice):

        print(f"Cliente {indice}")

        cliente = ConexionCliente('127.0.0.1', 9000, 'imagenes/1.png') 

        cliente.cargar_imagen()

        cliente.establecer_conexion()

        cliente.enviar_imagen()

        cliente.recibir_imagen_procesada()

        cliente.close()



if __name__ == "__main__":

    for indice in range(2):

        hilo_cliente = threading.Thread(target=crear_cliente, args=(indice,))

        hilo_cliente.start()
