from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

from tests.conftest import browser


class SbisPage:
    def __init__(self, browser):
        self.browser = browser

    # def test_google(self):
    #         logging.info("Переход на https://google.com/")
    #         self.browser.get("https://google.com")

    def navigate_to_contacts(self):
        try:
            logging.info("Переход на https://sbis.ru/")
            self.browser.get("https://sbis.ru/")

            # Ожидание, пока элемент preload-overlay исчезнет
            WebDriverWait(self.browser, 30).until(
                EC.invisibility_of_element((By.CLASS_NAME, "preload-overlay"))
            )

            # Попытка кликнуть на элемент "Контакты" с повторной попыткой
            for _ in range(3):  # Попробовать 3 раза
                try:
                    contact_link = WebDriverWait(self.browser, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Контакты')]"))
                    )
                    contact_link.click()
                    logging.info("Переход на страницу 'Контакты' выполнен успешно.")
                    break  # Если клик успешен, выходим из цикла
                except Exception as inner_e:
                    logging.warning(f"Ошибка при клике на 'Контакты': {inner_e}")
                    # Ожидание перед повторной попыткой
                    WebDriverWait(self.browser, 2).until(
                        EC.invisibility_of_element((By.CLASS_NAME, "preload-overlay"))
                    )

            # Ожидание появления элемента с ссылкой
            link_element = WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/div/div[2]/a[2]/span"))
            )
            try:
                link_element.click()
                logging.info("Переход на нужную ссылку выполнен успешно.")

                # Вызов функции для клика по баннеру Тензор
                self.click_tensor_banner()

            except Exception as e:
                logging.error(f"Ошибка при попытке кликнуть на ссылку: {str(e)}")

            logging.info("Переход на нужную ссылку выполнен успешно.")



        except Exception as e:
            logging.error(f"Ошибка при переходе на раздел 'Контакты' или клике по элементу: {str(e)}")
            self.browser.quit()

    def click_tensor_banner(self):
        try:
            time.sleep(2)  # Пауза на 2 секунды

            # Ожидание появления элемента с ссылкой
            tensor_link = WebDriverWait(self.browser, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="sbisru-Contacts__logo-tensor mb-12"]'))
            )

            try:
                # Клик по ссылке, которая открывает новую вкладку
                tensor_link.click()
                logging.info("Клик по ссылке выполнен. Открыта новая вкладка.")
                time.sleep(5)

                # Переключение на новую вкладку
                driver = self.browser
                original_window = driver.current_window_handle
                windows = driver.window_handles
                for window in windows:
                    if window != original_window:
                        driver.switch_to.window(window)
                        break

                logging.info("Переключение на новую вкладку выполнено успешно.")

                # Выполняем проверку блока на новой вкладке
                self.verify_sila_v_lyudyah_block()

            except Exception as e:
                logging.error(f"Ошибка при попытке кликнуть на ссылку: {str(e)}")

        except Exception as e:
            logging.error(f"Ошибка при попытке кликнуть на ссылку: {str(e)}")

    def verify_sila_v_lyudyah_block(self):
        logging.info("Начинаем проверку блока 'Сила в людях'.")
        driver = self.browser
        try:
            # Ожидание загрузки страницы
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]')))
            logging.info("Страница загружена.")

            # Закрытие соглашения о cookie, если оно есть
            try:
                cookie_close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.tensor_ru-CookieAgreement__close'))
                )
                cookie_close_button.click()
                logging.info("Cookie-соглашение закрыто.")
            except Exception:
                logging.info("Соглашение о cookie не найдено или уже закрыто.")

            # Прокрутка страницы вниз
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                logging.info("Прокручиваем страницу вниз.")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Даем странице время загрузить контент
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Достигли конца страницы
                last_height = new_height

            # Ищем основной элемент
            main_xpath = '//*[@id="container"]/div[1]/div/div[5]'
            logging.info(f"Ищем основной элемент по XPath: '{main_xpath}'.")
            main_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, main_xpath)))
            logging.info("Главный элемент найден.")

            # Ищем вложенный элемент
            nested_xpath = '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div'
            logging.info(f"Ищем вложенный элемент по XPath: '{nested_xpath}'.")
            nested_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, nested_xpath)))
            logging.info("Вложенный элемент найден.")

            # Нажимаем на ссылку "Подробнее"
            link_xpath = '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a'
            logging.info(f"Ищем элемент для нажатия по XPath: '{link_xpath}'.")
            link_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
            link_element.click()
            logging.info("Нажатие на ссылку 'Подробнее' выполнено.")

        except Exception as e:
            logging.error(f"Ошибка при проверке блока 'Сила в людях': {str(e)}")

    def check_region_and_partners(self):
        try:
            driver = self.browser
            wait = WebDriverWait(driver, 10)

            # 1. Переход на сайт "https://sbis.ru/"
            driver.get("https://sbis.ru/")
            logging.info("Переход на https://sbis.ru/")

            # 2. Переход в раздел "Контакты"
            contacts_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Контакты")))
            contacts_link.click()
            logging.info("Перешли в раздел 'Контакты'.")

            # 3. Проверка, что определился регион (например, Ярославская обл.)
            region_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.sbis_ru-content_wrapper.ws-flexbox.ws-flex-column > div > div.sbis_ru-container.sbisru-Contacts__relative > div.s-Grid-container.s-Grid-container--space.s-Grid-container--alignEnd.s-Grid-container--noGutter.sbisru-Contacts__underline > div:nth-child(1) > div > div:nth-child(2) > span > span")))
            current_region = region_element.text
            logging.info(f"Текущий регион: {current_region}")

            assert "Ярославская обл." in current_region, "Регион не определился как Ярославская обл."

            # Проверка, что есть список партнеров
            city_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="city-id-2"]')))
            city_text = city_element.text
            logging.info(f"Список партнеров в городе: {city_text}")
            assert "Ярославль" in city_text, "Текущий город не Ярославль."

            # 4. Изменение региона на "Камчатский край"
            try:
                region_element.click()
                kamchatka_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[43]')))
                kamchatka_option.click()
                time.sleep(2)
                logging.info("Регион изменен на 'Камчатский край'.")
            except Exception as e:
                logging.info(e)

            # 5. Проверка, что регион изменился на "Камчатский край"
            new_region = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div.sbis_ru-content_wrapper.ws-flexbox.ws-flex-column > div > div.sbis_ru-container.sbisru-Contacts__relative > div.s-Grid-container.s-Grid-container--space.s-Grid-container--alignEnd.s-Grid-container--noGutter.sbisru-Contacts__underline > div:nth-child(1) > div > div:nth-child(2) > span > span")))
            current_region = new_region.text
            logging.info(f"Текущий регион: {current_region}")
            assert "Камчатский край" in current_region, "Регион не определился как Камчатский край."
            #
            # 6. Проверка, что список партнеров изменился
            city_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="city-id-2"]')))
            city_text = city_element.text
            logging.info(f"Список партнеров после изменения: {city_text}")
            assert "Петропавловск-Камчатский" in city_text, "Текущий город не 'Петропавловск-Камчатский'."

            # 7. Проверка, что URL и title содержат информацию о выбранном регионе
            assert "41-kamchatskij-kraj" in driver.current_url, "URL не содержит информации о выбранном регионе."
            assert "СБИС Контакты — Камчатский край" in driver.title, "Title не содержит информации о выбранном регионе."
            logging.info("URL и title содержат информацию о выбранном регионе 'Камчатский край'.")

        except Exception as e:
            logging.error(f"Ошибка при проверке региона и списка партнеров: {str(e)}")
            self.browser.quit()