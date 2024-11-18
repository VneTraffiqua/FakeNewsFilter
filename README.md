# Фильтр желтушных новостей


Пока поддерживается только один новостной сайт - [ИНОСМИ.РУ](https://inosmi.ru/). Для него разработан специальный адаптер, умеющий выделять текст статьи на фоне остальной HTML разметки. Для других новостных сайтов потребуются новые адаптеры, все они будут находиться в каталоге `adapters`. Туда же помещен код для сайта ИНОСМИ.РУ: `adapters/inosmi_ru.py`.

В перспективе можно создать универсальный адаптер, подходящий для всех сайтов, но его разработка будет сложной и потребует дополнительных времени и сил.

# Как установить

Вам понадобится Python версии 3.7 или старше. Для установки пакетов рекомендуется создать виртуальное окружение.

Первым шагом установите пакеты:

```python3
pip install -r requirements.txt
```

# Как запустить

```python3
python server.py
```

## Как использовать

Выполните запрос к серверу, в параметрах запроса передайте список url со статьями (не больше 10 адресов)

Пример запроса:

```http
http://127.0.0.1:8080/?urls=https://inosmi.ru/20240628/drevnie-lyudi-269349491.html,https://inosmi.ru/20240629/kulisy-269369858.html
```

Пример ответа:

```json
[
  {
    "url": "https://lenta.ru/brief/2021/08/26/afg_terror/",
    "rate": null,
    "article_len": null,
    "time_execution": 1.11,
    "status": "PARSING_ERROR"
  },
  {
    "url": "https://inosmi.ru/not/exist.html",
    "rate": null,
    "article_len": null,
    "time_execution": 1.17,
    "status": "FETCH_ERROR"
  },
  {
    "url": "https://inosmi.ru/20241031/tramp-270579213.html",
    "rate": 0.5,
    "article_len": 798,
    "status": "OK",
    "time_execution": 2.55
  },
  {
    "url": "big_text_test",
    "rate": null,
    "article_len": null,
    "time_execution": 3.0,
    "status": "TIMEOUT"
  }
]
```


# Как запустить тесты

Для тестирования используется [pytest](https://docs.pytest.org/en/latest/), тестами покрыты фрагменты кода сложные в отладке: text_tools.py и адаптеры. Команды для запуска тестов:

```commandline
python -m pytest server.py 
```

```
python -m pytest adapters/inosmi_ru.py
```

```
python -m pytest text_tools.py
```

