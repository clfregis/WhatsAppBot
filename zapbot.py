from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
import time
import pandas as pd

data = pd.read_csv(r'./contacts.csv')
df = pd.DataFrame(data, columns=['Name'])

class WhatsappBot:
    def __init__(self):
        self.mensagem = "Insira sua mensagem aqui"
        self.contatos = []
        for i in range(len(df.index)):
            self.contatos.append(df.at[i,'Name'])
        #options = webdriver.ChromeOptions()
        #options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver')

    def EnviarMensagens(self):
        print('Esperando QR ser lido')
        self.driver.get('https://web.whatsapp.com')
        wait = WebDriverWait(self.driver, 10)
        wait5 = WebDriverWait(self.driver, 5)
        input("Leia o codigo QR e entao aperte ENTER")
        print('Executando codigo pica das galaxias!')
        success = 0
        failList = []
        for contato in self.contatos:
            print("Contato eh: " + contato)

            try:
                x_arg = '//span[contains(@title,'+'"'+contato+'"'+')]'

                # Primeiramente procura nos chats anteriores (ou seja, ja estara na tela)
                try:
                    print("Procurando nos chats recentes")
                    wait5.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                    # Se o contato nao foi encontrado, procura por ele na caixa de pesquisa
                except:
                    print("Contato nao encontrado nos chats recentes, pesquisando...")
                    botao_pesquisar = self.driver.find_element_by_xpath('//span[@data-icon="search"]')
                    # clica no botao de pesquisar
                    botao_pesquisar.click()
                    inputSearchBox = self.driver.find_element_by_xpath('//input[@class="_2zCfw copyable-text selectable-text"]')
                    print('Cliquei')
                    time.sleep(1)
                    # inputSearchBox.clear()
                    inputSearchBox.send_keys(contato)
                    print('Contato pesquisado')
                    # Aumente esse tempo se estiver levando muito para pesquisar os contatos
                    time.sleep(4)

                # Clica no Contato
                self.driver.find_element_by_xpath(x_arg).click()
                print("Contato Selecionado com Sucesso")
                time.sleep(2)

                # Seleciona o chat box
                inp_xpath = "//div[@contenteditable='true']"
                chat_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
                time.sleep(1)

                # Envia mensagem
                chat_box.send_keys(self.mensagem)
                time.sleep(2)
                chat_box.send_keys(Keys.ENTER)
                time.sleep(2)
                # Clica no botao de enviar anexo
                self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
                time.sleep(3)
                # Necessario que seja absolute path
                self.driver.find_element_by_css_selector('input[type="file"]').send_keys("absolute_path/1.jpeg")
                time.sleep(2)
                # Clica no botao de enviar
                self.driver.find_element_by_css_selector('span[data-icon="send-light"]').click()
                print("Mensagem enviada com sucesso para: "+ contato + '\n')
                success+=1
                time.sleep(0.5)

            except:
                # Se o contato nao for encontrado
                print("Nao foi possivel encontrar o contato: " + contato)
                failList.append(contato)
                pass

        print("\nEnviado com sucesso para: ", success)
        print("Falha ao enviar para: ", len(failList))
        print(failList)
        print('\n\n')




bot = WhatsappBot()
bot.EnviarMensagens()
print('Fim!!')