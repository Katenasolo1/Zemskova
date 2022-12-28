import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def show_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, "email").send_keys('qwertyqwerty@mail.ru')
   # Вводим пароль
   pytest.driver.find_element(By.ID,"pass").send_keys('qwerty')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Переходим на страницу Мои Питомцы
   my_pets = pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')
   my_pets.click()

class TableElement(object):
   def __init__(self):
      self.names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
      self.ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
      self.types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')

   def sravnitStrokuSDrugimi(self, current_row):
      for iterator in range(len(self.names)):
         if iterator > current_row:
            print("сравниваем строку")
            print("Сравниваем", self.ages[iterator].get_attribute("innerText"), " c ", self.ages[current_row].get_attribute("innerText"))
            print("Сравниваем", self.names[iterator].get_attribute("innerText"), " c ",
                  self.names[current_row].get_attribute("innerText"))
            print("Сравниваем", self.types[iterator].get_attribute("innerText"), " c ",
                  self.types[current_row].get_attribute("innerText"))
            if self.ages[iterator].get_attribute("innerText") == self.ages[current_row].get_attribute("innerText"):
               if self.names[iterator].get_attribute("innerText") == self.names[current_row].get_attribute("innerText"):
                  if self.types[iterator].get_attribute("innerText") == self.types[current_row].get_attribute("innerText"):
                     print("Нашли!!!!")
                     return 1
      return 0


def test_all_pets_are_present():
   show_my_pets()

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))

   #  Сохраняем в переменную все карточки питомцев
   number_my_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   #  Сохраняем в переменную элементы статистики
   stat = pytest.driver.find_elements(By.XPATH, "//div[@class='.col-sm-4 left']")
   # Получаем количество питомцев из данных статистики
   number = stat[0].text.split('\n')
   number = number[1].split(' ')
   number_from_stat = int(number[1])

   #  Проверяем, что количество питомцев из статистики совпадает с количеством карточек питомцев
   assert number_from_stat == len(number_my_pets)

def test_half_of_pets_have_photo():
   show_my_pets()

   #  Сохраняем в переменную элементы статистики
   stat = pytest.driver.find_elements(By.XPATH, "//div[@class='.col-sm-4 left']")
   # Получаем количество питомцев из данных статистики
   number = stat[0].text.split('\n')
   number = number[1].split(' ')
   number_from_stat = int(number[1])
   print("Количество питомцев из статистики:", number_from_stat)

   element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))

   pets_with_photo = int(0)
   images = pytest.driver.find_elements(By.XPATH, "//th[@scope='row']/img")
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   for i in range(len(names)):
      if images[i].get_attribute("currentSrc") != "":
         pets_with_photo += int(1)

   print("Количество питомцев c фото:", pets_with_photo, "штук")

   itogo = (pets_with_photo / number_from_stat) * 100
   print("Итого питомцев с фото:", itogo, "%")
   assert itogo >= 50

def test_pets_have_name_age_type():
   show_my_pets()

   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
   types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   for i in range(len(names)):
      assert names[i].get_attribute("innerText") != ""
   for i in range(len(ages)):
      assert ages[i].get_attribute("innerText") != ""
   for i in range(len(types)):
      assert types[i].get_attribute("innerText") != ""

def test_pets_have_different_name():
   show_my_pets()

   names_array = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   for current_name in range(len(names_array)):
      for next_name in range(len(names_array)):
         print("Сравнивается")
         print("Current name = ")
         print(names_array[current_name].get_attribute("innerText"))
         print("next_name = ")
         print(names_array[next_name].get_attribute("innerText"))
         if current_name.numerator == next_name.numerator:
            print("Сравнивается тот же элемент с индексом: ", current_name.numerator)
         else:
            assert names_array[next_name].get_attribute("innerText") != names_array[current_name].get_attribute("innerText")

def test_pets_have_different_fields():
   show_my_pets()
   result = 0
   table = TableElement()
   for iterator in range(len(table.names)):
      print("Проверяем элемент номер ", iterator)
      result = table.sravnitStrokuSDrugimi(iterator)
      print("Выводим результат ", result)
      assert result == 0
