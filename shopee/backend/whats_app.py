from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pyautogui
import pandas as pd
import time
import os
import pyperclip
import unicodedata
import gspread
from google.oauth2.service_account import Credentials

# Retorna um dataframe de uma planilha do Google Sheets
def get_GSheet(sheet_id, json_path, aba, col_link, line_header=0, line_values=1, sleep_time=5):
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    credentials = Credentials.from_service_account_file(json_path, scopes=scope)
    gc = gspread.authorize(credentials)
    spreadsheet_key = sheet_id
    book = gc.open_by_key(spreadsheet_key)
    time.sleep(sleep_time)
    worksheet = book.worksheet(aba)
    table = worksheet.get_all_values()
    df = pd.DataFrame(table[line_values:], columns=table[line_header])
    return df

# Função para enviar mensagens via WhatsApp
def send_whatsapp_message(link, timer=5):
    # Configurar o serviço do driver do Chrome
    service = Service()

    try:
        # Inicializar o navegador Chrome
        driver = webdriver.Chrome(service=service)
        driver.get(link)
        # Aguardar alguns segundos para a caixa de diálogo "Abrir WhatsApp" aparecer
        time.sleep(2)
        
        # Pressionar tecla de seta para a esquerda para evitar que a caixa de diálogo permaneça na frente
        pyautogui.press("left")
        pyautogui.press("enter")

        time.sleep(timer)
        # Pressionar a tecla Enter para enviar a mensagem
        pyautogui.press("enter")

        print("Mensagem enviada com sucesso!")

    except Exception as e:
        print("Ocorreu um erro ao enviar a mensagem:", e)

    finally:
        # Fechar o navegador após enviar a mensagem, independentemente do resultado
        driver.quit()

def get_user_input():
    # Solicitar ao usuário que informe o ID da planilha, o nome da aba, o nome da coluna dos links
    # e a mensagem a ser enviada via WhatsApp
    sheet_id = input("Informe o ID da planilha do Google Sheets: ")
    aba = input("Informe o nome da aba da planilha: ")
    col_link = input("Informe o nome da coluna onde estão os links: ")

    return sheet_id, aba, col_link

def main():
    # Obter o caminho absoluto do diretório atual
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Caminho para o arquivo JSON de credenciais da API do Google Sheets (json_api_whatsapp.json)
    json_filename = "json_api_whatsapp.json"
    json_path = os.path.join(current_directory, json_filename)

    # Obter informações do usuário
    sheet_id, aba, col_link= get_user_input()

    # Carregar os dados da planilha em um DataFrame
    df = get_GSheet(sheet_id=sheet_id, json_path=json_path, aba=aba, col_link=col_link)

    # Iterar sobre os links na coluna informada do DataFrame e enviar a mensagem para cada um
    for link in df[col_link]:
        send_whatsapp_message(link)

if __name__ == "__main__":
    main()