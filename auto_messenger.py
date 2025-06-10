import urllib.parse
import urllib
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
from random import randint


class AutoMessenger:
    ''' A classe rodar cobrança envia
        mensagens de cobrança. Recebe como
        parâmetro (website) uma string,
        um (data_frame) a planilha em DataFrame,
        o navegador configurado (browser)
        e um nome de quem gera a cobrança
        (usarname) em string.
        Grava na raíz da pasta um arquivo
        em .xlsx com os dados da cobrança e
        retorna um valor None.
    '''
    def __init__(self, costumers_list, browser, website: str):
        self.costumers_list = costumers_list
        self.browser = browser
        self.website = website

    def run_billing(self):
        """
        O método abre o navegador.

        :Envia as mensagens de cobrança:
        :Retorna um valor None:
        """

        # Pega o link para abrir o Whatsapp
        self.browser.get(self.website)

        # Mantem aberto o browser até o selenium encontrar algum elemento
        while len(self.browser.find_elements(By.ID, "side")) < 1:
            sleep(1)

        # Cria uma lista de dados dos clientes
        data = []

        # Data de hoje
        to_day = datetime.today().strftime('%d-%m-%Y')

        # Cria barra de progresso
        progress_bar = tqdm(range(len(self.costumers_list)), desc="Enviando mensagens")

        # Percorrer a lista de contatos e envia a mensagem
        for i in progress_bar:
            pessoa = self.costumers_list[i][0]
            valor = self.costumers_list[i][1]
            numero = self.costumers_list[i][2]

            # Atualiza a descrição dinamicamente
            progress_bar.set_description(f"Enviando para {pessoa}")

            texto = self.create_message(pessoa, valor)
            link = f"https://web.whatsapp.com/send?phone={int(numero)}&text={texto}"
            self.browser.get(link)

            # Espera até os contatos carregarem na página
            while len(self.browser.find_elements(By.ID, "side")) < 1:
                sleep(1)
            # Esperar 15 seg para continuar
            sleep(randint(5, 15))

            # Verifica se o contato está cadastrado no Whatsapp
            try:
                self.browser.find_element(By.CLASS_NAME, 'x12lqup9')

            except NoSuchElementException:
                # Esperar 15 seg para continuar
                sleep(randint(5, 15))

                # Envia a mensagem para o contato cadastrado no Whatsapp
                self.browser.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p/span').send_keys(Keys.ENTER)
                sleep(randint(5, 15))

                # Cria uma lista de tuplas com os dados dos clientes
                from_costumers_list_to_data = (pessoa, valor, to_day)
                data.append(from_costumers_list_to_data)

            finally:
                pass

        return data

    def format_number(self, num):
        valor_ = f'{num:_.2f}'
        valor_fmt = valor_.replace('.', ',').replace('_', '.')
        return valor_fmt

    def create_message(self, pessoa, num):
        emoji = "\U0001F6A8"  # Código em unicode do emoji "sirene"
        n = 2  # número que vai repetir o emoji por 'n' vezes.
        text = (
            f'Oi {pessoa}, aqui é da Loja São Lucas da BR-316, '
            f'verificamos que o senhor(a) tem débito(s) '
            f'em atraso no total de, '
            f'*R$ {self.format_number(num)}*. '
            f'Entre em contato para mais informações.{emoji * n}'
        )
        msg = urllib.parse.quote(text)
        return msg
