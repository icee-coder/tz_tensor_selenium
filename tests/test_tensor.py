import pytest
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
import logging
import time

@pytest.mark.usefixtures("browser")
class TestSbisToTensor:

    def test_navigate_to_tensor_and_check_images(self, browser):
        sbis_page = SbisPage(browser)
        tensor_page = TensorPage(browser)

        # Шаг 1: Переходим на SBIS и открываем контакты
        sbis_page.navigate_to_contacts()

        # Шаг 5: Проверяем размеры фотографий в хронологии
        tensor_page.check_images_size()

