from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BrowseAccountTests(StaticLiveServerTestCase):
    """ Tests browsing inside account app """

    fixtures = ["account_fixture.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_account_registration(self):
        """ test the registration for a new user """
        self.selenium.get(self.live_server_url)
        login_link = self.selenium.find_element_by_css_selector("#visitor_gui a")
        login_link.click()
        wait = WebDriverWait(self.selenium, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "login_side")
            )
        )
        register_link = self.selenium.find_element_by_css_selector("form a")
        register_link.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "signup_side")
            )
        )
        # register form
        self.selenium.find_element_by_id("id_username").send_keys("testuser")
        self.selenium.find_element_by_id("id_first_name").send_keys("Jean Claude")
        self.selenium.find_element_by_id("id_last_name").send_keys("Duss")
        self.selenium.find_element_by_id("id_email").send_keys("testuser@email.com")
        self.selenium.find_element_by_id("id_password1").send_keys("Psiph5sK")
        self.selenium.find_element_by_id("id_password2").send_keys("Psiph5sK")
        self.selenium.find_element_by_id("id_gender_0").click()
        self.selenium.find_element_by_id("id_gender_0").click()
        submit = self.selenium.find_element_by_css_selector("form button")
        submit.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "email_send_msg")
            )
        )
        message = self.selenium.find_element_by_id("email_send_msg").text
        assert message == "Un mail de confirmation a été envoyé à votre adresse."

    def test_account_login(self):
        """ test the login """
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
        account_link = account_links[0]
        account_link.click()
        # my_account template
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "my_account_page")
            )
        )
        username = self.selenium.find_element_by_css_selector("h1 strong").text
        assert username == "GROSSEBOUFFE"
        # disconnect
        account_links = self.selenium.find_elements_by_css_selector("#member_gui a")
        disconnect_button = account_links[2]
        disconnect_button.click()
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "visitor_gui")
            )
        )
        # return to index
        title = self.selenium.find_element_by_css_selector("h1 strong").text
        assert "DU GRAS, OUI" in title
