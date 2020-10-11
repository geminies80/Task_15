from seleniumbase import BaseCase

class NavigationTest(BaseCase):

    # задаем базовый урл и переменную-словарь
    def setup_class(self):
        self.base_url = "https://www.babyshop.com"
        self.menu_dict = {"Brands":['//div/a[@aria-label="Brands"]', self.base_url+"/brands/s/618"],
                     "Сlothing":['//div/a[@aria-label="Clothing"]', self.base_url+"/clothing/s/619"],
                     "Footwear":['//div/a[@aria-label="Footwear"]',self.base_url+"/footwear/s/620"]
            }


    # проверяем пункты меню
    def test_01_menu(self):
        self.get(self.base_url)
        for item in self.menu_dict:
            print(f"Меню {item}")
            self.click(self.menu_dict[item][0])
            # получаем текущий урл в переменную curr_url
            curr_url = self.get_current_url()
            # проверка соответствия полученного и ожидаемого урл
            self.assert_equal(curr_url, self.menu_dict[item][1])

    def test_02_sub_menu(self):
        self.get(self.base_url)
        sub = '//div[@class="sub-navigation__inner-links js-subnav"]//a[@aria-label="Boots and winter shoes"]'
        #'//div[@class="babyshoes mid-navigation-container"]/div[@class="content c-16"]/div[@class="c-8"]/ul[2]/li[1]/a'
        # '//*[@id="mid-navigation"]/div[@class="babyshoes mid-navigation-container"]//div[@class="c-8"]/ul[2]/li[1]/a'
        #
        #'//*[@id="mid-navigation"]/div[9]/div/div[1]/ul[2]/li[1]/a'
        self.click('//div/a[@aria-label="Footwear"]', sub)


    def test_03_find_items(self):

        self.get(self.base_url)
        # send_keys - это печать текста в поле (отправка клавиш)
        self.send_keys('//input[@id="instant-search__input"]', "Sirona S i-Size Car Seat")
        # клик на кнопке поиска
        self.click('//button[@class="header-search__button btn btn--primary"]')
        # получаем  все элементы по заданному х-пазу и считаем длинну списка 
        count = len(self.find_elements("//article"))
        # сверяем длину и ожидаемый результат
        self.assert_equal(count,5)
        # пример, как можно задать паузу
        self.sleep(2)
  
    def test_04_basket(self):

        # Идем на страницу товаров
        self.get(self.base_url+'/dolce-gabbana/s/1495')
        # сохраняем название первого товара страницы
        item_name = self.get_text('//*[@id="content"]/main/div[4]/article[3]/div[2]/h3/a/strong')
        # эмулируем наведение мышкой и клик на кнопке "Add to cart"
        self.hover_and_click('//article[3]','//article[3]//button[@class="quickshop-btn js-quickshop-btn"]')        
        # выбираем размер в выпадающем меню
        self.click('//article[@data-id="354579"]//button[@class="dropdown__btn"]')
        self.click('//label[@for="product-1643399"]')

       # эмулируем наведение мышкой и клик на кнопке "Add to cart"
        self.click('//button[@class="product-form__btn btn"]')
        # чуть ждем отработки скрипта
        self.sleep(0.1)
        # переходим к оплате
        self.click('//article[3]//a[@href="/cart/view"]')

        # сохраняем название товара в корзине
        basket_name = self.get_text('//*[@id="content"]/div[1]/div[1]/div/div/div[2]/a[1]/span[2]')
        # название выбранного товара и товара в корзине должно совпасть
        self.assert_equal(item_name,basket_name)

        # удаляем товар
        self.click('//span[@class="cart-item__remove-grouped-label"]')
        #self.sleep(0.1)
        # Получаем сообщение, что корзина пуста
        empty_text = self.get_text('//header[@class="cart-view__header"]/h1') 
        # проверяем его
        self.assert_equal(empty_text, "Your cart is empty")

       
    def test_05_change_region(self):
        # 
        self.get(self.base_url+'/dolce-gabbana/s/1495')
        # меняем сначала на анг., т.к. стоимость и регион все равно для России
        self.click('//div[@class="header__links header-links"]//a[@href="/country-and-language"]')
        self.click('//a[@aria-label="English"]')
        self.click('//div[@class="header__links header-links"]//a[@href="/country-and-language"]')
        self.click('//a[@title="USA"]')
        # получаем стоимость для Америки
        eng_text = self.get_text('//*[@id="content"]/main/div[4]/article[3]/div[2]/div/div/span[2]')

        # переход в раздел языковых параметров и их смена на Россию
        self.click('//div[@class="header__links header-links"]//a[@href="/country-and-language"]')
        self.click('//a[@aria-label="Русский"]')
        self.click('//div[@class="header__links header-links"]//a[@href="/country-and-language"]')
        self.click('//a[@title="Россия"]')
        self.sleep(0.1)
        
        # переход в раздел товаров на русском
        #self.get('https://ru.babyshop.com/dolce-gabbana/s/1495')

        # получаем цену для России
        ru_text = self.get_text(('//*[@id="content"]/main/div[4]/article[3]/div[2]/div/div/span[2]'))
        # английский текст не должен совпадать с русским
        self.assert_not_equal(eng_text, ru_text)

