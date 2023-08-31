import requests
from bs4 import BeautifulSoup as bs

from links import parsingCore

#Класс для нашего условного блока товара
class Sneaker:
    def __init__(self) -> None:
        self.name = None
        self.image = None
        self.source = None
        self.newPrice = None
        self.oldPrice = None
        self.sale = None

def takeHTML(coreLink: str, page: int):
    urlTemplate = coreLink + f'{page}'
    requestedPage = requests.get(urlTemplate)
    return bs(requestedPage.text, "html.parser")

def parsing(categories: list):
    sneakers = {}
    for category in categories:
        #Определяем количество найденных по категории товаров, чтобы посчитать количество страниц
        page = 1
        soupPage = takeHTML(parsingCore[category], page)
        amount = int(soupPage.body.div(class_="x-tree-view-catalog-navigation__category x-tree-view-catalog-navigation__category_selected")[0].span.text)
        PAGES = amount // 60
        if amount - PAGES * 60 > 0:
            PAGES += 1
        #Собираем все необходимые данные со страниц
        iName = 1
        while page <= PAGES:
            grid = soupPage.body.div(class_="grid__catalog")[0]
            foundProducts = grid.find_all("div", class_="x-product-card__card")
            #Разбираем все товары в гриде
            for product in foundProducts:
                nameKey = category + f'-{iName}'
                sneakers[nameKey] = Sneaker()
                sneakers[nameKey].name = product.find("div", class_="x-product-card-description__product-name").text
                #При запросе выгружается только 12 картинок, остальные нужно выгрузить уже со страницы самого товара. Пока оставляю так
                try:
                    sneakers[nameKey].image = product.find("img").get('src')
                except AttributeError:
                    pass
                sneakers[nameKey].source = 'https://www.lamoda.ru' + product.a.get('href')
                sneakers[nameKey].newPrice = product.find("span", class_="x-product-card-description__price-new x-product-card-description__price-WEB8507_price_no_bold").text
                sneakers[nameKey].oldPrice = product.find("span", class_="x-product-card-description__price-old").text
                iName += 1
                print(str(iName) + ' ', sneakers[nameKey].name)
            page += 1
            soupPage = takeHTML(parsingCore[category], page)
    return sneakers