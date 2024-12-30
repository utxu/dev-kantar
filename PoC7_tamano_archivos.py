
import os
import time


def monitorear_archivos_carpeta(carpeta, intervalo=1):
    """
    Monitorea continuamente los tamaños de los archivos en una carpeta.
    
    :param carpeta: Carpeta donde se encuentran los archivos a monitorear.
    :param intervalo: Intervalo en segundos entre cada comprobación.
    """
    archivos_previos = {}

    print(f"Monitoreando la carpeta: {carpeta}")
    try:
        while True:
            archivos_actuales = os.listdir(carpeta)
            for archivo in archivos_actuales:
                ruta_archivo = os.path.join(carpeta, archivo)

                # Verifica si es un archivo y no un directorio
                if os.path.isfile(ruta_archivo):
                    tamaño_actual = os.path.getsize(ruta_archivo)
                    tamaño_anterior = archivos_previos.get(archivo, -1)

                    if tamaño_actual != tamaño_anterior:
                        print(f"Archivo: {archivo}, Tamaño actual: {tamaño_actual} bytes")
                        archivos_previos[archivo] = tamaño_actual
                    else:
                        print(f"Archivo: {archivo}, el tamaño no ha cambiado.")

            # Eliminar archivos eliminados de la lista de seguimiento
            archivos_previos = {
                archivo: tamaño
                for archivo, tamaño in archivos_previos.items()
                if archivo in archivos_actuales
            }

            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("Monitoreo detenido manualmente.")
    except Exception as e:
        print(f"Error durante el monitoreo: {e}")

if __name__ == "__main__":
    carpeta = "grabaciones"  # Cambia esto si tu carpeta tiene otro nombre
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe.")
    else:
        monitorear_archivos_carpeta(carpeta)
