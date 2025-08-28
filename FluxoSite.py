import requests
import time
import random
import string
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

MAILTM_API = "https://api.mail.tm"
PROMPT = ("Crie um sistema de gerenciamento de reparos de celular com kanban etc...")

def criar_email_temporario_mailtm():
    print("\nCriando e-mail...")
    dominio = requests.get(f"{MAILTM_API}/domains").json()["hydra:member"][0]["domain"]
    email = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@{dominio}"
    senha = "Senha123"

    conta = {"address": email, "password": senha}
    requests.post(f"{MAILTM_API}/accounts", json=conta)
    token = requests.post(f"{MAILTM_API}/token", json=conta).json()["token"]

    print("\nEmail:",email, "\nSenha:", senha)
    return email, senha, token

def esperar_codigo_mailtm(token, timeout=60):
    headers = {"Authorization": f"Bearer {token}"}
    print("\nAguardando codigo do e-mail")

    for i in range(timeout // 5):
        mensagens = requests.get(f"{MAILTM_API}/messages", headers=headers).json()["hydra:member"]
        if mensagens:
            mensagem_id = mensagens[0]["id"]
            conteudo = requests.get(f"{MAILTM_API}/messages/{mensagem_id}", headers=headers).json()
            html_raw = conteudo.get("html", "")
            html = html_raw[0] if isinstance(html_raw, list) and html_raw else ""
            soup = BeautifulSoup(html, "html.parser")
            h1 = soup.find("h1")
            if h1:
                codigo = re.search(r'\b\d{4,8}\b', h1.text)
                if codigo:
                    return codigo.group()
                else:
                    raise Exception("Código numérico não encontrado no <h1>.")
            else:
                raise Exception("Tag <h1> não encontrada no e-mail.")
        time.sleep(5)

    raise Exception("\nE-mail não chegou a tempo.")

def abrir_site_mitra(driver, wait):
    driver.get("https://mitralab.io/devs")
    print("\nSite Mitra aberto.")
    textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'crie um')]"))
    )
    textarea.send_keys(Keys.TAB)
    textarea.send_keys(PROMPT)
    textarea.send_keys(Keys.ENTER)
    time.sleep(4)

def preencher_email(driver, wait, email):
    BotCad = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="link-create-account"]')))
    BotCad.click()
    BotNome = wait.until(EC.element_to_be_clickable((By.ID, 'signup_form_name')))
    BotNome.send_keys(email.split('@')[0][:4])
    BotEmail = wait.until(EC.element_to_be_clickable((By.ID, 'signup_form_email')))
    BotEmail.send_keys(email)
    BotSenha = wait.until(EC.element_to_be_clickable((By.ID, 'signup_form_password')))
    BotSenha.send_keys("123Lipe")
    bot1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="btn-submit"]')))
    bot1.click()
    print("\nFormulário preenchido.")

def main():
    email, senha, token = criar_email_temporario_mailtm()

    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60)

    try:
        abrir_site_mitra(driver, wait)
        preencher_email(driver, wait, email)
        codigo = esperar_codigo_mailtm(token)
        print(f"\n[INFO] Código recebido: {codigo}")


        campo_codigo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="number"]')))
        campo_codigo.send_keys(codigo)
        print("\n[INFO] Código enviado.")
        time.sleep(999999999)
        print("\n[INFO] Aguardando finalização do bot...")
        time.sleep(999999999)
    except Exception as e:
        print(f"\n[ERRO] {e}")
    print("\n[INFO] Aguardando finalização do bot...")
    time.sleep(999999999999)

    # driver.quit()  # Descomente se quiser fechar automaticamente

if __name__ == "__main__":
    main()
