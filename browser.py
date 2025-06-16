from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebChromeBrowser:
    """Nevegador Chrome configurado."""
    def __init__(self):

        OPTIONS = (
            '--ignore-certificate-errors',  # Ignora erros de certificado
            '--ignore-ssl-errors',  # Ignora erros SSL
            '--disable-crl-checks',  # Desativa verificação CRL
            '--disable-extensions',  # Desativa extensões que podem interferir
            '--no-sandbox',  # Necessário em alguns sistemas
            '--disable-dev-shm-usage',  # Evita problemas de memória
            '--log-level=3'  # Nível 3 suprime a maioria dos logs
        )
        # Caminho para a raiz do projeto
        ROOT_FOLDER = Path(__file__).parent

        # Caminho para a pasta onde o chromedriver está
        CHROME_DRIVER_PATH = ROOT_FOLDER / 'drivers' / 'chromedriver.exe'

        chrome_options = webdriver.ChromeOptions()

        if OPTIONS is not None:
            for option in OPTIONS:
                chrome_options.add_argument(option)  # type: ignore

        chrome_service = Service(
            executable_path=str(CHROME_DRIVER_PATH),
            )

        self.driver = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

    def get_driver(self):
        return self.driver
