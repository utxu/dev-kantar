import os
import time
import json
from datetime import datetime
import whisper

def transcribir_audio(carpeta_entrada, carpeta_salida, intervalo=10, duracion_fragmento=60):
    """
    Transcribe fragmentos de audio en una carpeta utilizando Whisper y guarda las transcripciones en JSON en formato específico.
    
    :param carpeta_entrada: Carpeta donde se almacenan los fragmentos de audio.
    :param carpeta_salida: Carpeta donde se guardarán los archivos JSON de las transcripciones.
    :param intervalo: Intervalo de tiempo en segundos para buscar nuevos archivos.
    :param duracion_fragmento: Duración de cada fragmento de audio en segundos.
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Cargar modelo Whisper
    print("Cargando modelo Whisper...")
    modelo = whisper.load_model("base")  # Puedes usar "tiny", "base", "small", etc., según tus necesidades

    procesados = set()

    try:
        while True:
            archivos_audio = [f for f in os.listdir(carpeta_entrada) if f.endswith(".wav")]
            
            for archivo in archivos_audio:
                ruta_audio = os.path.join(carpeta_entrada, archivo)
                
                # Verificar si ya fue procesado
                if ruta_audio in procesados:
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

    except KeyboardInterrupt:
        print("Procesamiento detenido manualmente.")
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    carpeta_entrada = "grabaciones"  # Carpeta donde el primer script guarda los fragmentos de audio
    carpeta_salida = "transcripciones"  # Carpeta donde se guardarán los archivos JSON
    transcribir_audio(carpeta_entrada, carpeta_salida, intervalo=80)

