import aiohttp
from aiohttp import web
import asyncio
import pymorphy2
from anyio import create_task_group
from adapters.inosmi_ru import sanitize
from adapters.exceptions import ArticleNotFound
from text_tools import split_by_words, calculate_jaundice_rate
from enum import Enum
from async_timeout import timeout
from contextlib import asynccontextmanager
import time
from functools import partial


TIMEOUT=3
MAX_URLS_IN_REQUEST=10

class ProcessingStatus(Enum):
    OK = 'OK'
    FETCH_ERROR = 'FETCH_ERROR'
    PARSING_ERROR = 'PARSING_ERROR'
    TIMEOUT = 'TIMEOUT'

async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()

@asynccontextmanager
async def time_execution(article_params):
    start_time = time.monotonic()
    try:
        yield
    finally:
        end_time = time.monotonic()
        elapsed_time = end_time - start_time
        article_params['time_execution'] = round(elapsed_time, 2)

def read_charged_dict_to_list(file_path, words_list):
    with open(file_path, 'r') as file:
        for line in file:
            words_list.append(line.strip())
    return words_list

async def process_article(morph, charged_words, url, article_parameters):
    article_params = {
        'url': url,
        'rate': None,
        'article_len': None
    }
    try:
        async with time_execution(article_params):
            async with timeout(TIMEOUT):
                if url == 'big_text_test':
                    await asyncio.sleep(TIMEOUT + 1)
                else:
                    async with aiohttp.ClientSession() as session:
                        html = await fetch(session, url)
                        text = sanitize(html, plaintext=True)
                text = await split_by_words(morph, text)
                article_rate = calculate_jaundice_rate(text, charged_words)
                article_params['url'] = url
                article_params['status'] = ProcessingStatus.OK.name
                article_params['rate'] = article_rate
                article_params['article_len'] = len(text)
    except asyncio.TimeoutError:
        article_params['status'] = ProcessingStatus.TIMEOUT.name
    except aiohttp.ClientResponseError:
        article_params['status'] = ProcessingStatus.FETCH_ERROR.name
    except ArticleNotFound:
        article_params['status'] = ProcessingStatus.PARSING_ERROR.name
    finally:
        article_parameters.append(article_params)

async def main(request, morph, words_list):
    urls = request.rel_url.query.get('urls').split(',')
    if len(urls) > MAX_URLS_IN_REQUEST:
        return web.json_response(
            data={"error": "too many urls in request, should be 10 or less"},
            content_type='text/plain'
        )
    article_parameters = []
    async with create_task_group() as tg:
        for url in urls:
            tg.start_soon(process_article, morph, words_list, url, article_parameters)
    return web.json_response(article_parameters, content_type='text/plain')



if __name__ == '__main__':
    negative_words_list = read_charged_dict_to_list('./charged_dict/negative_words.txt', words_list=[])
    morph = pymorphy2.MorphAnalyzer()
    app = web.Application()
    app.add_routes([web.get("/", partial(main, morph=morph, words_list=negative_words_list))])
    web.run_app(app)
