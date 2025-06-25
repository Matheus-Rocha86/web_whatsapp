import urllib.parse
import urllib
from tqdm import tqdm
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    def __init__(self, costumers_list, browser: WebDriver, website: str, billing_message=None):
        self.costumers_list = costumers_list
        self.browser: WebDriver = browser
        self.website = website
        self.billing_message = billing_message
        self.data = []
        self.data_no_send = []

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

        # Verifica tela de boas-vindas
        try:
            wait = WebDriverWait(self.browser, randint(5, 15))
            button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'x889kno')]"))
            )
            sleep(randint(10, 15))
            button.click()  # Manda o clique
        except TimeoutException:
            print('Mensagem de boas-vindas não presente.')

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
            texto = self.create_message_default(pessoa, valor)
            link = f"https://web.whatsapp.com/send?phone={int(numero)}&text={texto}"
            self.browser.get(link)

            # Espera até os contatos carregarem na página
            while len(self.browser.find_elements(By.ID, "side")) < 1:
                sleep(1)

            try:
                # Envia a mensagem para o contato cadastrado no Whatsapp
                wait = WebDriverWait(self.browser, 20)
                button_send = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Enviar')]"))
                )
                sleep(randint(10, 15))
                button_send.click()  # Manda o clique
                sleep(randint(10, 15))
            except TimeoutException:
                try:
                    # O número de telefone compartilhado por url é inválido
                    wait = WebDriverWait(self.browser, 20)
                    button_url_inv = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'x889kno')]"))
                    )

                    self.data_no_send.append(pessoa)

                    sleep(randint(10, 15))
                    button_url_inv.click()  # Manda o clique
                    sleep(randint(10, 15))
                except TimeoutException as e:
                    print(f'Exceção: {e}')
            else:
                # Cria uma lista de tuplas com os dados dos clientes
                from_costumers_list_to_data = (pessoa, valor, to_day)
                self.data.append(from_costumers_list_to_data)
        self.browser.quit()
        print()
        print('-' * 25)
        print('List of unnotified customers')
        for customer in self.data_no_send:
            print(customer)
        return self.data

    def format_number(self, num: str) -> str:
        """
        Formata números com "." e "," para separar
        milhares e decimais
        """
        valor_ = f'{num:_.2f}'
        valor_fmt = valor_.replace('.', ',').replace('_', '.')
        return valor_fmt

    def create_message_default(self, pessoa: str, num: str) -> str:
        """
        Gerador de mensagens ao cliente
        """
        if self.billing_message is None:
            emoji = "\U0001F6A8"  # Código em unicode do emoji "sirene"
            n = 2  # número que vai repetir o emoji por 'n' vezes.
            text = (
                f'Oi {pessoa}, aqui é da Loja São Lucas da BR-316, '
                f'verificamos que o senhor(a) tem débito(s) '
                f'em atraso no total de '
                f'*R$ {self.format_number(num)}*. '
                f'Entre em contato para mais informações.{emoji * n}'
            )
            msg = urllib.parse.quote(text)
            return msg
        else:
            text = (
                f'Olá {pessoa}, tudo bem? '
                f'Gostaríamos de lembrar sobre o pagamento '
                f'pendente do(s) seu(s) débito(s). '
                f'Caso já tenha efetuado o pagamento, por favor, '
                f'desconsidere este lembrete. Agradecemos a sua atenção!'
            )
            msg = urllib.parse.quote(text)
            return msg
