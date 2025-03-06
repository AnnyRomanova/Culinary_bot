from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup


class Culinary:

    def __init__(self):
        # Страница поиска на сайте Повар.ру
        self.host = "https://povar.ru/xmlsearch?query="
        # Создание фссинхронной сессии
        self.session = aiohttp.ClientSession()

    # Прописываем заголовок в Http-запрос
    # Указываем User-агента, чтобы при парсинге сервер не блокировал запрос
    @property
    def headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

    # метод отправки get-запроса
    async def make_request(self, url: str) -> str:
        async with self.session.get(url, headers=self.headers) as response:
            return await response.text()

    async def get_recipe(self, recipe_name: str):
        url = self.host + quote(recipe_name)
        data = await self.make_request(url)
        soup = BeautifulSoup(data, "lxml")
        recipe_list = soup.find_all("div", class_="recipe")
        recipe_dict = {}
        for recipe in recipe_list[:3 ]:
            title = recipe.find("a").text
            link = "https://povar.ru" + recipe.find("a").get("href")
            recipe_dict[title] = link

        return recipe_dict