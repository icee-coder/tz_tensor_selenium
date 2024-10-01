from datetime import time

from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import time

class TensorPage:
    URL = "https://tensor.ru/"

    def __init__(self, browser):
        self.browser = browser

    def check_images_size(self):
        try:
            logging.info("Проверка размеров фотографий в разделе 'Работаем'.")

            # Поиск всех фотографий
            photos = self.browser.find_elements(By.CSS_SELECTOR,
                                                "#container > div.tensor_ru-content_wrapper > div > div.tensor_ru-container.tensor_ru-section.tensor_ru-About__block3 > div.s-Grid-container > div > a > div.tensor_ru-About__block3-image-wrapper")

            if not photos:
                logging.error("Фотографии не найдены на странице.")
                return

            # Получаем реальные размеры первой фотографии через JavaScript
            first_photo = photos[0]
            first_height = self.browser.execute_script("return arguments[0].offsetHeight;", first_photo)
            first_width = self.browser.execute_script("return arguments[0].offsetWidth;", first_photo)
            logging.info(f"Размеры первой фотографии - Высота: {first_height}, Ширина: {first_width}.")

            # Проверяем размеры всех фотографий
            for i, photo in enumerate(photos):
                current_height = self.browser.execute_script("return arguments[0].offsetHeight;", photo)
                current_width = self.browser.execute_script("return arguments[0].offsetWidth;", photo)

                # Логгирование для каждой фотографии
                logging.info(f"Проверка фото {i + 1}: Высота - {current_height}, Ширина - {current_width}.")

                # Сравнение размеров с первой фотографией
                assert current_height == first_height, f"Ошибка: Высота фото {i + 1} не совпадает с первой."
                assert current_width == first_width, f"Ошибка: Ширина фото {i + 1} не совпадает с первой."

            logging.info("Все фотографии имеют одинаковые размеры.")

        except Exception as e:
            logging.error(f"Ошибка при проверке размеров фотографий: {str(e)}")
            self.browser.quit()


