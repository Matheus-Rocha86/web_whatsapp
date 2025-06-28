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
    """The class "rotate collection" sends
    collection messages. It receives as a parameter (website) a string,
    a spreadsheet in DataFrame (data_frame),
    the configured browser (browser)
    and a name of the person generating the collection
    (usarname) in string.
    It writes a file in .xlsx with the collection
    data in the root of the folder and
    returns a None value.
    """

    def __init__(self, costumers_list, browser: WebDriver, website: str, billing_message=None):
        self.costumers_list = costumers_list
        self.browser: WebDriver = browser
        self.website = website
        self.billing_message = billing_message
        self.data = []
        self.data_no_send = []

    def run_billing(self):
        """## The method opens the browser.
            #### Sends billing messages:
            #### Returns a None value:
        """

        # Get the link to open Whatsapp
        self.browser.get(self.website)

        # Keep the browser open until Selenium finds an element
        while len(self.browser.find_elements(By.ID, "side")) < 1:
            sleep(1)

        # Check welcome screen
        try:
            wait = WebDriverWait(self.browser, randint(5, 15))
            button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'x889kno')]"))
            )
            sleep(randint(10, 15))
            button.click()  # Send the click
        except TimeoutException:
            print('Mensagem de boas-vindas não presente.')

        # Today's date
        to_day = datetime.today().strftime('%d-%m-%Y')

        # Create progress bar
        progress_bar = tqdm(range(len(self.costumers_list)), desc="Enviando mensagens")

        #  Scroll through the contact list and send the message
        for i in progress_bar:
            pessoa = self.costumers_list[i][0]
            valor = self.costumers_list[i][1]
            numero = self.costumers_list[i][2]

            # Updates the description dynamically
            progress_bar.set_description(f"Enviando para {pessoa}")
            texto = self.create_message_default(pessoa, valor)
            link = f"https://web.whatsapp.com/send?phone={int(numero)}&text={texto}"
            self.browser.get(link)

            # Wait for contacts to load on the page
            while len(self.browser.find_elements(By.ID, "side")) < 1:
                sleep(1)

            try:
                # Send the message to the contact registered on Whatsapp
                wait = WebDriverWait(self.browser, 20)
                button_send = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Enviar')]"))
                )
                sleep(randint(10, 15))
                button_send.click()  # Send the click
                sleep(randint(10, 15))
            except TimeoutException:
                try:
                    # The phone number shared by url is invalid
                    wait = WebDriverWait(self.browser, 20)
                    button_url_inv = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'x889kno')]"))
                    )

                    self.data_no_send.append(pessoa)

                    sleep(randint(10, 15))
                    button_url_inv.click()  # Send the click
                    sleep(randint(10, 15))
                except TimeoutException as e:
                    print(f'Exceção: {e}')
            else:
                # Creates a list of tuples with customer data
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
        """Formats numbers with "." and "," to separate
        thousands and decimals
        """
        valor_ = f'{num:_.2f}'
        valor_fmt = valor_.replace('.', ',').replace('_', '.')
        return valor_fmt

    def create_message_default(self, pessoa: str, num: str) -> str:
        """Customer Message Generator"""

        if self.billing_message is None:
            emoji = "\U0001F6A8"  # Unicode code for the "siren" emoji
            n = 2  # Number that will repeat the emoji 'n' times
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
