from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowseProductTests(StaticLiveServerTestCase):
    """ Tests browsing inside product app """

    fixtures = ['product_fixture.json', 'substitutes_fixture.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_product_navigation(self):
        """ tests for navigation in product """
        # index template: -page and header title  -number of sections
        self.selenium.get(self.live_server_url)
        page_title = self.selenium.title
        header_title = self.selenium.find_element_by_tag_name("h1")
        sections = self.selenium.find_elements_by_tag_name("section")
        assert  page_title == "Pur Beurre WebApp"
        assert header_title.text == "DU GRAS, OUI, MAIS DE QUALITÉ!"
        assert len(sections) == 2
        # index form submit
        input_search = self.selenium.find_element_by_id("input_search")
        input_search.send_keys("nutella")
        self.selenium.find_element_by_id("submit").click()
        # wait the response
        wait = WebDriverWait(self.selenium, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "header_prod_list")
            )
        )
        # substitutes list template: - product name  - pagination
        product_name = self.selenium.find_element_by_tag_name("h2")
        assert product_name.text == "Nutella"
        substitute_names = self.selenium.find_elements_by_css_selector("figcaption strong")
        assert len(substitute_names) == 6
        # product template:
        # -correct description with the second substitute
        second_substitute_name = substitute_names[1].text
        description_links = self.selenium.find_elements_by_css_selector('figcaption a')
        second_description_link = description_links[1]
        second_description_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "description")
            )
        )
        substitute_name = self.selenium.find_element_by_tag_name("h2")
        assert second_substitute_name == substitute_name.text
        # - nutriscore
        images = self.selenium.find_elements_by_tag_name("img")
        nutriscore_url = images[2].get_attribute("src")
        nutriscore = nutriscore_url[-5]
        assert nutriscore < "e"
        # link to OpenFoddFacts product page
        off_link = self.selenium.find_element_by_css_selector("section a")
        off_link.click()
        page_title = self.selenium.title
        wait.until(
            EC.number_of_windows_to_be(2)
        )
        self.selenium.switch_to_window(self.selenium.window_handles[1])
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "top-bar")
            )
        )
        assert "openfoodfacts" in self.selenium.current_url
        assert second_substitute_name.lower() in self.selenium.title.lower()
