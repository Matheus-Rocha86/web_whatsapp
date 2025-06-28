from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class WebChromeBrowser:
    """Chrome browser configured."""
    def __init__(self):

        OPTIONS = (
            '--ignore-certificate-errors',  # Ignore certificate errors
            '--ignore-ssl-errors',  # Ignore SSL errors
            '--disable-crl-checks',  # Disable CRL checking
            '--disable-extensions',  # Disable extensions that may interfere
            '--no-sandbox',  # Required on some systems
            '--disable-dev-shm-usage',  # Avoids memory problems
            '--log-level=3'  # Level 3 suppresses most logs
        )
        # Path to project root
        ROOT_FOLDER = Path(__file__).parent

        # Path to the folder where chromedriver is located
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
        """Returns the configured browser"""
        return self.driver
