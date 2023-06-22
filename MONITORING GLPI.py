import time
import requests
import smtplib
import urllib3

urllib3.disable_warnings()

#Infos de acesso
api_url = 'https://URL/glpi/apirest.php'
session_token = 'VERIFY GLPI DOC TO GENERATE THIS'
item_id = 456

#Destinatario
recipient_email = 'email@email.com.br'

#Infos do servidor de email
smtp_server = 'servidor.mail.com.br'
smtp_port = 587
smtp_username = 'mail@email.com.br'
smtp_password = 'password123'

#Codigo

last_date_mod = None

def get_knowledge_base_item():
    headers = {
        'Content-Type': 'application/json',
        'Session-Token': session_token
    }
    response = requests.get(f'{api_url}/KnowbaseItem/{item_id}', headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    return None

def send_email_notification():
    subject = 'Alteracao na base de conhecimento'
    body = f'O item da base de conhecimento com ID {item_id} foi modificado em {last_date_mod}.'
    msg = f'Subject: {subject}\n\n{body}'
    msg = msg.encode('utf-8')  # Usar a codificação UTF-8

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(smtp_username, recipient_email, msg)
    smtp.quit()

def monitor_knowledge_base_item():
    global last_date_mod

    while True:
        item_data = get_knowledge_base_item()
        if item_data is None:
            print(f'Erro ao obter informações do item da base de conhecimento com ID {item_id}')
            continue

        date_mod = item_data['date_mod']

        if last_date_mod is not None and last_date_mod != date_mod:
            last_date_mod = date_mod
            send_email_notification()
        else:
            last_date_mod = date_mod

        time.sleep(3600)  # Esperar 1 Hora

monitor_knowledge_base_item()