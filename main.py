import aiohttp
import asyncio
import aiofiles
import pymorphy2
from anyio import sleep, create_task_group, run
from adapters.inosmi_ru import sanitize, test_sanitize
from text_tools import split_by_words, calculate_jaundice_rate


TEST_ARTICLES = [
    'https://inosmi.ru/20241031/tramp-270579213.html',
    'https://inosmi.ru/20241105/vybory-270639230.html',
    'https://inosmi.ru/20241106/vybory-270653156.html',
    'https://inosmi.ru/20241106/ekonomika-270651327.html',
    'https://inosmi.ru/20241106/izrail-270660075.html'
]

async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


# async def read_charged_dict_to_list(file_path, words_list):
#     async with aiofiles.open(file_path, mode='r') as file:
#         async for line in file:
#             words_list.append(line.strip())
#     return words_list

def read_charged_dict_to_list(file_path, words_list):
    with open(file_path, 'r') as file:
        for line in file:
            words_list.append(line.strip())
    return words_list


async def process_article(session, morph, charged_words, url, title):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
    text = sanitize(html, plaintext=True)
    text = split_by_words(morph, text)
    result = calculate_jaundice_rate(text, charged_words)
    print('Заголовок:', title)
    print(f'URL: {url}')
    print(f'Рейтинг: {result}')
    print(f'Слов в статье: {len(text)}')



async def main():
    negative_words_list = read_charged_dict_to_list('./charged_dict/negative_words.txt', words_list=[])
    morph = pymorphy2.MorphAnalyzer()
    async with create_task_group() as tg:
        for url in TEST_ARTICLES:
                tg.start_soon(process_article, 'session', morph, negative_words_list, url, '')


if __name__ == '__main__':
    asyncio.run(main())
