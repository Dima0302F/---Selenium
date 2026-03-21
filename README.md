# Login Tests Automation

Automated tests for the-internet.herokuapp.com login form using Selenium, pytest and Allure.

## 📊 Allure Report

### Просмотр отчета
Актуальный Allure отчет доступен по ссылке:  
🔗 [https://dima0302f.github.io/---Selenium/](https://dima0302f.github.io/---Selenium/)

[![Allure Report](https://img.shields.io/badge/Allure-Report-brightgreen)](https://dima0302f.github.io/---Selenium/)
[![GitHub Actions](https://github.com/Dima0302F/---Selenium/actions/workflows/test.yml/badge.svg)](https://github.com/Dima0302F/---Selenium/actions)

---

## 📝 Test Scenarios

| № | Тест | Описание |
|---|------|----------|
| 1 | **Successful Login** | Вход с валидными данными (tomsmith / SuperSecretPassword!) |
| 2 | **Unsuccessful Login** | Вход с неверным логином или паролем |
| 3 | **Empty Fields** | Попытка входа с пустыми полями |
| 4 | **Page Title** | Проверка заголовка страницы |
| 5 | **Form Elements** | Проверка наличия всех элементов формы |

---

## 🚀 Setup

### 1. Clone the repository
```bash
git clone https://github.com/Dima0302F/---Selenium.git
cd ---Selenium
