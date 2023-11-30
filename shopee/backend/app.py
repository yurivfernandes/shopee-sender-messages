from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pyautogui
import time
from flask_cors import CORS
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

app = Flask(__name__)
CORS(app)

# Retorna um dataframe de uma planilha do Google Sheets
def get_GSheet(sheet_id, json_path, aba):
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    credentials = Credentials.from_service_account_file(json_path, scopes=scope)
    gc = gspread.authorize(credentials)
    spreadsheet_key = sheet_id
    try:
        worksheet = gc.open_by_key(spreadsheet_key).worksheet(aba)
        table = worksheet.get_all_values()
        df = pd.DataFrame(table[1:], columns=table[0])
        return df
    except gspread.exceptions.APIError as e:
        print("Erro ao acessar a planilha:", e)
        return None

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
        
        pyautogui.press("enter")

    except Exception as e:
        print("Ocorreu um erro ao enviar a mensagem:", e)

    finally:
        # Fechar o navegador após enviar a mensagem, independentemente do resultado
        driver.quit()

def get_user_input():
    data = request.get_json()
    sheet_id = data.get('sheet_id', '')
    aba = data.get('aba', '')
    col_link = data.get('col_link', '')

    return sheet_id, aba, col_link

@app.route('/', methods=['GET', 'POST'])
def index():
    sheet_id = ""
    aba = ""
    col_link = ""

    if request.method == 'POST':
        try:
            # Obter o caminho absoluto do diretório atual
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Caminho para o arquivo JSON de credenciais da API do Google Sheets (json_api_whatsapp.json)
            json_filename = "json_api_whatsapp.json"
            json_path = os.path.join(current_directory, json_filename)
            sheet_id, aba, col_link = get_user_input()

            # Verificar se a planilha, a aba e a coluna existem
            df = get_GSheet(sheet_id, json_path, aba)
            if df is None:
                return jsonify({'error': 'Planilha ou aba não encontrada'}), 400
            if col_link not in df.columns:
                return jsonify({'error': 'Coluna não encontrada'}), 400

            # Enviar as mensagens usando os links da coluna especificada pelo usuário
            for link in df[col_link]:
                send_whatsapp_message(link)

            return "Mensagem enviada com sucesso!"
        
        except Exception as e:
            print("Ocorreu um erro ao enviar a mensagem:", e)
            return "Erro ao enviar a mensagem!"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)