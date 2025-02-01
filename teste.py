from moviepy.editor import TextClip

try:
    texto = TextClip("Teste", fontsize=50, color="white")
    texto.save_frame("teste_texto.png", t=0)
    print("Texto gerado com sucesso!")
except Exception as e:
    print("Erro ao gerar texto:", e)
