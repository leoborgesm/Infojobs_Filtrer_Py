from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import smtplib
import email.message 
import os

firefox_options = Options()
firefox_options.headless = True

#variaveis
keyword = input('Digite a(s) palavra(s) chave(s): ')
localizaçao = input('Digite a localizaçao das vagas: ')
email_to = input('Digite o email para receber as vagas: ')

#Digite aqui o email remetente
email_from = ''

#Digite aqui o email destinatario
email_to = ''
#digite aqui a senha do app google
password_google = ''
os.system('cls')

#URL
driver = webdriver.Firefox(options=firefox_options)
driver.get('https://www.infojobs.com.br')
driver.set_window_size(1920,1080)

#aceitar cookies
driver.find_element('xpath','/html/body/div[1]/div/div/div/div/div/div[3]/button[2]/span').click()

#palavra_chave
palavra_chave = driver.find_element('xpath','//*[@id="keywordsCombo"]')
palavra_chave.send_keys(keyword)

#localização
local = driver.find_element('xpath','//*[@id="city"]')
local.send_keys(localizaçao)
local.send_keys(Keys.RETURN)
time.sleep(3)
#data
data = driver.find_element('xpath','/html/body/main/div[1]/div[2]/div/div[1]/div[1]/div/div[3]/div[1]')
data.click()

semana = driver.find_element('xpath','/html/body/main/div[1]/div[2]/div/div[1]/div[1]/div/div[3]/div[2]/div/a[3]')
semana.click()

#cards

cards = driver.find_elements(By.XPATH,'//*[@id="filterSideBar"]//div[contains(@class,"card card-shadow card-shadow-hover text-break mb-16 grid-row js_rowCard")]')

#info email 
msg = email.message.Message()

corpo_email = ""

#loop
linha = '=' * 100
contador = 0

for card in cards:
    try:
        contador += 1
        card.click()
        time.sleep(0.5)

        
        nome_vaga = driver.find_element('xpath','//*[@id="VacancyHeader"]/div[1]/div[1]/h2')
        nome_vaga = nome_vaga.text
        corpo_email += f'<p>{nome_vaga}</p>\n'
        print(nome_vaga)
        
        
        detalhes = driver.find_elements(By.XPATH,'//*[@id="VacancyHeader"]/div[1]/div[1]/div[2]//div[contains(@class,"text-medium")]')
        for detalhe in detalhes:
            detalhe_texto = detalhe.text
            corpo_email += f'<p>{detalhe_texto}</p>\n'
            print(detalhe_texto)
  
        #URL
        element = card.find_element(By.XPATH, './/div[contains(@class, "js_cardLink")]')
        url_pagina = element.get_attribute("data-href")
        print(f'https://www.infojobs.com.br{url_pagina}')
        corpo_email += f'<p> URL: https://www.infojobs.com.br{url_pagina}</p>\n'


        
        print('-' * 46)
        corpo_email += f'<p>{linha}</p>\n'
    except Exception as error:
        continue


#configurar email , senha

if contador != 0:
    msg = email.message.Message()
    msg['Subject'] = "Info Jobs Filtrer"
    msg['From'] = email_from
    msg['To'] = email_to
    password = password_google
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print(f'Aqui esta {contador} vaga(s) da palavra chave {keyword}')
    corpo_email+= f'<p>Aqui esta {contador} vaga(s) na ultima semana da palavra chave:" {keyword}" </p>\n'
    print('Email enviado')
else:
    print(f'Nenhuma vaga encontrada com a palavra chave "{keyword}", na localização {localizaçao}, na ultima semana')

driver.quit()

