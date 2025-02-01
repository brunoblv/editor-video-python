from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

from moviepy.config import change_settings

# Caminho do ImageMagick (verifique se está correto)
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"})

# Função para criar um lower third com texto animado
def lower_third(texto, posicao, clip_duracao, largura_retangulo=800, altura_retangulo=150):
    # Criando o retângulo de fundo (semi-transparente)
    fundo = ColorClip(size=(largura_retangulo, altura_retangulo), color=(0, 0, 0), duration=clip_duracao)
    fundo = fundo.set_opacity(0.6)  # Opacidade do fundo

    # Criando o texto
    texto_clip = TextClip(texto, fontsize=40, color='white', font='Arial-Bold', size=(largura_retangulo, 50))
    texto_clip = texto_clip.set_duration(clip_duracao).set_position(('center', 'bottom'))

    # Animação de deslizar para cima
    fundo = fundo.set_position(('center', posicao)).crossfadein(1)  # Fade-in no início
    texto_clip = texto_clip.set_position(("center", posicao)).crossfadein(1)

    # Retornando o composite com fundo e texto
    return CompositeVideoClip([fundo, texto_clip])

# Exemplo de uso
clip_duracao = 5  # Duração do lower third
texto = "Shape of You - #1"
lower_third_clip = lower_third(texto, 'bottom', clip_duracao)

# Agora você pode combinar esse lower third com seu clipe principal
# clip_final = CompositeVideoClip([clip_principal, lower_third_clip])