import os
import subprocess
import time
from datetime import datetime

def grabar_audio_segmentado(duracion_segmento=10, duracion_total=60, carpeta_salida="grabaciones"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    tiempo_inicial = time.time()
    while time.time() - tiempo_inicial < duracion_total:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.join(carpeta_salida, f"audio_{timestamp}.wav")
        comando = [
            "ffmpeg",
            "-f", "dshow",
            "-i", "audio=Stereo Mix (Realtek(R) Audio)",
            "-t", str(duracion_segmento),
            "-y", nombre_archivo
        ]
        print(f"Grabando segmento: {nombre_archivo}")
        subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Grabación completada.")

if __name__ == "__main__":
    grabar_audio_segmentado(duracion_segmento=60, duracion_total=180)  #5 minutos
