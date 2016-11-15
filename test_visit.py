# -*- coding: utf-8 -*-
# Задание 1
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time, unittest

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

class test_visit(unittest.TestCase):
    def setUp(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(60)
    
    def test_test_visit(self):
        success = True
        wd = self.wd
        wd.get("http://n22127.yclients.com/")
        # Выбрать сотрудника
        # И проверить,что сотрудник выбран
        if not len(wd.find_elements_by_xpath("//i[@class='warn-color-dark master-time-slot ng-binding ng-scope']"))>0:
            wd.find_element_by_xpath("//div[@class='list-item-wrapper ng-scope']//i[@class='fa fa-angle-right y-item-arrow ng-scope']/a").click()
            master = wd.find_element_by_xpath("//div[@class='y-list-item y-master-card__item']//h3[@class='y-master-card__master-name ng-binding']").text
            wd.find_elements_by_xpath("//div[@class='y-master-card__master-info']/i[@class='fa fa-angle-right y-item-arrow ng-scope']/a").click()
        else:
            master = wd.find_element_by_xpath("//div[@class='list-item-wrapper ng-scope']//h4[@class='ng-binding']").text
        # Выбрать услугу
        # И проверить, что услуга выбрана
        if not len(wd.find_elements_by_xpath("//i[@class='y-icon warn-color remove-button mdi mdi-close-circle-outline ng-scope']"))>0:
            wd.find_element_by_xpath("//h3[@class='service-title ng-binding']//i[@class='fa fa-angle-right y-item-arrow ng-scope']/a").click()
            wd.find_elements_by_xpath("//div[@class='service-card-wrapper']//i[@class='fa fa-angle-right y-item-arrow ng-scope']/a").click()
        else:
            service = wd.find_element_by_xpath("//div[@class='list-item-wrapper ng-scope']/h4[@class='services']").text
        # Проверить,что дата и время еще не выбраны
        if not len(wd.find_element_by_xpath("//div[@class='list-item-wrapper ng-scope']//i[@class='y-icon warn-color remove-button mdi mdi-close-circle-outline ng-scope']"))>0:
            wd.find_elements_by_xpath("//h3[@class='ng-binding']//i[@class='fa fa-angle-right y-item-arrow ng-scope']/a").click()
            wd.find_elements_by_xpath("//div[@class='calendar-wrapper light-background-color ng-scope ng-isolate-scope']//button[@class='y-button y-button_transparent ng-binding worked calendar-active-day'").click()
            data = wd.find_elements_by_xpath("//div[@class='calendar-wrapper light-background-color ng-scope ng-isolate-scope']//button[@class='y-button y-button_transparent ng-binding worked calendar-active-day'").text
            if len(wd.find_elements_by_xpath("//button{@class='y-button y-button_transparent time-slot ng-binding']"))>0:
                wd.find_elements_by_xpath("//div[@class='time-content ng-scope']//button[@class='y-button y-button_transparent time-slot ng-binding']").click()
            else:
                wd.find_element_by_xpath("//a[@class='text-color-50 go-to-right y-accent-text-color']/i[@class='fa fa-angle-right']/a").click()
                wd.find_elements_by_xpath("//div[@class='time-content ng-scope']//button{@class='y-button y-button_transparent time-slot ng-binding']").click()
                time = wd.find_elements_by_xpath("//div[@class='time-content ng-scope']//button{@class='y-button y-button_transparent time-slot ng-binding']").text
        else:
            data = wd.find_element_by_xpath("//div[@class='list-item-wrapper ng-scope']//span[@class='ng-binding']").text
            time = wd.find_elements_by_xpath("//div[@class='list-item-wrapper ng-scope']//span[@class='ng-binding ng-scope']").text
        # Переходим на форму оформления заказа
        wd.find_element_by_xpath("//button[text()='Оформить визит']").click()
        # Проверяем сообщения при пустой форме
        assert wd.find_element_by_xpath("//div[@class='errors-block y-block-shadow mb ng-scope']/div[@class='y-items-md-content y-bottom-divider ng-binding ng-scope']").text == 'Введите имя'
        assert wd.find_element_by_xpath("//div[@class='errors-block y-block-shadow mb ng-scope']/div[@class='y-items-md-content y-bottom-divider ng-binding ng-scope']").text == 'Введите телефон'
        # Вводим имя
        wd.find_element_by_xpath("//input[@class='name-input md-input ng-empty ng-dirty ng-valid-parse ng-invalid ng-invalid-required ng-touched']").send_keys("Наталья")
        # Вводим телефон
        wd.find_element_by_xpath("//input[@class='ng-valid md-input ng-valid-mask ng-empty ng-dirty ng-touched']").send_keys("916 955-89-30")
        # Проверяем согласие с пользовательским соглашением
        if not len(wd.find_element_by_xpath("//y-checkbox[@class='order-agreement ng-pristine ng-untouched ng-valid md-checked ng-not-empty ng-valid-required'//]"))>0:
             assert wd.find_element_by_xpath("//div[@class='errors-block y-block-shadow mb ng-scope']/div[@class='y-items-md-content y-bottom-divider ng-binding ng-scope']").text == 'Вы должны принять пользовательское соглашение'
        else:
            wd.find_element_by_xpath("//y-checkbox[@class='order-agreement ng-untouched ng-dirty ng-valid-parse ng-empty ng-invalid ng-invalid-required']").click()
        # Записываемся на прием
        wd.find_element_by_xpath("//button[text()='Записаться']").click()
        # Проверяем прием
        assert wd.find_element_by_xpath("//h3[@class='y-record-card-full__service ng-binding ng-scope y-record-card-full__service_last']").text == '^\d$ $service'
        assert wd.find_element_by_xpath("//h3[@class='y-record-card-full__master-name ng-binding']").text == '$master'
        assert wd.find_element_by_xpath("//div[@class='y-record-card-full__date ng-binding']").text == '$data 2016'
        assert wd.find_element_by_xpath("//div[@class='y-record-card-full__time ng-binding']").text == '$time'
        self.assertTrue(success)


    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
