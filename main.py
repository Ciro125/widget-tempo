import tkinter as tk
from tkinter import Label, Button
import requests
from PIL import Image, ImageTk
from io import BytesIO

def obter_tempo():
    api_key = "1492f2c5fc894a6b99c183001231711"
    cidade = "rio de janeiro"
    linguagem = "pt"
    lon = -43.2075
    lat = -22.9028

    link = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={cidade}&lang={linguagem}&aqi=no"
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    descricao = requisicao_dic['current']['condition']['text']
    temperatura = requisicao_dic['current']['temp_c']
    nome_cidade = requisicao_dic['location']['name']

    # Baixar o ícone da URL
    response = requests.get(f"http:{requisicao_dic['current']['condition']['icon']}")
    img = Image.open(BytesIO(response.content))
    icone = ImageTk.PhotoImage(img)

    # Exibir o ícone
    icone_label.config(image=icone)
    icone_label.image = icone

    # Atualizar o rótulo de texto
    texto_tempo.config(text=f"{descricao}, {temperatura}°C\n{nome_cidade}")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Widget de Tempo")

# Defina o tamanho da janela (largura x altura) e a posição inicial
janela.geometry("400x250")  # Largura x Altura + Posição X + Posição Y

# Adiciona um ícone à janela
caminho_icone = r'imagens\icone.ico'
icone = ImageTk.PhotoImage(Image.open(caminho_icone))
janela.iconphoto(True, icone)

# Configuração do rótulo para exibir o ícone
icone_label = Label(janela)
icone_label.pack()

# Configuração do rótulo para exibir o tempo
texto_tempo = Label(janela, font=("Arial", 18, "bold"), pady=20, fg="#333")
texto_tempo.pack()

# Botão para atualizar o tempo
botao_atualizar = Button(janela, text="Atualizar Tempo", command=obter_tempo, font=("Arial", 12), bg="#4CAF50", fg="white", bd=2, relief="groove")
botao_atualizar.pack(pady=20)  # Ajuste o valor de pady conforme necessário

# Configuração de cor de fundo
janela.configure(bg='#e6e6e6')
icone_label.configure(bg='#e6e6e6')
texto_tempo.configure(bg='#e6e6e6')

# Defina a opacidade da janela (0.9 significa 90% opaca)
janela.attributes('-alpha', 0.9)

# Inicializa o tempo quando a janela é aberta
obter_tempo()

# Inicia o loop principal da interface gráfica
janela.mainloop()
