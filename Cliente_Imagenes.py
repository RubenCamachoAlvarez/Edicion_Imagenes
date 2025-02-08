#Este script de Python representa el cliente que enviara las imagenes al servidor para ser aclaradas.

import sys
import os

lista_argumentos = sys.argv

print(f"Numero de argumentos: {len(sys.argv)}", f"Lista de argumentos: {sys.argv}", sep="\n")

if len(lista_argumentos) > 2:

    print("Este script puede ser invocado con solo un argumento como maximo", file=sys.stderr)

    sys.exit(1)

else:

    # Si el script se ejecuta sin ningun argumento, entonces el directorio de trabajo sera el mismo directorio en el que se inicio la ejecucion del script.

    directorio_trabajo = "."

    if len(lista_argumentos) == 2 and  os.path.exists(lista_argumentos[1]) and os.path.isdir(lista_argumentos[1]):

        #Si el argumento representa una ruta valida a un directorio en el sistema de archivos, entonces asignamos la ruta del argumento como el directorio de trabajo.

        directorio_trabajo = lista_argumentos[1]

    with os.scandir(directorio_trabajo) as archivos:

        for archivo in archivos:

            if archivo.name.endswith(".png") and archivo.is_file():

                print(archivo.name)

        



