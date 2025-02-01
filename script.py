import os
import csv
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy.config import change_settings

# Caminho do ImageMagick (verifique se está correto)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"})

# Lê os dados do CSV
musicas = []
with open("musicas.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  
    for row in reader:
        musicas.append({
            "posicao": int(row["posicao"]),
            "titulo": row["titulo"],  
            "arquivo": row["arquivo"],
            "cortes": [row["corte1"], row["corte2"], row["corte3"]],
            "semanas": row["semanas"],
            "status": row["status"],
            "pico": row["pico"]
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

    # Carrega o vídeo e define o corte (16s de duração)
    clip = VideoFileClip(musica["arquivo"]).subclip(inicio, inicio + 16)

    # Define dimensões do vídeo
    largura_video, altura_video = clip.size

    # 🔹 Criando FUNDO TRANSPARENTE para a posição
    largura_pos = 100
    altura_pos = 100
    posicao_fundo = ColorClip(size=(largura_pos, altura_pos), color=(0, 0, 0), duration=clip.duration)
    posicao_fundo = posicao_fundo.fl_image(lambda img: (img * 0.6).astype('uint8'))  # 60% de opacidade
    posicao_fundo = posicao_fundo.set_position(('left', 'top'))

    # Texto da posição dentro do quadrado
    texto_posicao = TextClip(
        f"{musica['posicao']}", 
        fontsize=70, 
        color='white', 
        font='Arial-Bold',
        size=(largura_pos, altura_pos)
    ).set_position(('left', 'top')).set_duration(clip.duration)

    # 🔹 Criando RETÂNGULO TRANSPARENTE no rodapé
    altura_retangulo = 120  
    largura_retangulo = largura_video  

    retangulo = ColorClip(size=(largura_retangulo, altura_retangulo), color=(0, 0, 0), duration=clip.duration)
    retangulo = retangulo.fl_image(lambda img: (img * 0.6).astype('uint8'))  # 60% de opacidade
    retangulo = retangulo.set_position(("center", altura_video - altura_retangulo))

    # Texto do nome da música
    texto_titulo = TextClip(
        f"{musica['titulo']}",  
        fontsize=50, 
        color='white', 
        font='Arial-Bold',
        size=(largura_retangulo, 50)
    ).set_position(("center", altura_video - altura_retangulo + 10)).set_duration(clip.duration)

    # Texto com as informações adicionais (Semanas, Status, Pico), logo abaixo do título
    texto_info = TextClip(
        f"Semanas: {musica['semanas']} | {musica['status']} | Pico: {musica['pico']}", 
        fontsize=40, 
        color='white', 
        font='Arial-Bold',
        size=(largura_retangulo, 40)
    ).set_position(("center", altura_video - altura_retangulo + 60)).set_duration(clip.duration)

    # Combina o vídeo com os elementos visuais
    video_com_texto = CompositeVideoClip([clip, posicao_fundo, texto_posicao, retangulo, texto_titulo, texto_info])

    # Aplica efeito de fade
    video_com_texto = video_com_texto.fadein(1).fadeout(1)

    # Adiciona o clip à lista
    clips.append(video_com_texto)

# Concatena os clipes
video_final = concatenate_videoclips(clips, method="compose")
video_final.write_videofile("output/parada_musical.mp4", fps=24)

print("Vídeo final gerado com sucesso!")
