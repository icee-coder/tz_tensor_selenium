import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


import logging

@pytest.fixture(scope="function")
def browser():
    # Устанавливаем chromedriver для Chrome
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='test_log.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

