import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    """Фикстура для настройки браузера"""
    with allure.step("Настройка браузера Chrome для тестирования"):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        allure.attach("Браузер Chrome успешно запущен", "Статус", allure.attachment_type.TEXT)
        yield driver
        driver.quit()
        allure.attach("Браузер закрыт", "Статус", allure.attachment_type.TEXT)


@allure.epic("Тестирование веб-интерфейсов")
@allure.feature("Авторизация на сайте the-internet")
class TestLoginForm:
    
    @allure.title("Успешная авторизация с валидными данными")
    @allure.description("Тест проверяет, что пользователь может успешно войти в систему, используя правильные учетные данные: tomsmith / SuperSecretPassword!")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke", "positive", "critical")
    def test_successful_login(self, driver):
        with allure.step("Открыть страницу авторизации"):
            driver.get("https://the-internet.herokuapp.com/login")
            allure.attach(driver.current_url, "Текущий URL", allure.attachment_type.TEXT)
        
        with allure.step("Найти поле ввода логина"):
            username_field = driver.find_element(By.ID, "username")
            allure.attach("Поле логина найдено", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Найти поле ввода пароля"):
            password_field = driver.find_element(By.ID, "password")
            allure.attach("Поле пароля найдено", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Найти кнопку входа"):
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            allure.attach("Кнопка входа найдена", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Ввести логин 'tomsmith'"):
            username_field.send_keys("tomsmith")
            allure.attach("tomsmith", "Введенный логин", allure.attachment_type.TEXT)
        
        with allure.step("Ввести пароль 'SuperSecretPassword!'"):
            password_field.send_keys("SuperSecretPassword!")
            allure.attach("********", "Введенный пароль", allure.attachment_type.TEXT)
        
        with allure.step("Нажать кнопку входа"):
            login_button.click()
            allure.attach("Кнопка нажата", "Действие", allure.attachment_type.TEXT)
        
        with allure.step("Проверить сообщение об успешном входе"):
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
            )
            allure.attach(success_message.text, "Сообщение об успехе", allure.attachment_type.TEXT)
            assert "You logged into a secure area!" in success_message.text, "Сообщение об успешном входе не найдено"
        
        with allure.step("Проверить наличие кнопки выхода"):
            logout_button = driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
            assert logout_button.is_displayed(), "Кнопка выхода не отображается"
            allure.attach("Кнопка выхода найдена", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Сделать скриншот успешной авторизации"):
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, "Скриншот после входа", allure.attachment_type.PNG)
    
    @allure.title("Неуспешная авторизация с неверными данными")
    @allure.description("Тест проверяет, что система показывает ошибку при вводе неверного логина или пароля")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_unsuccessful_login(self, driver):
        with allure.step("Тест 1: Авторизация с неверным логином"):
            with allure.step("Открыть страницу авторизации"):
                driver.get("https://the-internet.herokuapp.com/login")
            
            with allure.step("Ввести неверный логин 'wrongusername' и верный пароль"):
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_field = driver.find_element(By.ID, "password")
                login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                
                username_field.send_keys("wrongusername")
                password_field.send_keys("SuperSecretPassword!")
                login_button.click()
            
            with allure.step("Проверить сообщение об ошибке"):
                error_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
                )
                allure.attach(error_message.text, "Сообщение об ошибке", allure.attachment_type.TEXT)
                assert "Your username is invalid!" in error_message.text, "Сообщение о неверном логине не найдено"
        
        with allure.step("Тест 2: Авторизация с верным логином и неверным паролем"):
            with allure.step("Открыть страницу авторизации"):
                driver.get("https://the-internet.herokuapp.com/login")
            
            with allure.step("Ввести верный логин и неверный пароль"):
                username_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                password_field = driver.find_element(By.ID, "password")
                login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                
                username_field.send_keys("tomsmith")
                password_field.send_keys("wrongpassword")
                login_button.click()
            
            with allure.step("Проверить сообщение об ошибке"):
                error_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
                )
                allure.attach(error_message.text, "Сообщение об ошибке", allure.attachment_type.TEXT)
                assert "Your password is invalid!" in error_message.text, "Сообщение о неверном пароле не найдено"
        
        with allure.step("Сделать скриншот ошибки авторизации"):
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, "Скриншот ошибки", allure.attachment_type.PNG)
    
    @allure.title("Авторизация с пустыми полями")
    @allure.description("Тест проверяет, что система показывает ошибку при попытке входа с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation", "empty-fields")
    def test_empty_fields_login(self, driver):
        with allure.step("Открыть страницу авторизации"):
            driver.get("https://the-internet.herokuapp.com/login")
            allure.attach(driver.current_url, "Текущий URL", allure.attachment_type.TEXT)
        
        with allure.step("Нажать кнопку входа без заполнения полей"):
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            allure.attach("Кнопка нажата без ввода данных", "Действие", allure.attachment_type.TEXT)
        
        with allure.step("Проверить сообщение об ошибке"):
            error_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
            )
            allure.attach(error_message.text, "Сообщение об ошибке", allure.attachment_type.TEXT)
            assert "Your username is invalid!" in error_message.text or "error" in error_message.text.lower(), "Сообщение об ошибке не найдено"
        
        with allure.step("Сделать скриншот ошибки"):
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, "Скриншот ошибки при пустых полях", allure.attachment_type.PNG)
    
    @allure.title("Проверка заголовка страницы авторизации")
    @allure.description("Тест проверяет, что страница авторизации имеет правильный заголовок")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("smoke", "ui")
    def test_login_page_title(self, driver):
        with allure.step("Открыть страницу авторизации"):
            driver.get("https://the-internet.herokuapp.com/login")
        
        with allure.step("Получить заголовок страницы"):
            title = driver.title
            allure.attach(title, "Заголовок страницы", allure.attachment_type.TEXT)
        
        with allure.step("Проверить заголовок страницы"):
            assert "The Internet" in title or "Login" in title, f"Заголовок '{title}' не соответствует ожидаемому"
    
    @allure.title("Проверка наличия всех элементов формы")
    @allure.description("Тест проверяет, что все элементы формы авторизации присутствуют на странице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "positive")
    def test_form_elements_exist(self, driver):
        with allure.step("Открыть страницу авторизации"):
            driver.get("https://the-internet.herokuapp.com/login")
        
        with allure.step("Проверить наличие поля ввода логина"):
            username_field = driver.find_element(By.ID, "username")
            assert username_field.is_displayed(), "Поле логина не отображается"
            allure.attach("Поле логина присутствует", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Проверить наличие поля ввода пароля"):
            password_field = driver.find_element(By.ID, "password")
            assert password_field.is_displayed(), "Поле пароля не отображается"
            allure.attach("Поле пароля присутствует", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Проверить наличие кнопки входа"):
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            assert login_button.is_displayed(), "Кнопка входа не отображается"
            allure.attach("Кнопка входа присутствует", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Проверить наличие ссылки на страницу Elemental Selenium"):
            elemental_link = driver.find_element(By.CSS_SELECTOR, "a[href='http://elementalselenium.com/']")
            assert elemental_link.is_displayed(), "Ссылка на Elemental Selenium не отображается"
            allure.attach("Ссылка на Elemental Selenium присутствует", "Результат", allure.attachment_type.TEXT)
        
        with allure.step("Сделать скриншот формы авторизации"):
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, "Скриншот формы авторизации", allure.attachment_type.PNG)
