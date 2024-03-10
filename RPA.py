#Programa para automatizar a busca de mensagens no whatsapp e
#passar essas informações para uma planilha no google sheets

#Conquista para ser implementada na GYMBRO:
#ir 5 vezes na semana
#ir 6 vezes na semana
#ir 7 vezes na semana
#ir um mes sem faltar nenhum dia
#ir 3 meses sem faltar nenhum dia
#ir 31 dias consecutivos
#Constancia (treinar uma semana no msm periodo do dia)
#Treinar em todos os periodo em uma msm semana
#

import pyautogui
import pygetwindow as gw
import webbrowser
import time
import sys

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import os


# Abra o navegador padrão com o URL
#webbrowser.open('https://web.whatsapp.com/')

# Aguarde o navegador abrir
time.sleep(10)              

# Mova o mouse para as coordenadas especificadas
pyautogui.moveTo(167, 284)  # Move o mouse durante um segundo
                        
# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)

# Escreva o texto da pesquisa
pyautogui.write("GymBro")

pyautogui.moveTo(284, 440)  # Move o mouse durante um segundo

time.sleep(1)

# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)

pyautogui.moveTo(800, 462)  # Move o mouse durante um segundo

# Defina o número de scrolls e a quantidade por scroll
numero_de_scrolls = 70
quantidade_por_scroll = 500  # Este valor pode precisar de ajustes

# Realiza o scroll para cima
for _ in range(numero_de_scrolls):
    pyautogui.scroll(quantidade_por_scroll)


pyautogui.moveTo(1907, 462)  # Move o mouse durante um segundo

pyautogui.click(button='right')

pyautogui.moveTo(1643, 615)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

pyautogui.moveTo(821, 887)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

num_backspaces = 20

# Simula pressionamentos de backspace
for i in range(num_backspaces):
    pyautogui.press('backspace')

# Escreva o texto da pesquisa
pyautogui.write(r"caminho/para/seu/arquivo.htm")

pyautogui.moveTo(1714, 980)  # Move o mouse durante um segundo
time.sleep(1)

# Clique no local
pyautogui.click()

pyautogui.moveTo(1028, 526)  # Move o mouse durante um segundo
time.sleep(1)

# Clique no local
pyautogui.click()


time.sleep(15)
# Encontrar a janela pelo título (parte do título é suficiente se for único)
vs_code_window = gw.getWindowsWithTitle('Visual Studio Code')[0]

# Traz a janela para o primeiro plano
vs_code_window.activate()
print("salvou")



def check_message_existence(html_content, name, date, tag):
    # Converte a data para o formato que aparece no atributo 'data-pre-plain-text'
    date_pattern = f"{date.strftime('%d/%m/%Y')}"
    tag_lower = tag.lower()  # Transforma a tag em minúsculas

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the message details in the parsed HTML
    message_details = soup.find_all('div', {'class': 'copyable-text'})
    
    # Check each message for the specified name, date, and tag
    for detail in message_details:
        # Check if the 'data-pre-plain-text' attribute contains the name and date
        pre_text = detail.get('data-pre-plain-text', '')
        if name in pre_text and re.search(date_pattern, pre_text):
            print(name)
            # Check if the message contains a 'span' with 'data-icon'
            if detail.find('span', {'data-icon': True}):
                # If so, check for the tag in the entire message
                message_text = detail.get_text().lower()
                print("data-icon")
                if tag_lower in message_text:  # Procura a tag em qualquer lugar do texto da mensagem
                    print("achou")
                    # Se a tag for encontrada, procure pela div com a classe 'gq1t1y46 o38k74y6 e4p1bexh cr2cog7z le5p0ye3 p357zi0d gndfcl4n'
                    special_div = detail.find('div', {'class': 'gq1t1y46 o38k74y6 e4p1bexh cr2cog7z le5p0ye3 p357zi0d gndfcl4n'})
                    if special_div:
                        return 1
                

            # Check for the tag in the alt attribute of each image
            images = detail.find_all('img')
            for image in images:
                alt_text = image.get('alt', '').lower()
                if tag_lower in alt_text:  # Procura a tag em qualquer lugar do texto alternativo da imagem
                    print("achou")
                    # Se a tag for encontrada, procure pela div com a classe 'gq1t1y46 o38k74y6 e4p1bexh cr2cog7z le5p0ye3 p357zi0d gndfcl4n'
                    special_div = detail.find('div', {'class': 'gq1t1y46 o38k74y6 e4p1bexh cr2cog7z le5p0ye3 p357zi0d gndfcl4n'})
                    if special_div:
                        return 1
    
    return 0

def generate_date_range(start_from_last_monday=True):
    today = datetime.now()
    # Encontrar a última segunda-feira
    if start_from_last_monday:
        start_day = today - timedelta(days=today.weekday())
    else:
        start_day = today
    # Gerar o intervalo da semana a partir da última segunda-feira
    return [start_day + timedelta(days=x) for x in range(7)]

