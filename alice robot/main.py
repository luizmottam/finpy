import smtplib
from email.message import EmailMessage

def enviar_email():
    remetente = ''
    destinatario = ''
    assunto = 'Teste'
    mensagem = 'Olá, isso é um teste'
    senha = ''
    
    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.set_content(mensagem)
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 587) as email:
        email.login(remetente, senha)
        email.send_message(msg)
        
    print('Email enviado com sucesso')

enviar_email()
