from biblioteca_servidor.SocketServidor import SocketServidor


if __name__ == "__main__":

    servidor = SocketServidor('127.0.0.1', 9000)

    servidor.iniciar_servidor()

    servidor.escuchar_clientes()
