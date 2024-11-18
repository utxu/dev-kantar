
import os
import whisper

audio_path = "C:/Users/34676/Desktop/dev_projects/dev_kantar/video_largo1.mp3"  # Cambia esto por la ruta correcta de tu archivo

if os.path.exists(audio_path):
    print("El archivo existe. Iniciando transcripción...")
    modelo = whisper.load_model("base")
    resultado = modelo.transcribe(audio_path, language="es")
    texto_transcrito_largo = resultado["text"]
    print("Texto transcrito:\n", texto_transcrito_largo)
else:
    print("Archivo no encontrado. Verifica que la ruta y el nombre del archivo sean correctos.")

audio_path2 = "C:/Users/34676/Desktop/dev_projects/dev_kantar/video_corto1.mp3"
if os.path.exists(audio_path2):
    print("El archivo existe. Iniciando transcripción...")
    modelo = whisper.load_model("base")
    resultado = modelo.transcribe(audio_path2, language="es")
    texto_transcrito_corto = resultado["text"]
    print("Texto transcrito:\n", texto_transcrito_corto)
else:
    print("Archivo no encontrado. Verifica que la ruta y el nombre del archivo sean correctos.")


import hashlib

def generate_fingerprints(text, n=4):
    """
    Genera fingerprints a partir de n-grams de un texto.
    :param text: Texto de entrada
    :param n: Tamaño de los n-grams (por ejemplo, 4 para secuencias de 4 palabras)
    :return: Conjunto de fingerprints (hashes únicos) para los n-grams
    """
    words = text.split()
    fingerprints = set()
    
    # Genera n-grams y calcula un hash para cada uno
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i + n])
        fingerprint = hashlib.md5(ngram.encode()).hexdigest()
        fingerprints.add(fingerprint)
    
    return fingerprints


# Genera fingerprints
fingerprints_anuncio = generate_fingerprints(texto_transcrito_corto, n=3)
fingerprints_emision = generate_fingerprints(texto_transcrito_largo, n=3)

print(fingerprints_anuncio)
print(fingerprints_emision)
len(fingerprints_anuncio)
len(fingerprints_emision)

coincidencias = fingerprints_anuncio.intersection(fingerprints_emision)

if coincidencias:
    print("El anuncio parece estar en la emisión.")
else:
    print("No se detectaron coincidencias significativas.")


len(coincidencias)

fingerprints_comunes = fingerprints_anuncio & fingerprints_emision
num_coincidencias = len(fingerprints_comunes)
porcentaje_similitud = (num_coincidencias / len(fingerprints_anuncio)) * 100

# Resultados
print("Fingerprints comunes:", fingerprints_comunes)
print("Número total de coincidencias de fingerprints:", num_coincidencias)
print("Porcentaje de similitud:", porcentaje_similitud)

# Para conocer el texto que ha matcheado:
def generar_ngrams(texto, n):
    palabras = texto.split()
    ngrams = []
    for i in range(len(palabras) - n + 1):
        ngram = " ".join(palabras[i:i + n])
        hash_ngram = hashlib.md5(ngram.encode()).hexdigest()
        ngrams.append((hash_ngram, ngram, i))  # Guardamos el hash, n-grama y el índice
    return ngrams

# Generamos los n-gramas con sus posiciones
anuncio_ngrams_pos = generar_ngrams(texto_transcrito_corto, 3)
emision_ngrams_pos = generar_ngrams(texto_transcrito_largo, 3)

# Crear diccionarios para buscar coincidencias por hash
anuncio_hash_map_pos = {hash_val: (ngram, idx) for hash_val, ngram, idx in anuncio_ngrams_pos}
emision_hash_map_pos = {hash_val: (ngram, idx) for hash_val, ngram, idx in emision_ngrams_pos}

# Encontrar coincidencias
coincidencias_pos = set(anuncio_hash_map_pos.keys()).intersection(emision_hash_map_pos.keys())

# Mostrar coincidencias con posición
for hash_value in coincidencias_pos:
    anuncio_ngram, anuncio_idx = anuncio_hash_map_pos[hash_value]
    emision_ngram, emision_idx = emision_hash_map_pos[hash_value]
    print(f"Hash: {hash_value}")
    print(f"Texto coincidente del anuncio: '{anuncio_ngram}' en posición {anuncio_idx}")
    print(f"Texto coincidente de la emisión: '{emision_ngram}' en posición {emision_idx}")


