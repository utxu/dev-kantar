import os
import datetime
import subprocess

def grabar_audio_por_tiempo(carpeta_salida, duracion_total, duracion_fragmento=60):
    """
    Graba audio continuamente durante un tiempo total específico, dividiéndolo en fragmentos.
    
    :param carpeta_salida: Carpeta donde se almacenarán los archivos de audio.
    :param duracion_total: Tiempo total de grabación en segundos.
    :param duracion_fragmento: Duración de cada fragmento de audio en segundos (predeterminado: 60).
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    print(f"Grabación iniciada. Tiempo total: {duracion_total} segundos. Fragmentos: {duracion_fragmento} segundos.")
    timestamp_inicial = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    # Comando FFmpeg base
    comando_base = [
        "ffmpeg",
        "-f", "dshow",  # Para Windows (modifica según tu sistema operativo)
        "-i", "audio=Stereo Mix (Realtek High Definition Audio)",  # Dispositivo de entrada
        "-f", "segment",  # Modo de segmentos
        "-segment_time", str(duracion_fragmento),  # Duración de cada segmento
        "-c:a", "pcm_s16le",  # Formato de audio sin comprimir (WAV)
    ]

    # Calcula el número de fragmentos que se necesitan
    numero_fragmentos = duracion_total // duracion_fragmento

    try:
        for i in range(numero_fragmentos):
            nombre_fragmento = os.path.join(carpeta_salida, f"{timestamp_inicial}_fragmento_{i:03d}.wav")
            comando = comando_base + ["-t", str(duracion_fragmento), nombre_fragmento]
            
            print(f"Grabando fragmento {i+1}/{numero_fragmentos}: {nombre_fragmento}")
            subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except KeyboardInterrupt:
        print("Grabación detenida manualmente.")
    except Exception as e:
        print(f"Error durante la grabación: {e}")

    print("Grabación completada.")

if __name__ == "__main__":
    carpeta_salida = "grabaciones"
    duracion_total = 10 * 60  # Total de grabación: 10 minutos
    duracion_fragmento = 60  # Duración de cada fragmento: 1 minuto
    grabar_audio_por_tiempo(carpeta_salida, duracion_total, duracion_fragmento)
