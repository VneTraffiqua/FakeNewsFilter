from server import ProcessingStatus, read_charged_dict_to_list, process_article
import pymorphy2
import asyncio


def test_process_article():
    article_parameters = []
    negative_words_list = read_charged_dict_to_list('./charged_dict/negative_words.txt', words_list=[])
    morph = pymorphy2.MorphAnalyzer()
    urls = ["https://inosmi.ru/20241105/vybory-270639230.html",
            "https://inosmi.ru/not/exist.html",
            "https://lenta.ru/brief/2021/08/26/afg_terror/",]
    for url in urls[:4]:
        asyncio.run(process_article(morph, negative_words_list, url, article_parameters))

    assert article_parameters[0]["url"] == urls[0]
    assert article_parameters[0]["status"] == ProcessingStatus.OK.name
    assert article_parameters[0]["article_len"] == 997
    assert article_parameters[0]["rate"] == 1.2

    assert article_parameters[1]["url"] == urls[1]
    assert article_parameters[1]["status"] == ProcessingStatus.FETCH_ERROR.name
    assert article_parameters[1]["article_len"] is None
    assert article_parameters[1]["rate"] is None

    assert article_parameters[2]["url"] == urls[2]
    assert article_parameters[2]["status"] == ProcessingStatus.PARSING_ERROR.name
    assert article_parameters[2]["article_len"] is None
    assert article_parameters[2]["rate"] is None

def test_process_article_with_big_text():
    article_parameters = []
    negative_words_list = read_charged_dict_to_list('./charged_dict/negative_words.txt', words_list=[])
    morph = pymorphy2.MorphAnalyzer()

    asyncio.run(process_article(morph, negative_words_list, 'big_text_test', article_parameters))
    assert article_parameters[0]["url"] == 'big_text_test'
    assert article_parameters[0]["status"] == ProcessingStatus.TIMEOUT.name
    assert article_parameters[0]["article_len"] is None
    assert article_parameters[0]["rate"] is None
