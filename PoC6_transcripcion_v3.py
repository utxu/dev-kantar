import os
import time
import json
from datetime import datetime
import whisper

# README:
# En este caso, es igual a la versión v2, con la novedad de que si no encuentra 
# nuevos archivos, se detiene el script de transcripción:

def esperar_a_completarse(ruta_archivo, intervalo=5, intentos=3):
    """
    Espera a que un archivo deje de cambiar de tamaño, lo que indica que está completo.
    
    :param ruta_archivo: Ruta del archivo a comprobar.
    :param intervalo: Tiempo en segundos entre cada comprobación.
    :param intentos: Número de intentos consecutivos para verificar que el tamaño no cambia.
    :return: True si el archivo está completo, False si falla después de los intentos.
    """
    intentos_restantes = intentos
    tamaño_anterior = -1

    while intentos_restantes > 0:
        tamaño_actual = os.path.getsize(ruta_archivo)
        if tamaño_actual == tamaño_anterior:
            intentos_restantes -= 1
        else:
            intentos_restantes = intentos  # Reinicia los intentos si el tamaño cambia
        tamaño_anterior = tamaño_actual
        time.sleep(intervalo)

    return intentos_restantes == 0

def transcribir_audio(carpeta_entrada, carpeta_salida, intervalo=10, duracion_fragmento=60, intentos_para_salir=3):
    """
    Transcribe fragmentos de audio en una carpeta utilizando Whisper y guarda las transcripciones en JSON en formato específico.
    Se detiene si no encuentra nuevos archivos después de un número de intentos consecutivos.
    
    :param carpeta_entrada: Carpeta donde se almacenan los fragmentos de audio.
    :param carpeta_salida: Carpeta donde se guardarán los archivos JSON de las transcripciones.
    :param intervalo: Intervalo de tiempo en segundos para buscar nuevos archivos.
    :param duracion_fragmento: Duración de cada fragmento de audio en segundos.
    :param intentos_para_salir: Número de intentos consecutivos sin archivos nuevos antes de detenerse.
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Cargar modelo Whisper
    print("Cargando modelo Whisper...")
    modelo = whisper.load_model("base")  # Puedes usar "tiny", "base", "small", etc., según tus necesidades

    procesados = set()
    intentos_sin_archivos = 0

    try:
        while intentos_sin_archivos < intentos_para_salir:
            archivos_audio = [f for f in os.listdir(carpeta_entrada) if f.endswith(".wav")]
            nuevos_archivos = [archivo for archivo in archivos_audio if os.path.join(carpeta_entrada, archivo) not in procesados]
            
            if not nuevos_archivos:
                intentos_sin_archivos += 1
                print(f"No se encontraron nuevos archivos. Intento {intentos_sin_archivos}/{intentos_para_salir}.")
                time.sleep(intervalo)
                continue
            
            # Reiniciar el contador si se encuentran nuevos archivos
            intentos_sin_archivos = 0

            for archivo in nuevos_archivos:
                ruta_audio = os.path.join(carpeta_entrada, archivo)
                
                # Esperar a que el archivo esté completo
                print(f"Esperando a que el archivo esté completo: {ruta_audio}")
                if not esperar_a_completarse(ruta_audio):
                    print(f"El archivo {ruta_audio} no se completó correctamente. Ignorando.")
                    continue

                print(f"Procesando: {ruta_audio}")
                resultado = modelo.transcribe(ruta_audio, language="es", word_timestamps=True)

                # Extraer transcripción segmentada
                transcripcion = [
                    {"timestamp": segmento["start"], "text": segmento["text"]}
                    for segmento in resultado["segments"]
                ]

                # Preparar datos para guardar en formato compatible
                timestamp_inicio = os.path.splitext(archivo)[0].split("_")[1]  # Extraer timestamp del nombre
                metadata = {
                    "archivo_audio": archivo,
                    "timestamp_inicio": timestamp_inicio,
                    "duracion_fragmento": duracion_fragmento
                }

                datos_guardar = {
                    "metadata": metadata,
                    "transcription": transcripcion
                }

                # Guardar transcripción en archivo JSON
                nombre_base = os.path.splitext(archivo)[0]
                ruta_json = os.path.join(carpeta_salida, f"{nombre_base}.json")
                with open(ruta_json, "w", encoding="utf-8") as archivo_json:
                    json.dump(datos_guardar, archivo_json, ensure_ascii=False, indent=4)

                print(f"Transcripción guardada en: {ruta_json}")
                procesados.add(ruta_audio)

            print(f"Esperando {intervalo} segundos antes de buscar nuevos archivos...")
            time.sleep(intervalo)

        print("No se encontraron archivos nuevos después de múltiples intentos. Finalizando proceso.")
    except KeyboardInterrupt:
        print("Procesamiento detenido manualmente.")
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    carpeta_entrada = "grabaciones"  # Carpeta donde el primer script guarda los fragmentos de audio
    carpeta_salida = "transcripciones"  # Carpeta donde se guardarán los archivos JSON
    transcribir_audio(carpeta_entrada, carpeta_salida, intervalo=20, intentos_para_salir=4)
