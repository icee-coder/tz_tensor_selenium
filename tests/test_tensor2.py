import pytest
from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage
import logging
import time

@pytest.mark.usefixtures("browser")
class TestSbisToTensor:

    def test_navigate_to_tensor_and_check_images(self, browser):
        sbis_page = SbisPage(browser)

        sbis_page.check_region_and_partners()