def generate_date_range_last(start_from_last_monday=True):
    today = datetime.now()
    # Encontrar a segunda-feira desta semana
    current_week_monday = today - timedelta(days=today.weekday())
    
    # Se start_from_last_monday for True, subtrair uma semana para encontrar a segunda-feira da semana passada
    if start_from_last_monday:
        start_day = current_week_monday - timedelta(days=7)
    else:
        start_day = current_week_monday
    
    # Gerar o intervalo da semana a partir da segunda-feira encontrada
    return [start_day + timedelta(days=x) for x in range(7)]

# Função para verificar a existência da mensagem para cada nome na lista
#def check_messages_for_all_names(html_content, names, date, tag):
#    results = {}
#    for name in names:
#        message_exists = check_message_existence(html_content, name, date, tag)
#        results[name] = message_exists
#    return results


# Exemplo de uso:
# Substitua 'caminho/para/seu/arquivo.htm' pelo caminho correto do seu arquivo .htm.
with open(r'caminho/para/seu/arquivo.htm', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Valores de exemplo para data e tag
# Lista de nomes
names = ["A", "Ar", "Fer", "Gus", "Hug", "Mic", "Thi"]
#date = datetime.now().strftime("%d/%m/%Y")  # A data específica a ser procurada na mensagem, sem horário
tag = "#fui"  # A tag específica a ser verificada na imagem
date_range = generate_date_range_last()

data = {date.strftime("%d/%m"): [] for date in date_range}

# Preenche o dicionário com os dados
for date in date_range:
    formatted_date = date.strftime("%d/%m")
    for name in names:
        message_exists = check_message_existence(html_content, name, date, tag)
        data[formatted_date].append(message_exists)

# Criando o DataFrame
df = pd.DataFrame(data, index=names)
print(df)


array_numpy = df.values
df1 = pd.DataFrame(array_numpy)


current_directory = os.getcwd()

# Define o nome do arquivo CSV
csv_file_name = 'resultados_mensagens.csv'

# Combina o diretório atual com o nome do arquivo para criar o caminho completo
csv_file_path = os.path.join(current_directory, csv_file_name)

# Salva o DataFrame em um arquivo CSV no diretório atual
df1.to_csv(csv_file_path, index=False, header=False)

print(f"DataFrame salvo com sucesso em: {csv_file_path}")

time.sleep(5)
print("salvou")

# Abra o navegador padrão com o URL
webbrowser.open('https://docs.google.com')

# Aguarde o navegador abrir
time.sleep(5)              

# Mova o mouse para as coordenadas especificadas
pyautogui.moveTo(355, 458)  # Move o mouse durante um segundo
                        
# Clique no local
pyautogui.click()
time.sleep(2)              

# Mova o mouse para as coordenadas especificadas
pyautogui.moveTo(88, 194)  # Move o mouse durante um segundo
                        
# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)

pyautogui.moveTo(174, 314)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)


pyautogui.moveTo(1079, 334)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)

pyautogui.moveTo(954, 739)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

# Aguarde um momento para a página responder
time.sleep(1)


pyautogui.moveTo(889, 938)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

# Escreva o texto da pesquisa
pyautogui.write(r"caminho/para/seu/arquivo.htm")

pyautogui.moveTo(1699, 979)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

time.sleep(5)


pyautogui.moveTo(765, 600)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()


pyautogui.moveTo(788, 791)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()


pyautogui.moveTo(1000, 820)  # Move o mouse durante um segundo

# Clique no local
pyautogui.click()

time.sleep(5)

# Mover o cursor para a posição inicial
pyautogui.moveTo(58, 338)

# Pressiona e solta a combinação de teclas 'Win' + 'Shift' + 'S'
pyautogui.hotkey('win', 'shift', 's')

# Espera um momento para a ferramenta de recorte abrir
time.sleep(1)  # Ajuste este tempo conforme necessário

# Clicar e segurar o botão do mouse na posição inicial
pyautogui.mouseDown()

# Mover o cursor para a posição final, mantendo o botão do mouse pressionado
pyautogui.moveTo(1064, 788)  # Ajuste a duração conforme necessário

time.sleep(1) 

# Soltar o botão do mouse na posição final
pyautogui.mouseUp()

time.sleep(1) 

pyautogui.hotkey('ctrl', 'tab')

time.sleep(1) 

pyautogui.hotkey('ctrl', 'v')

# Aguarda um breve momento para a ação de colar ser concluída
time.sleep(0.5)

# Digita a mensagem "conferem ai rapazeada"
pyautogui.write("conferem ai rapazeada!!!", interval=0.05)

# Aguarda um breve momento para terminar a digitação
time.sleep(0.5)

# Pressiona Enter para enviar a mensagem
#pyautogui.press('enter')