from time import sleep

def send_email_log(email: str, subject: str, message: str = ""):
    """
    Simula o envio de um email (operação demorada).
    """
    # Simula latência de rede
    sleep(2) 
    print(f"\n[EMAIL_SERVICE] Enviando email para: {email}")
    print(f"[EMAIL_SERVICE] Assunto: {subject}")
    print(f"[EMAIL_SERVICE] Mensagem: {message}")
    print("[EMAIL_SERVICE] Enviado com sucesso!\n")
