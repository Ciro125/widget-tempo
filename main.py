import tkinter as tk
from tkinter import Label, Button
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

def obter_localizacao_por_ip():
    try:
        # Obter o endereço IP público
        resposta = requests.get('https://ipinfo.io')
        dados = resposta.json()

        # Obter a cidade a partir dos dados de localização
        cidade = dados.get('city', 'Cidade Desconhecida')
        return cidade
    except Exception as e:
        print(f"Erro ao obter localização por IP: {e}")
        return 'Cidade Desconhecida'

def obter_tempo():
    try:
        api_key = "1492f2c5fc894a6b99c183001231711"
        cidade = obter_localizacao_por_ip()
        linguagem = "pt"

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

        # Atualizar o rótulo de texto
        texto_tempo.config(text=f"{descricao}, {temperatura}°C\n{nome_cidade}")

        # Obter a hora local da cidade sem os segundos
        hora_local = datetime.now().strftime('%H:%M')

        # Atualizar o rótulo de texto com a hora
        texto_tempo.config(text=f"{descricao}, {temperatura}°C\n{nome_cidade}\nHora Local: {hora_local}")

        # Atualizar o ícone
        icone_label.config(image=icone)
        icone_label.image = icone

        # Agendar a próxima atualização após 5000 milissegundos (5 segundos)
        janela.after(5000, obter_tempo)
    except Exception as e:
        print(f"Erro ao obter tempo: {e}")
        # Se houver um erro, tentar novamente após 5000 milissegundos
        janela.after(5000, obter_tempo)

# Configuração da janela principal
janela = tk.Tk()
janela.title("Widget de Tempo")

# Defina o tamanho da janela (largura x altura) e a posição inicial
janela.geometry("500x300")  # Ajuste conforme necessário

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
botao_atualizar.pack(pady=20)  # Ajuste conforme necessário

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
