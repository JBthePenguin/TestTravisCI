from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowseFavoriteTests(StaticLiveServerTestCase):
    """ Tests browsing inside favorite app """

    fixtures = [
        "account_fixture.json",
        "favorite_fixture.json",
        "substitutes_fixture.json"
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_favorite_navigation(self):
        """ tests for navigation in product """
        # favorites template
        #connect to account
        self.selenium.get(self.live_server_url)
        login_link = self.selenium.find_element_by_css_selector("#visitor_gui a")
        login_link.click()
        wait = WebDriverWait(self.selenium, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "login_side")
            )
        )
        # login form
        self.selenium.find_element_by_id("id_username").send_keys("grossebouffe")
        self.selenium.find_element_by_id("id_password").send_keys("azertyui")
        submit = self.selenium.find_element_by_css_selector("form button")
        submit.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "member_gui")
            )
        )
        account_links = self.selenium.find_elements_by_css_selector("#member_gui a")
        account_link = account_links[1]
        account_link.click()
        # favorites list template
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "favorites_page")
            )
        )
        title = self.selenium.find_element_by_tag_name("h1").text
        assert "MES PRODUITS" == title
        favorites = self.selenium.find_elements_by_class_name("card")
        assert len(favorites) == 2
        # favorite display with template substitutes_list
        favorite_links = self.selenium.find_elements_by_css_selector(".card a")
        first_favorite_link = favorite_links[1]
        first_favorite_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "save_prod")
            )
        )
        substitutes_saved = self.selenium.find_elements_by_class_name("save_prod")
        assert len(substitutes_saved) == 3
        # delete favorite
        save_check_buttons = self.selenium.find_elements_by_class_name("save_prod")
        save_check_buttons[0].click()
        popup = self.selenium.switch_to.alert
        popup.accept()
        # return to index
        search_button = self.selenium.find_element_by_css_selector("#topNavBar .col-md-2 a")
        search_button.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "search")
            )
        )
        # return favorites list template
        account_links = self.selenium.find_elements_by_css_selector("#member_gui a")
        account_link = account_links[1]
        account_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "favorites_page")
            )
        )
        # return favorite display with template substitutes_list
        favorite_links = self.selenium.find_elements_by_css_selector(".card a")
        first_favorite_link = favorite_links[1]
        first_favorite_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "save_prod")
            )
        )
        substitutes_saved = self.selenium.find_elements_by_class_name("save_prod")
        assert len(substitutes_saved) == 2
        # delete all substitutes for this product
        save_check_buttons = self.selenium.find_elements_by_class_name("save_prod")
        save_check_buttons[0].click()
        popup = self.selenium.switch_to.alert
        popup.accept()
        save_check_buttons[1].click()
        popup = self.selenium.switch_to.alert
        popup.accept()
        # return favorites list template
        account_links = self.selenium.find_elements_by_css_selector("#member_gui a")
        account_link = account_links[1]
        account_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "favorites_page")
            )
        )
        favorites = self.selenium.find_elements_by_class_name("card")
        assert len(favorites) == 1
        # return to index
        search_button = self.selenium.find_element_by_css_selector("#topNavBar .col-md-2 a")
        search_button.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "search")
            )
        )
        # index form submit (search)
        input_search = self.selenium.find_element_by_id("input_search")
        input_search.send_keys("nutella")
        self.selenium.find_element_by_id("submit").click()
        # wait the response
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "save_prod")
            )
        )
        # save  new favorite for the same product
        save_check_buttons = self.selenium.find_elements_by_class_name("save_prod")
        save_check_buttons[3].click()
        save_check_buttons[5].click()
        # return to favorites list
        account_links = self.selenium.find_elements_by_css_selector("#member_gui a")
        account_link = account_links[1]
        account_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "favorites_page")
            )
        )
        # return to favorite
        favorite_links = self.selenium.find_elements_by_css_selector(".card a")
        first_favorite_link = favorite_links[1]
        first_favorite_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "portfolio-box")
            )
        )
        substitutes_saved = self.selenium.find_elements_by_class_name("portfolio-box")
        assert len(substitutes_saved) == 2
