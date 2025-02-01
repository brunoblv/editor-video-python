import os
import csv
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.config import change_settings
# Caminho do ImageMagick (verifique se está correto)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"})

# Lê os dados do CSV
musicas = []
with open("musicas.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # Especifica o delimitador como ';'
    for row in reader:
        musicas.append({
            "posicao": int(row["posicao"]),
            "titulo": row["titulo"],
            "arquivo": row["arquivo"],
            "cortes": [row["corte1"], row["corte2"], row["corte3"]]
        })

# Lista de trechos de vídeo
clips = []

def converter_tempo(tempo_str):
    """Converte 'MM:SS' para segundos"""
    minutos, segundos = map(int, tempo_str.split(":"))
    return minutos * 60 + segundos

for musica in musicas:
    # Escolhe um corte aleatório
    corte_escolhido = random.choice(musica["cortes"])
    inicio = converter_tempo(corte_escolhido)

    # Carrega o vídeo e define o corte (10s de duração)
    clip = VideoFileClip(musica["arquivo"]).subclip(inicio, inicio + 16)

    # Adiciona texto com posição e título
    texto = TextClip(
        f"{musica['posicao']}. {musica['titulo']}", 
        fontsize=50, 
        color='white', 
        font='Arial-Bold',
        size=(clip.size[0], 50)
    ).set_position(('center', 'top')).set_duration(clip.duration)

    # Aplica efeito de fade
    clip = clip.fadein(1).fadeout(1)

    # Combina vídeo com texto
    video_com_texto = CompositeVideoClip([clip, texto])

    clips.append(video_com_texto)

# Concatena e salva
video_final = concatenate_videoclips(clips)
video_final.write_videofile("output/parada_musical.mp4", fps=24)

print("Vídeo final gerado com sucesso!")