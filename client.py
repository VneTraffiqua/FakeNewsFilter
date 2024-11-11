import aiohttp
import asyncio

async def fetch():
    url = ("http://127.0.0.1:8080/?urls=https://inosmi.ru/20241031/tramp-270579213.html,"
           "https://inosmi.ru/20241105/vybory-270639230.html,"
           "https://inosmi.ru/20241106/vybory-270653156.html,"
           "https://inosmi.ru/20241106/ekonomika-270651327.html,"
           "https://inosmi.ru/20241106/izrail-270660075.html,"
           "https://inosmi.ru/not/exist.html,"
           "https://lenta.ru/brief/2021/08/26/afg_terror/,"
           "https://www.gutenberg.org/cache/epub/74696/pg74696-images.html")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(await response.text())

if __name__ == "__main__":
    asyncio.run(fetch())