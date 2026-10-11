# VseGPT — полная документация

Источник: https://vsegpt.ru/Docs/

---

# 1. API

## VseGPT : Документация по API

Источник: https://vsegpt.ru/Docs/API

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

   

Мы предоставляем **единое OpenAI-совместимое API для ВСЕХ нейросетей, включая OpenAI, Anthropic, Google, DeepSeek и пр.**   
   
**Для переключения на другую нейросеть** достаточно поменять идентификатор модели (Model ID) в запросе API или интерфейсе приложения. В случае, если имя модели жестко задано в вашем приложении, и его нельзя ввести вручную, вы можете настроить редирект модели в нужную вам в [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)ваших пользовательских настройках маппинга моделей на нашем сайте](https://vsegpt.ru/User/SettingsModels "User / Settings Models")  
   
**Доказательство того, что у нас хорошее OpenAI-совместимое API** – [готовые интеграции с множеством сторонних опенсорс приложений.](https://vsegpt.ru/ExtTools "Ext Tools")

  

**Оглавление документа**   
  

[Совместимое API](#h84-1)

[ОСНОВНОЕ OpenAI-совместимое API](#h84-2)

[Кастомные точки доступа API (баланс аккаунта, текст из PDF/DOCX, генерация видео)](#h84-3)

[Stable Diffusion API (A1111, Automatic)](#h84-4)

[Anthropic-совместимое API (бета)](#h84-5)

[Механика доступа по API и URL для подключений](#h84-6)

[Важно: при автоматизации следуйте Правилам хорошего бота, чтобы избежать блокировки](#h84-7)

  

## Совместимое API

  

### ОСНОВНОЕ OpenAI-совместимое API

  
В первую очередь **мы поддерживаем** только часть OpenAI API, касающуюся текстовых нейросетей – зато для самых разных нейросетей (v1/chat/completions).  
  
Также мы поддерживаем   

- v1/embeddings – модель для создания текстовых эмбеддингов
- v1/chat/completions для vision-нейросетей
- v1/images/generations, v1/images/edit – генерации картинок,
- v1/audio/transcriptions (speech to text)
- v1/audio/speech – генерации голоса (TTS),

  
Эндпойнт с НАШЕЙ (не OpenAI) реализацией:  

- v1/video/generate – генерация видео. Он разрабатывался до Sora 2, которая предложила API для генерации видео.

  
В планах поддержка:  

- поискового API (не OpenAI)

  
Нет планов на поддержку:  

- v1/assistants кастомных ассистенты и пр. – но вы можете использовать [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)наш пример реализации RAG (поиска по документам)](https://github.com/janvarev/demo_rag_vsegpt "Внешняя ссылка (откроется в новом окне)"), если вам нужна такая функциональность.
- v1/responses

  
Мы **не поддерживаем**  

- решения с сайта OpenAI (хотя для них есть [аналоги](https://vsegpt.ru/ExtTools "Ext Tools"))

### Кастомные точки доступа API (баланс аккаунта, текст из PDF/DOCX, генерация видео)

  
Поддерживается:  

- v1/balance – получение баланса и статуса аккаунта пользователя
- v1/extract\_text – получение текста из PDF/DOCX, включая OCR при необходимости
- v1/video/generate – для генерации видео (долгая)

  

### Stable Diffusion API (A1111, Automatic)

  
Поддерживается:  

- sdapi/v1/txt2img – генерация изображений

  
Полный адрес вызова: https://api.vsegpt.ru/sdapi/<ваш\_api\_ключ>/sdapi/v1/txt2img  
  
При вызове будет вызвана модель sdapi/txt2img – её по умолчанию не существует, надо вручную установить её существование в маппинге. Маппинг настраивается в [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Настройках пользователя](https://vsegpt.ru/User/SettingsModels "User / Settings Models")  
  
Например:  
sdapi/txt2img=img-stable/stable-diffusion-xl-lightning  
  
Пример использования в приложении: <https://vsegpt.ru/ExtTools/AIRoguelite#imggen>  

### Anthropic-совместимое API (бета)

  
**Позволяет использовать Claude Code с любыми моделями VseGPT**  
  

Проект в бете, может некорректно обрабатывать какие-то запросы. Также может некорректно возвращать для отображения в клиенте число токенов.

  
Anthropic-совместимое API позволяет делать запросы к любым моделям VseGPT. Поддерживается как стриминговый режим, так и нестриминговый.  
  
Про настройку Claude Code: <https://vsegpt.ru/ExtTools/ClaudeCode>  
  
Пример кода для прямого вызова:  

```
import requests
import json

# Настройки
API_URL = "https://services.vsegpt.ru:3000/v1/messages" 
API_KEY = "sk-or-v...."  # Ваш VseGPT API ключ

# Формируем запрос в формате Anthropic API
data = {
    "model": "openai/gpt-4o-mini",  # или другая модель
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": "Перечисли числа от 1 до 5"
        }
    ]
}
# Заголовки
headers = {
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY,
}
# Отправляем запрос
response = requests.post(API_URL, headers=headers, json=data)
# Проверяем статус
if response.status_code == 200:
    result = response.json()

    # Извлекаем текст ответа
    if result.get("content"):
        text = result["content"][0]["text"]
        print("Ответ модели:")
        print(text)
        print("\n" + "=" * 50)
        print("Полный ответ:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Ошибка: нет content в ответе")
        print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
```

  
  

## Механика доступа по API и URL для подключений

  
Поддерживается стандартный доступ по API OpenAI – вы можете использовать любые программы для доступа по нему.  
  
Не забудьте указать следующие кастомные параметры – **URL точки доступ и имя модели**:  
  
**URL:** https://api.vsegpt.ru/v1/chat/completions  

- В зависимости от программы, это может быть https://api.vsegpt.ru/v1 или ещё что-то, см. примеры в [![](https://vsegpt.ru/themes/bs5vsegpt/icons/file.gif)Руководстве по подключению сторонних инструментов](https://vsegpt.ru/pdfs/custom_tool.pdf)

  
также поддерживается старый URL на другом порту [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://api.vsegpt.ru:6070/](https://api.vsegpt.ru:6070/ "Внешняя ссылка (откроется в новом окне)"), который можно увидеть в некоторых примерах подключения  
  
**model:** id модели из [списка моделей](https://vsegpt.ru/Docs/Models "Docs / Models")  

- Вы можете поменять только ID модели при запросе и перенаправить запрос к Antropic Claude, Google или опенсорс моделям, не меняя остальные поля в запросе. Мы поддерживаем **единый интерфейс для всех моделей**.
- Допускается указание стандартных идентификаторов gpt-3.5-turbo, gpt-4 – они будут автоматически преобразованы в соответствующие полные ID моделей OpenAI в большинстве случаев.
- Также возможно автоматическое преобразование ваших моделей в новые идентификаторы, если вы настроите маппинг моделей в [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Настройках](https://vsegpt.ru/User/SettingsModels "User / Settings Models")

  

### Важно: при автоматизации следуйте Правилам хорошего бота, чтобы избежать блокировки

  

Чтобы наше API работало хорошо, мы просим вас придерживаться [Правил хорошего бота](https://vsegpt.ru/Tutorials/GoodBotRules "Tutorials / Good Bot Rules"), иначе мы можем временно ограничить ваш доступ к API

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Документация по API - особенности реализации и дополнительные возможности

Источник: https://vsegpt.ru/Docs/API/AddFeatures

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

 

[Дополнительные возможности](#h221-1)

[Поддержка function calls (УСТАРЕЛО)](#h221-2)

[Поддержка tools (РЕКОМЕНДУЕТСЯ, поддерживаются и другие модели при записи tools в OpenAI-формате)](#h221-3)

[Поддержка structured outputs (РЕКОМЕНДУЕТСЯ, поддерживаются и другие модели при записи в OpenAI-формате)](#h221-4)

[Поддержка MCP (Model Context Protocol)](#h221-5)

[Модификаторы модели (фича VseGPT)](#h221-6)

[nojsonencode – не кодировать ответ в json в ascii](#h221-7)

[x-title – установить x-title в запросе для статистики](#h221-8)

  

## Дополнительные возможности

  

### Поддержка function calls (УСТАРЕЛО)

  

С 20 августа 2024 функциональность function calls, как [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)устаревшая версия tool calls](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling "Внешняя ссылка (откроется в новом окне)"), больше не работает. Пожалуйста, используйте tool calls для реализации.

  
**У нас добавлена поддержка function calling вызовов OpenAI – в том числе для части опенсорс моделей!**  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://openai.com/blog/function-calling-and-other-api-updates](https://openai.com/blog/function-calling-and-other-api-updates "Внешняя ссылка (откроется в новом окне)")  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://cookbook.openai.com/examples/how\_to\_call\_functions\_with\_chat\_models](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models "Внешняя ссылка (откроется в новом окне)")  
  
Такой вызов просит OpenAI модель вывести json, соответствующий одной из предложенных функций. Например, можно подать на вход функцию “get\_current\_weather” – и выходом модели будет json “get\_current\_weather” с параметрами, соответствующими текущему пользовательскому текстовому запросу (см. примеры по ссылке)  
  
Поддерживаются модели:   

- OpenAI openai/gpt-3.5-turbo, gpt4, и, возможно другие (ответ будет в элементе function\_call)
- jondurbin/airoboros-l2–70b (ответ будет в элементе content)

  
Также на практике и множество других моделей поддерживают function calls (Claude и пр.), но их поддержка не задекларирована, так что используйте на свой страх и риск. У автора работали anthropic/claude-instant-v1, openchat/openchat-7b, gryphe/mythomax-L2–13b и пр.  
  
Пример вызова:  

```
#
    prompt = "What is the weather like in Boston?"

    messages = []
    #messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(

        model="openai/gpt-3.5-turbo",
        # model="jondurbin/airoboros-l2-70b",
        messages =messages,
        temperature=0.9,
        n=1,
        max_tokens = 1500,
        stream=stream,
        functions=[
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
    )
```

  
  

  

### Поддержка tools (РЕКОМЕНДУЕТСЯ, поддерживаются и другие модели при записи tools в OpenAI-формате)

  
Аналогично предыдущему.  
  

Tool calls поддерживается моделями, у которых есть бедж tools в списке моделей – их более 20, включая опенсорс модели. Вы можете зайти в список моделей по новизне, и отфильтровать модели по слову tools.  
   
У не OpenAI-моделей могут быть незначительные несовестимости с форматом, но наши базовые тесты показывают совместимость.

  
Пример вызова:  

```
#
    prompt = "What is the weather like in Boston?"

    messages = []
    #messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(

        model="openai/gpt-3.5-turbo",
        messages =messages,
        temperature=0.1,
        n=1,
        max_tokens = 1500,
        stream=False,
        tool_choice="auto",
        tools = [{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
        ]
    )
```

  
  

  

### Поддержка structured outputs (РЕКОМЕНДУЕТСЯ, поддерживаются и другие модели при записи в OpenAI-формате)

  
Аналогично предыдущему.  
  

Structured outputs поддерживается моделями, у которых есть бедж structured-outputs в списке моделей – включая опенсорс модели. Вы можете зайти в список моделей по новизне, и отфильтровать модели по слову structured-outputs. Обычно поддерживаются OpenAI модели, и последние модели Google (Gemini Flash 3, Gemini Pro 3)  
   
У не OpenAI-моделей могут быть незначительные несовестимости с форматом, но наши базовые тесты показывают совместимость.

  
Для ознакомления рекомендуем ознакомиться со статьей: [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://cookbook.openai.com/examples/structured\_outputs\_intro](https://cookbook.openai.com/examples/structured_outputs_intro "Внешняя ссылка (откроется в новом окне)")  
  
Базовый пример  

```
def test_structured_outputs(model:str) -> dict:
    math_tutor_prompt = '''
        You are a helpful math tutor. You will be provided with a math problem,
        and your goal will be to output a step by step solution, along with a final answer.
        For each step, just provide the output as an equation use the explanation field to detail the reasoning.
    '''

    prompt = "There are equation 'x+3=8'. Find the integer 'x'"

    messages = []

    messages.append({"role": "system", "content": math_tutor_prompt})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        headers={
            "X-Title": "Test structured outputs"
        },
        model=model,
        messages=messages,
        temperature=0.1,
        n=1,
        max_tokens=500,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"}
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False
                            }
                        },
                        "final_answer": {"type": "integer"}
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }

    )
    print("Response:", response)
    response1 = response["choices"][0]["message"] # будет содержать content, в котором нужный JSON со структурой

    # response_text: str = str(response1).strip()
    return response1
```

  

### Поддержка MCP (Model Context Protocol)

  
Наши нейросети c tools эффективно поддерживают Model Context Protocol.  
См. описание здесь: <https://vsegpt.ru/ExtTools/CherryStudio>  
  
Также мы поддерживаем доступ к части функциональности с помощью MCP Servers for VseGPT:  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://github.com/janvarev/mcp-vsepgt-server](https://github.com/janvarev/mcp-vsepgt-server "Внешняя ссылка (откроется в новом окне)")  
  

  

## Модификаторы модели (фича VseGPT)

  
**Модификаторы** – это прием, позволяющий **без изменения кода приложения** добавить некие функции в вызов путем изменения ID модели.  
  
Общая логика использования модификаторов: **вы пишете model id, а затем, через двоеточие – неограниченное число модификаторов, разделяемых двоеточием**.  
  
Примеры:  
gpt-4:mod1:mod2  
openai/gpt-4o-mini:x-title=My Test Mod  
  
и прочее.  
  
Список поддерживаемых модификаторов и их описание – ниже.  
  

### nojsonencode – не кодировать ответ в json в ascii

  
**Смысл**: ответ в json приходит в виде закодированных русских строк (потому что по стандарту если ensure\_ascii, то нужно пользовать только ascii в ответе). Это не всегда удобно для отладки + некоторые приложения это некорректно поддерживают. Добавление модификатора ОТКЛЮЧАЕТ кодирование в JSON всего не-ascii в ascii. Это может создать проблемы для каких-то приложений, но обычно нет.  
  
**Пример использования:** openai/gpt-4o-mini:nojsonencode  

  
  

### x-title – установить x-title в запросе для статистики

  
**Смысл**: в Статистике использования на сайте можно увидеть, от каких приложений идут запросы. Обычно, чтобы приложение это сказало, ему надо установить заголовок X-Title – но не все приложения это делают.  
Теперь можно вручную, задав Model ID сказать, что запрос пришел от такого-то приложения, чтобы в статистике это показывалось более корректно.  
  
**Пример использования:** openai/gpt-4o-mini:x-title=Chat GPT Box  
  
**Ограничения:**   
1. Используйте английские буквы/цифры/знаки препинания для задания x-title – иначе будет ошибка  
2. Если приложение УЖЕ передает свой X-Title, вы его не сможете перезаписать

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Документация по API

Источник: https://vsegpt.ru/Docs/API/Code

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

 

[ГОТОВЫЕ ПРИМЕРЫ в Google Colab](#h82-1)

[Пример вызова API (Python, CURL)](#h82-2)

[Генерация текста (chat/completions)](#h82-3)

[Поддержка диалога](#h82-4)

[Генерация текста с Web search](#h82-5)

[Получение размышлений в reasoning моделях (o1,R1)](#h82-6)

[Получение ответа в виде JSON](#h82-7)

[Генерация Embedding](#h82-8)

[Embedding в LangChain](#h82-9)

[Vision-модель (распознавание картинок, OCR) (текст+картинка -> текст)](#h82-10)

[Загрузка картинки из локального файла](#h82-11)

[Отправка нескольких изображений](#h82-12)

[Подача на вход аудиофайла (фича audioinput)](#h82-13)

[Генерация изображения](#h82-14)

[Редактирование изображения](#h82-15)

[Альтернативный OpenAI-совместимый вариант через v1/images/edits](#h82-16)

[Распознавание речи](#h82-17)

[Генерация речи (Text-to-Speech)](#h82-18)

[Конвертация документов в текст (utils/extract-text)](#h82-19)

[Генерация видео (Text-to-Video)](#h82-20)

[Генерация видео по картинке (Image-to-Video)](#h82-21)

[Генерация музыки (Text-to-Audio)](#h82-22)

[Получение баланса (Python)](#h82-23)

[Получение информации о доступных моделях](#h82-24)

[Сторонние библиотеки и примеры на других языках (CURL, NodeJS)](#h82-25)

[С# (async)](#h82-26)

[TypeScript](#h82-27)

[TypeScript (OpenAI library)](#h82-28)

[Библиотеки для других языков](#h82-29)

[Библиотека для работы с VseGPT для Go](#h82-30)

  

## ГОТОВЫЕ ПРИМЕРЫ в Google Colab

  
[![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Ссылки на блокноты с примерами](https://vsegpt.ru/Docs/API/Colabs "Docs / API / Colabs")  

- Базовый пример – вызов gpt-4o-mini
- Работа с большим текстом – поиск по текстовой базе знаний с помощью эмбеддингов (RAG)

  

## Пример вызова API (Python, CURL)

  

### Генерация текста (chat/completions)

  

Примеры даны для Python и CURL. [Другие языки здесь](https://vsegpt.ru/Docs/API/Code "Docs / API / Code").

  

- [Python, openai==1.x](#wikiTab1)
- [Python, requests](#wikiTab2)
- [CURL](#wikiTab3)

```
from openai import OpenAI

client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

prompt = "Напиши последовательно числа от 1 до 10"

messages = []
#messages.append({"role": "system", "content": system_text})
messages.append({"role": "user", "content": prompt})

response_big = client.chat.completions.create(
    model="anthropic/claude-3-haiku", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
    messages=messages,
    temperature=0.7,
    n=1,
    max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
    extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
)

#print("Response BIG:",response_big)
response = response_big.choices[0].message.content
print("Response:",response)
```

```
import requests
import json

# Выполнение POST запроса
response = requests.post(
    "https://api.vsegpt.ru/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {VSEGPT_KEY}",
        "Content-Type": "application/json",
        "X-Title": "File analysis demo" # опционально - передача информация об источнике API-вызова
    },
    json={
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "system", "content": context_prompt},
                     {"role": "user", "content": question}]
    }
)

# Обработка ответа
response_data = response.json()
msg = response_data["choices"][0]["message"]["content"]

print("Ответ:", msg)
```

```
curl https://api.vsegpt.ru/v1/chat/completions
  -H "Content-Type: application/json"
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'
```

  
  

#### Поддержка диалога

  
Для поддержки диалога вы должны сохранять диалог в массив messages, а затем каждый раз подавать его на вход в запросе к модели.  
  
Пример:  

```
# Ход 1
messages = [
   {"role": "user", "content": "Кто такой Барак Обама?"}
]

# Получили ответ - "Барак Обама - президент США"
# добавляем его в массив с ролью assistant
# задаем еще вопрос - "Кто его жена?"

# Ход 2 - здесь запрос Кто его жена? будет обработан в контексте
messages = [
   {"role": "user", "content": "Кто такой Барак Обама?"},
   {"role": "assistant", "content": "Барак Обама - президент США"},
   {"role": "user", "content": "Кто его жена?"}
]
```

  
  

#### Генерация текста с Web search

  
Модели Perplexity на нашем сайте поддерживают chat completions с выполнением веб-поиска актуальной информации и возвращением ссылок.  
  
Для деталей обратитесь к:  

- Описанию моделей Perplexity в Моделях
- Примеру клиента с поиском (Сервисы > Чат с веб поиском)
- Документации Perplexity – [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://docs.perplexity.ai/api-reference/chat-completions](https://docs.perplexity.ai/api-reference/chat-completions "Внешняя ссылка (откроется в новом окне)")

#### Получение размышлений в reasoning моделях (o1,R1)

  
o1 и o3 не поддерживает получение размышлений; только ответов  
Deepseek R1, Sonnet 3.7, QwQ 32 дают ответ в одном из полей ответа (reasoning):  

```
"choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The numbers from 1 to 5 written sequentially are:  \n1, 2, 3, 4, 5.",
        "reasoning": "Okay, let's see. The user wants me to write the numbers from 1 to 5 in order. That sounds straightforward, but I should make sure I do it correctly. Let me start by recalling the sequence of numbers.\n\nFirst, 1 is the starting point. Then comes 2, followed by 3. After that, it's 4 and then 5. Wait, is there any chance I might mix up the order? I don't think so. Numbers from 1 to 5 are pretty basic. Let me count them again in my head to double-check: 1, 2, 3, 4, 5. Yep, that's five numbers, each increasing by one. \n\nHmm, maybe the user wants them listed each on a separate line or separated by commas. The instruction says \"sequentially,\" so probably just one after the other. The example didn't specify formatting, but to be clear, I should present them in a simple sequence. Let me write them out: 1, 2, 3, 4, 5. \n\nWait, but maybe they want each number written out as a word? Like one, two, three, four, five. The original query says \"numbers,\" which could be interpreted either way. But since it's about writing the numbers, not the words, digits are more likely expected. \n\nAlternatively, maybe they want a vertical list. But the example response the assistant is supposed to generate uses commas. Let me check the user's exact request again: \"Write the numbers from 1 to 5 sequentially.\" The key word is \"sequentially,\" which just means in order. So the simplest way is to list them in order separated by commas. \n\nI think that's all. No complications here. Just make sure not to skip any number or repeat any. Let me verify once more: starting at 1, each subsequent number increases by 1 until 5. So 1, then 2, then 3, then 4, then 5. No mistakes there. Alright, ready to present the answer."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
```

  

#### Получение ответа в виде JSON

  
**Вариант 1** – подходит для большинства нейросетей, но не дает никаких гарантий (для гарантий смотрите Вариант 2).   

1. Напишите промт, в котором явно указываете, что ожидаете в ответе JSON.
2. (Опционально) Добавьте указание response\_format={ “type”: “json\_output” } в запросе, некоторые поставщики учитывают это и стараются вернуть вам JSON.

  

**Важно:** Этот способ не дает никаких гарантий, что в ответе будет JSON – тем не менее, если промт написан правильно, и нейросеть может вернуть осмысленный ответ – она его чаще всего вернет в JSON, причем чем умнее сеть, тем чаще так будет.

  
Пример:  

```
math_tutor_prompt = '''
        You are a helpful math tutor. You will be provided with a math problem,
        and your goal will be to output an answer.
    '''

    prompt = "There are equation 'x+3=8'. Find the integer 'x'. Answer with ONLY JSON dictionary with final 'x', where 'x' is key of dictionary, and value of key is answer. "

    messages = []

    messages.append({"role": "system", "content": math_tutor_prompt})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        headers={
            "X-Title": "Test (no-stream, json_output)"
        },
        model=model,
        messages=messages,
        temperature=0.01,
        max_tokens=4000,
        response_format={
            "type": "json_output"
        }
    )
```

  
  
**Вариант 2** – рекомендуется, но не работает для всех сетей. Используйте механизм [structured outputs](#structuredoutputs) (если ссылка не работает, найдите ее через меню). Нейросети, поддерживающие этот механизм, имеют специальный бейдж (наряду c tools). **Этот механизм позволяет формально записать требуемую схему ответа JSON и ожидать, что ответ будет ей соответствовать.**   
  

### Генерация Embedding

  

- [Python, openai==1.x](#wikiTab4)
- [CURL](#wikiTab5)

```
from openai import OpenAI
client = OpenAI(
  api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

client.embeddings.create(
  model="text-embedding-ada-002",
  input="The food was delicious and the waiter...",
  encoding_format="float"
)
```

```
curl https://api.vsegpt.ru/v1/embeddings
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -H "Content-Type: application/json"
  -d '{
    "input": "The food was delicious and the waiter...",
    "model": "text-embedding-ada-002",
    "encoding_format": "float"
  }'
```

  

#### Embedding в LangChain

  
В model указывается ID эмбеддингов из списка моделей (по умолчанию 'text-embedding-ada-002', и это будет обработано)  
  

```
from langchain_openai import OpenAIEmbeddings

model = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_base = "https://api.vsegpt.ru/v1/")
```

  
  
Ссылка на документацию: [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://api.python.langchain.com/en/latest/embeddings/langchain\_openai.embeddings.base.OpenAIEmbeddings.html](https://api.python.langchain.com/en/latest/embeddings/langchain_openai.embeddings.base.OpenAIEmbeddings.html "Внешняя ссылка (откроется в новом окне)")  
  

### Vision-модель (распознавание картинок, OCR) (текст+картинка -> текст)

  

**Внимание:** для корректной тарификации стоимости картинок используйте Vision-варианты сетей (начинаются с префикса vis-, у них отдельный раздел в Моделях). Иначе ваш запрос либо не пройдет по причине стоимости, либо будет слишком дорогим.

  
Вариант с указанием картинки по URL (если картинка не будет найдена, или будет заблокирована, получите ошибку в духе openai.error.InvalidRequestError: Unknown MIME type)  
  

- [Python, openai==1.x](#wikiTab6)
- [CURL](#wikiTab7)

```
from openai import OpenAI
client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

response = client.chat.completions.create(
    model="vis-google/gemini-flash-1.5",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What you think the person in the image is doing?"},
                {
                    "type": "image_url",
                    "image_url": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA18Lnc8.img?w=1920&h=1080&q=60&m=2&f=jpg",
                },
            ],
        }
    ],
    max_tokens=400,
)

print(response.choices[0])
```

```
curl https://api.vsegpt.ru/v1/chat/completions
  -H "Content-Type: application/json"
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -d '{
    "model": "vis-google/gemini-flash-1.5",
    "messages": [
      {
        "role": "user",
        "content": [
                {"type": "text", "text": "What you think the person in the image is doing?"},
                {
                    "type": "image_url",
                    "image_url": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AA18Lnc8.img?w=1920&h=1080&q=60&m=2&f=jpg"
                }
        ]
      }
    ],
    "max_tokens": 400
  }'
```

  

#### Загрузка картинки из локального файла

  
Вариант с загрузкой картинки из локального файла (вариант для openai=0.28.1, для 1.x решается соответствующей заменой функций для передачи картинки)  
  

```
import openai
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

openai.api_key = "sk-XXXXXXXXXXXXXXXX" # ваш ключ в VseGPT после регистрации

openai.api_base = "https://api.vsegpt.ru/v1"

base64_image = encode_image("Einstein.jpg")
messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What you think the person in the image is doing?"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ]

response_big = openai.ChatCompletion.create(
    model="vis-google/gemini-pro-vision",
    messages=messages,
    temperature=0.8,
    n=1,
    max_tokens=300,
)

#print("Response BIG:",response_big)
response = response_big["choices"][0]["message"]
print("Response:",response)
```

  

#### Отправка нескольких изображений

  
Нужно сконструировать messages, например, следующим образом:  
  

```
messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Image 1"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image1}",
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Image 2"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image2}",
                },
            ],
        },
        {
            "role": "user",
            "content": "Какая разница между этими двумя изображениями?"
        }
    ]
```

  

#### Подача на вход аудиофайла (фича audioinput)

  
Фича audioinput позволяет обычной текстовой модели принять на вход также аудиофайл.  
  

```
import openai
import base64

def encode_mp3(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

openai.api_key = "sk-XXXXXXXXXXXXXXXX" # ваш ключ в VseGPT после регистрации

openai.api_base = "https://api.vsegpt.ru/v1"

base64_mp3 = encode_mp3("test_rec.mp3")
messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": base64_mp3,
                        "format": "mp3"
                    }
                },
                {"type": "text", "text": "Please transcribe this audio file."},

            ],
        }
    ]

response_big = openai.ChatCompletion.create(
    model="google/gemini-3.1-flash-lite-pre",
    messages=messages,
    temperature=0.8,
    n=1,
    max_tokens=300,
)

#print("Response BIG:",response_big)
response = response_big["choices"][0]["message"]
print("Response:",response)
```

  
  

### Генерация изображения

  

- [Python, openai==1.x](#wikiTab8)
- [CURL](#wikiTab9)

```
from openai import OpenAI
client = OpenAI(
  api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

client.images.generate(
  model="dall-e-3",
  prompt="An astronaut riding the horse on the Moon.",
  n=1,
  size="1024x1024"
  # aspect_ratio="1:1" 
  # ряд моделей, типа Imagen 4, требуют указания aspect_ratio вместо size. Смотрите карточку модели
)
```

```
curl https://api.vsegpt.ru/v1/images/generations   
  -H "Content-Type: application/json"   
  -H "Authorization: Bearer $VSEGPT_API_KEY"   
  -d '{
    "model": "dall-e-3",
    "prompt": "An astronaut riding the horse on the Moon.",
    "n": 1,
    "size": "1024x1024"
  }'
```

  
  
Полный код для работы с разными моделями с получением результатов в base64\_json и их декодированием: [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)Github MCP Server for image generation](https://github.com/janvarev/mcp-vsepgt-server/blob/main/mcp_gen_image.py "Внешняя ссылка (откроется в новом окне)")  
  

  

### Редактирование изображения

  

```
import base64
import os
from pathlib import Path

import time

import requests

api_key = "your_vsegpt_key"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image("test_car.png")

# Create API session
session = requests.Session()

# Set up authorization headers
session.headers.update({
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
})

# VseGPT API endpoint for image generation
url = "https://api.vsegpt.ru/v1/images/generations"

# Prepare payload as specified
payload = {
    "model": "img2img-google/flash-edit",
    "prompt": "Make the car black",
    "response_format": "b64_json",
    "image_url": f"data:image/jpeg;base64,{base64_image}",
    # в случае нескольких изображений, например, для flash-edit-multi 
    # используйте также image2_url, image3_url, image4_url - вплоть до image10_url 
    # (смотрите возможности нейросети по числу входных изображений)
}
# Update headers with title
session.headers.update({"X-Title": f"Test Image-to-Image"})
# Make the API request
response = session.post(url, json=payload)
# Check if request was successful
if response.status_code == 200:
    # Saving image to file

    # Get base64 string from response
    response_json = response.json()
    print(response_json)
    b64_data = response_json["data"][0]["b64_json"]

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create tmp_images directory in the same folder as the script
    tmp_dir = Path(script_dir) / "tmp_images"
    tmp_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp
    timestamp = int(time.time())
    filename = f"{timestamp}.jpg"
    filepath = tmp_dir / filename

    # Decode base64 and save to file
    with open(filepath, "wb") as img_file:
        img_file.write(base64.b64decode(b64_data))

    # Return absolute path to the file
    # return str(filepath.absolute())
    print("File here: ",str(filepath.absolute()))
else:
    raise ValueError(f"{response.status_code}: {response.text}")
```

  

#### Альтернативный OpenAI-совместимый вариант через v1/images/edits

  
Мы также поддерживаем редактирование через endpoint v1/images/edits, в целях совместимости с [Cherry Studio](https://vsegpt.ru/ExtTools/CherryStudio "Ext Tools / Cherry Studio") и библиотеками OpenAI в целом.  
  
Тем не менее, чтобы система лучше работала в Cherry Studio, мы используем трюк – к присланному ID модели добавляется “-imgedit”, чтобы была возможность перенаправить запрос в любую интересующую вас модель редактирования изображений.  
  
Так что для вам нужно будет настроить маппинг, если вы хотите использовать этот эндпойнт (см. пример для [Cherry Studio](https://vsegpt.ru/ExtTools/CherryStudio "Ext Tools / Cherry Studio") )  

### Распознавание речи

  

- [Python, openai==1.x](#wikiTab10)
- [CURL](#wikiTab11)
- [CURL с диаризацией](#wikiTab12)

```
from openai import OpenAI
client = OpenAI(
  api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
  base_url="https://api.vsegpt.ru/v1",
)

audio_file = open("speech.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model = "stt-openai/whisper-1",
  response_format="json",
  language="ru", # опционально, может быть пустым
  file=audio_file
)
```

```
curl https://api.vsegpt.ru/v1/audio/transcriptions
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -H "Content-Type: multipart/form-data"
  -F file="@/path/to/file/audio.mp3"
  -F model="stt-openai/whisper-1"
  -F response_format="json"
```

```
curl https://api.vsegpt.ru/v1/audio/transcriptions
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -H "Content-Type: multipart/form-data"
  -F file="@/path/to/file/audio.mp3"
  -F language="ru"
  -F model="stt-deepgram/nova-3-diarize"
  -F response_format="verbose_json"
```

  
  

### Генерация речи (Text-to-Speech)

  

- [Python, openai==1.x](#wikiTab13)
- [CURL](#wikiTab14)

```
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-openai/tts-1",
    voice="nova", # поддерживаются голоса alloy, echo, fable, onyx, nova и shimmer
    input="Сегодня на улице очень жарко, не так ли?",
    # response_format="wav" # другой формат, при необходимости
)

response.write_to_file(speech_file_path)
```

```
curl https://api.vsegpt.ru/v1/audio/speech
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -H "Content-Type: application/json"
  -d '{
    "model": "tts-1",
    "input": "The quick brown fox jumped over the lazy dog.",
    "voice": "alloy"
  }'
  --output speech.mp3
```

  
  

  

### Конвертация документов в текст (utils/extract-text)

  

- [Python, requests](#wikiTab15)

```
import requests
import base64

# Кодируем файл в base64
with open("example.pdf", "rb") as file:
    encoded_file = base64.b64encode(file.read()).decode('utf-8')

# Отправляем запрос
response = requests.post(
    "https://api.vsegpt.ru/v1/extract_text",
    headers = {
        "Authorization": "Bearer VSEGPT_API_KEY", # ваш ключ vsegpt
        "X-Title": "Doc2Text example" # опционально
    },
    json={
        "encoded_base64_file": encoded_file,
        "filename": "example.pdf",
        "model": "utils/extract-text-1.0", # вариант - utils/pdf-ocr-1.0 для оптического распознавания OCR
        # "return_images": True, # для utils/pdf-ocr-1.0 также возвращает картинки в base64
    }
)

# print(response.text)

response.raise_for_status()

# Получаем результат
print(response.json()["text"])
```

  
  

### Генерация видео (Text-to-Video)

  
Общая логика:  

- Сначала идет обращение на /v1/video/generate – ставим задачу на генерацию видео, получаем request\_id в ответе.
- Далее каждые 10 секунд (можно больше) обращаемся на /v1/video/status?request\_id=<request\_id> и api key для получения статуса и URL результата.
- Когда status=COMPLETED, можно получить URL и по нему скачать видео

  

```
import requests
import json
import time
from datetime import datetime, timedelta

api_key = "your_vsegpt_api_key"

def generate_and_wait_video(prompt, model_id="txt2vid-kling/standart", aspect_ratio="16:9",
                            timeout_minutes=20):
    base_url = "https://api.vsegpt.ru/v1/video"

    # Заголовки запроса для генерации
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Тело запроса
    payload = {
        "model": model_id,
        "action": "generate",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration": 0 # для моделей, поддерживающих указание числа секунд нужно это заполнить. 0 будет означать дефолтовое значение
    }

    # Запоминаем время начала генерации
    start_time = datetime.now()

    # Выполнение POST запроса для генерации
    response = requests.post(
        url=f"{base_url}/generate",
        headers=headers,
        json=payload
    )

    # Проверка статус кода
    if response.status_code != 200:
        print('ERROR', response.status_code, response.text)
        return

    # Получение request_id
    response_data = response.json()
    request_id = response_data.get('request_id')

    if not request_id:
        raise Exception("Failed to get request_id")

    print(f"Generation started with request_id: {request_id}")
    print(f"Using model: {model_id}")
    print(f"Aspect ratio: {aspect_ratio}")

    # Заголовки для проверки статуса
    status_headers = {
        "Authorization": f"Key {api_key}"
    }

    # Установка времени окончания ожидания
    timeout_time = datetime.now() + timedelta(minutes=timeout_minutes)

    # Цикл проверки статуса
    while datetime.now() < timeout_time:
        # Запрос статуса
        status_response = requests.get(
            url=f"{base_url}/status?request_id={request_id}",
            headers=status_headers
        )

        status_data = status_response.json()
        status = status_data.get('status')
        video_url = status_data.get('url')

        # Вычисляем прошедшее время
        elapsed_time = datetime.now() - start_time
        elapsed_minutes = elapsed_time.total_seconds() / 60

        print(f"Current status: {status} (Elapsed time: {elapsed_minutes:.1f} minutes)")

        if status == 'COMPLETED':
            print(f"Video generated successfully!")
            print(f"Total generation time: {elapsed_minutes:.1f} minutes")
            print(f"Video URL: {video_url}")
            return video_url

        elif status == 'FAILED':
            raise Exception(f"Video generation failed after {elapsed_minutes:.1f} minutes")

        # Ждем 10 секунд перед следующей проверкой
        time.sleep(10)

    # Если вышли из цикла по таймауту
    elapsed_time = datetime.now() - start_time
    elapsed_minutes = elapsed_time.total_seconds() / 60
    raise Exception(f"Timeout after {elapsed_minutes:.1f} minutes")

# Примеры использования
try:
    # Использование с указанием конкретной модели
    video_url = generate_and_wait_video(
        prompt="Panda playing guitar in the middle of Paris.",
        model_id="txt2vid-kling/standart",
        aspect_ratio="9:16"

    )

    # Использование с указанием модели и таймаута
    # video_url = generate_and_wait_video(
    #     prompt="Panda playing guitar in the middle of Manhattan.",
    #     model_id="txt2vid-kling/standart",
    #     timeout_minutes=30
    # )

except Exception as e:
    print(f"Error: {e}")
```

  

#### Генерация видео по картинке (Image-to-Video)

  
Аналогично предыдущему, только надо добавить еще   
  

```
def encode_image_to_base64(image_file):
    """Кодирует загруженное изображение в base64"""
    return base64.b64encode(image_file.read()).decode('utf-8')

# Добавляем в JSON запроса указание картинки
payload["image_url"] = f"data:image/jpeg;base64,{image_base64}"

# Если модель поддерживает - добавляем в JSON запроса указание последнего фрейма видео
payload["end_image_url"] = f"data:image/jpeg;base64,{end_image_base64}"
```

  

### Генерация музыки (Text-to-Audio)

  

- [Python, openai==1.x](#wikiTab16)
- [CURL](#wikiTab17)

```
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

response = client.audio.speech.create(
    extra_body={
        "seconds_total": 10 # число секунд для генерации
    },
    voice="nova", # не используется, но требуется библиотекой
    model="tta-stable/stable-audio",
    response_format="wav", # всегда WAV, другие не поддерживаются
    input="128 BPM, techno drum music",
)

response.write_to_file(music_wav_file)
```

```
curl https://api.vsegpt.ru/v1/audio/speech
  -H "Authorization: Bearer $VSEGPT_API_KEY"
  -H "Content-Type: application/json"
  -d '{
    "model": "tta-stable/stable-audio",
    "input": "128 BPM, techno drum music",
    "seconds_total": 10
  }'
  --output music.wav
```

  
  

### Получение баланса (Python)

  
Получение баланса должно быть включено в [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)настройках пользователя](https://vsegpt.ru/User/SettingsModels "User / Settings Models").  
  
Также в настройках можно указать лимит средств, после которого API будет возвращать состояние 1 – yellow, предупреждение о возможно недостаточном количестве средств.  
  
Возвращаемые данные:  

```
{
 "status":"ok", # общий статус запроса
 "data":{
   "credits":"10.752448", # остаток на балансе
   "subscription_status":"ok", # статус подписки (должен быть ok - это означает, что подписка работает)
   "subscription_end":"2024-05-02 00:08:02" # формальное время окончания подписки, МСК
   "user_status":1, # статус пользователя 0 - green, 1 - yellow (меньше средств, чем указано в настройках), 2 - red (аккаунт неработоспособен). 
   "user_status_text":"Less than 500 credits on account. " # в случае, если status не 0 - причина.
}}
```

  
  
**В принципе, достаточно отслеживать, чтобы user\_status все время был 0.** При любых ошибках и проблемах информация будет передана в поле user\_status\_text.   
  
**Пример запроса на Python**  
  

```
import requests
    import json
    response = requests.get(
        url="https://api.vsegpt.ru/v1/balance",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
    )

    # print(response.text)

    if response.status_code == 200:
        response_big = json.loads(response.text)
        if response_big.get("status") == "ok":
            credits = float(response_big.get("data").get("credits"))
        else:
            raise response_big.get("reason") # reason of error
    else:
        raise ValueError(str(response.status_code) + ": " + response.text)
```

  
  

### Получение информации о доступных моделях

  
Обратитесь к URL [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://api.vsegpt.ru/v1/models](https://api.vsegpt.ru/v1/models "Внешняя ссылка (откроется в новом окне)")  
  

## Сторонние библиотеки и примеры на других языках (CURL, NodeJS)

### С# (async)

  
Пример прислан одним из наших пользователей  
  

```
static async Task Main()
        {

            string apiKey = "sk-or-vv-86*************"; // ваш ключ в VseGPT после регистрации
            string baseApiUrl = "https://api.vsegpt.ru/v1/";
            string prompt = "Напиши последовательно числа от 1 до 10";

            try
            {
                HttpClient client = new HttpClient();
                client.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}");

                List<dynamic> messages = new List<dynamic>();
                messages.Add(new { role = "user", content = prompt });

                var requestData = new
                {
                    model = "openai/gpt-4o-mini",
                    messages = messages,
                    temperature = 0.7,
                    n = 1,
                    max_tokens = Convert.ToInt32(prompt.Length * 1.5),
                    extra_headers = new { X_Title = "My App" } // опционально - передача информации об источнике API-вызова
                };

                var jsonRequest = Newtonsoft.Json.JsonConvert.SerializeObject(requestData);
                var content = new StringContent(jsonRequest, Encoding.UTF8, "application/json");

                var response = await client.PostAsync(baseApiUrl + "chat/completions", content);

                if (response.IsSuccessStatusCode)
                {
                    var jsonResponse = await response.Content.ReadAsStringAsync();
                    dynamic responseData = Newtonsoft.Json.JsonConvert.DeserializeObject(jsonResponse);
                    string responseContent = responseData.choices[0].message.content;
                    Console.WriteLine("Response: " + responseContent);
                }
                else
                {
                    Console.WriteLine("Error: " + response.ReasonPhrase);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Exception: " + ex.Message);
            }
}
```

  

### TypeScript

```
fetch("https://api.vsegpt.ru/v1/chat/completions", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${VSEGPT_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    "model": "openai/gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "What is the meaning of life?"}
    ]
  })
});
```

  

### TypeScript (OpenAI library)

  

```
import OpenAI from "openai"

const openai = new OpenAI({
  baseURL: "https://api.vsegpt.ru/v1",
  apiKey: $VSEGPT_API_KEY,
  // dangerouslyAllowBrowser: true,
})
async function main() {
  const completion = await openai.chat.completions.create({
    model: "openai/gpt-3.5-turbo",
    messages: [
      { role: "user", content: "Say this is a test" }
    ],
  })

  console.log(completion.choices[0].message)
}
main()
```

  

## Библиотеки для других языков

  
Должно подходить большинство библиотек для других языков программирования. Например, их можно взять здесь: [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://platform.openai.com/docs/libraries/community-libraries](https://platform.openai.com/docs/libraries/community-libraries "Внешняя ссылка (откроется в новом окне)")  

### Библиотека для работы с VseGPT для Go

  
Решение от одного из наших пользователей:  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://github.com/saintbyte/vsegpt\_api](https://github.com/saintbyte/vsegpt_api "Внешняя ссылка (откроется в новом окне)")  
  
Внимание: мы не являемся официальным разработчиком и не даем никаких гарантий по данной библиотеке

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## У вас нет доступа к данной странице

Источник: https://vsegpt.ru/Docs/API/Colabs

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# У вас нет доступа к данной странице

  
Возможно, она будет доступна после [регистрации](https://vsegpt.ru/Reg "Reg") или [входа](https://vsegpt.ru/Login "Login") в систему.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Документация по API - поиск проблем и обработка ошибок

Источник: https://vsegpt.ru/Docs/API/Errors

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

 

[ВАЖНО: процесс отладки вызовов по API в случае, если возникают проблемы](#h219-1)

[1. Проверка в наших сервисах](#h219-2)

[Для текстовых запросов](#h219-3)

[Для других запросов (картинки и пр.)](#h219-4)

[2. Проверьте на разных моделях](#h219-5)

[3. Получите информацию об ошибке](#h219-6)

[4. Обратитесь к отладочной точке доступа, чтобы посмотреть ваш запрос](#h219-7)

[Ошибки API и их обработка](#h219-8)

[Общие принципы](#h219-9)

[Вебчат: Failed to fetch](#h219-10)

[Ошибка 400 (большинство обычных ошибок)](#h219-11)

[Ошибка 403 (наша)](#h219-12)

[Ошибка 429](#h219-13)

[Ошибка 500, 502 (EDGE\_FUNCTION\_INVOCATION\_FAILED или INTERNAL\_SERVER\_ERROR или пусто)](#h219-14)

[Ошибка 504 (EDGE\_FUNCTION\_INVOCATION\_TIMEOUT)](#h219-15)

  

## ВАЖНО: процесс отладки вызовов по API в случае, если возникают проблемы

### 1. Проверка в наших сервисах

  
Все наши сервисы также используют наше же API для работы.   
  
Поэтому мы настоятельно просим перед тем как писать «Ваше API не работает» проверить, работает ли оно в наших сервисах.  
  

#### Для текстовых запросов

  
Если вы делаете **обычный (нестриминговый) запрос** (с одним ответом), то, пожалуйста  

- Зайдите в Сервисы > Чат с o1 (просто этот чат использует нестриминговый вызов, в отличие от обычного чата, где данные выводятся стримингом по мере поступления)
- Выбираете модель **model-from-sidebar**
- В левой панели выбираете модель, к которой хотите обратиться.
- Запускаете запрос. Если запрос работает – значит, наше API работает.

  
Альтернативный вариант – воспользуйтесь нашим примером из Google Colab: [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Ссылки на блокноты с примерами](https://vsegpt.ru/Docs/API/Colabs "Docs / API / Colabs") для проверки работоспособности.  
  
Если вы делаете **стриминговый запрос** – просто протестируйте работу модели в нашем обычном чате с нейросетью. Если чат работает – значит, проблема в вашем запросе.  
  

#### Для других запросов (картинки и пр.)

  
Используйте соответствующие клиенты из раздела Сервисы.  
  

### 2. Проверьте на разных моделях

  
Ваш запрос не работает на конкретной модели или вообще в целом?   
  

- Используйте другую модель для проверки. Обычно постоянно работает openai/gpt-4o-mini
- Посмотрите на страницу [Uptime и инциденты](https://vsegpt.ru/Docs/Uptime "Docs / Uptime") (есть в меню) – там можно посмотреть статистику по часто используемым моделям и информацию, нет ли инцидентов с какими-то моделями, мы об этом пишем
- Почитайте информацию о вашей модели на странице Моделей – может, есть какие-то особенности (например, у моделей серии OMF есть холодный старт, и они могут стать доступны в течение после 1 неуспешного запроса)

  
**Также отмечаем, что мы не даем гарантий 100% доступности для любых сетей.** Бывают периоды, когда сети просто недоступны, тогда просто надо запастись терпением – если проблема не на нашей стороне, она обычно решается в течение нескольких часов.  
  

### 3. Получите информацию об ошибке

  
**Без этой информации мы обычно не рассматриваем вопросы в техподдержку.**  
  
При запросе кроме кода ошибки (400 и пр.) также возвращается текст ошибки. Нам он нужен, чтобы понять, что произошло – вам, чтобы легче пофиксить проблему.  
  
Ошибки бывают двух типов:  

- Если ваш запрос **не прошел валидацию в нашем API**, то мы вернем 400 или 429 ошибку с описанием. Обычно проблемы простые – закончились средства на счете, нет подписки, невалиден ключ и пр. Этот запрос **не будет зарегистрирован в системе**.
- Если ваш запрос **прошел наше API и ушел поставщику нейросети**, то он **будет зарегистрирован в системе**, его статус и текст ошибки будет доступен в меню Кабинет > [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Стоимость последних генераций](https://vsegpt.ru/User/Activity "User / Activity"). Можете использовать его.

  

### 4. Обратитесь к отладочной точке доступа, чтобы посмотреть ваш запрос

  
Иногда запрос формируется во внутренней логике вашего программного обеспечения, и вы не можете понять, что с ним не так.  
  
В таком случае можете отправить запрос к API с другим базовым URL (с другим портом) – https://api.vsegpt.ru:6010/v1/   
  
На этой точке доступа **будет логироваться последний запрос**.  
  
Чтобы получить информацию о последнем запросе обратитесь к URL:  
https://api.vsegpt.ru:6010/v1/latest/call?key=ваш\_API\_ключ\_VseGPT  
  
Это отладочная точка доступа – не используйте её для работы. Запросы на неё можно отсылать не чаще раз в 20 секунд.  
  
Получите последний запрос и сравните его с эталоном – возможно, проблема вам станет понятна.  
  

## Ошибки API и их обработка

  

### Общие принципы

  
Ошибка передается как код HTTP-запроса, а также во внутреннем JSON.  
  
Общие принципы обработки кодов:  

- 200 – все ОК
- 4xx – что-то не ОК
- 504 – (EDGE\_FUNCTION\_INVOCATION\_TIMEOUT) – сервер не смог ответить в нужное время. Попробуйте тупо переотправить запрос повторно. (Редко бывают периоды, когда сервера перегружены и таких ошибок бывает до 10%)
- 500 – ошибка сервера. Либо у нас всё плохо (маловероятно), либо вы некорректно сформировали запрос по API (очень вероятно)

  

### Вебчат: Failed to fetch

  
Иногда вебчат не возвращает ошибку, а просто говорит “Failed to fetch” – что часто означает недоступность сервера API.  
  
Пути решения:  
1. Проверить, повторяется ли ошибка на другой модели. Если нет – значит, временная проблема именно с этой моделью; переключитесь пока на другую.  
2. **Проверьте, выключен ли VPN (наиболее частый случай)**. Часто коннект к VPN не пропускает запросы из вебчата.  
3. Проверьте, повторяется ли ошибка в других браузерах (Chrome, Firefox). Если другие браузеры работают – значит, по каким-то причинам этот браузер или какое-то расширение не пропускают запросы.  
  

### Ошибка 400 (большинство обычных ошибок)

  
Основной код ошибки от нас.  
  
Ошибка:  
Expected maxTokens to be at least 1, received -15  
  
Решение: такое возникает, когда ваш запрос превышает возможности обработки модели (выходит за размер её контекста).  
Варианты решения:  

- если вы долго ведете чат – начните новый чат! Чтобы нейросеть понимала контекст разговора, при запросе обрабатываются ВСЕ предыдущие сообщения чата как входные данные. Поэтому, если вы начинаете НОВУЮ ТЕМУ разговора, начинайте НОВЫЙ чат без истории диалога – это сэкономит вам массу средств.
- или перейдите на другую модель с более большим размером контекста

  
Ошибка:  
This endpoint's maximum context length is 128000 tokens. However, you requested about 131425 tokens (31425 of text input, 100000 in the output  
  
Решение: max\_tokens (число токенов ожидаемой для генерации) для данной модели не может быть таким большим (даже если контекст у модели большой). Поменяйте его в настройках API-запроса или в чате  
  
Общее правило: сумма запроса + ожидаемый ответ не должны быть больше контекста модели.  
  
Ошибка: User with this API key not found   
  
Решение: вы указали неверный или старый ключ API; пользователь с таким ключом не найден. Возьмите ваш ключ на <https://vsegpt.ru/User/API>  
  
Ошибка: «Seems you use original OpenAI API key. This key will not work on this site; you need VseGPT API Key, you can get your own here: <https://vsegpt.ru/User/API>   
  
Решение: вы используете оригинальный ключ API вместо нашего. Зайдите на <https://vsegpt.ru/User/API> и получите наш ключ.  
  
Ошибка: This model is not available on your subscription plan. Please, upgrade your subscription plan to use it. Subscription plans: <https://vsegpt.ru/Docs/Tariffs>  
  
Решение: Данная модель не доступна на вашем тарифном плане – измените тарифный план, чтобы получить к ней доступ. Список тарифных планов: <https://vsegpt.ru/Docs/Tariffs>  
  
Ошибка:   
{"error": {"message": "Potentially out of budget: 285->700, expected price 7.5825, but you have only 0.930400 on account. Pleae, add some money to balance to proceed: https://vsegpt.ru/User/Money", "code": 400} }  
  
Решение: ошибка показывает, что ожидаемая стоимость запроса на данную модель превышает средства на вашем аккаунте. Пополните баланс или переключитесь на другую модель.  
  
Ошибка:   
InvalidRequestError: Exceeded soft user limit per query: 47972->700, expected price 11.0037, but your limit is 10.000. If you still want to process query, adjust limit in your settings on website: https://vsegpt.ru/User/SettingsModels  
  
Решение: ошибка показывает, что ожидаемая стоимость запроса на данную модель превышает пользовательский лимит на 1 запрос на вашем аккаунте. Если вы по-прежнему хотите провести запрос, вы можете настроить ваш лимит по ссылке <https://vsegpt.ru/User/SettingsModels>  
  

### Ошибка 403 (наша)

  
Ваш запрос был заблокирован из-за того, что он нарушает политику ToS модерации выбранной модели по какой-то тематике. Вам надо отредактировать его, чтобы он не нарушал, либо использовать модель без модерации.  
  
Если вы получаете ошибку 403 со словами в духе «Ваш ключ не найден» и прочее – скорее всего, вы обращаетесь не к нашему серверу, а, например, к серверу OpenAI или другим. Надо скорректировать настройки, чтобы обращаться к нашему серверу.  

### Ошибка 429

  
Вы отправляете запросы слишком часто. Допускается отправка запросов с одного аккаунта не чаще 1 раза в 2 секунды (на тарифе FAST – больше)  
  
(Также подобное поведение может быть у вышестоящих провайдеров для отдельных сетей с ограничением числа запросов в секунду)  
  

### Ошибка 500, 502 (EDGE\_FUNCTION\_INVOCATION\_FAILED или INTERNAL\_SERVER\_ERROR или пусто)

  
Два варианта:  

- Сервер временно недоступен, какие-то проблемы у нас (маловероятно)
- Вы некорректно отправляете API запрос. EDGE\_FUNCTION\_INVOCATION\_FAILED возвращает наш вышестоящий провайдер, означает, что с вызовом API что-то не так, но что именно, сказать невозможно. Попробуйте отладить API-запрос.

  

### Ошибка 504 (EDGE\_FUNCTION\_INVOCATION\_TIMEOUT)

  
Она же: EDGE\_FUNCTION\_INVOCATION\_TIMEOUT с разными комментариями  
  
Означает, что вышестоящий провайдер (у которого мы берем доступ) не может обработать запрос из-за таймаута (т.е. скорее всего перегружены сервера с моделями или другая проблема)  
  
Решается на стороне вышестоящего провайдера, вам ничего делать не нужно.   
  
Если вы находитесь в чате – просто перегенерируйте сообщение, чаще всего запрос пройдет.  
  
Если по API – то отправьте запрос повторно, чаще всего запрос пройдет.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Документация по API

Источник: https://vsegpt.ru/Docs/API/Opensource

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

 

[Опенсорс примеры](#h218-1)

[Как сделать сервис «Вопросы по файлу»](#h218-2)

[Демо: аналог сервиса «Вопросы по файлу»](#h218-3)

[Демо: RAG (поиск по базе знаний / серии документов с помощью эмбеддингов и векторной базы данных)](#h218-4)

[Демо: телеграм-бот, отвечающий на вопросы](#h218-5)

[Опенсорс: телеграм-бот Киберникто](#h218-6)

  

## Опенсорс примеры

  

  

### Как сделать сервис «Вопросы по файлу»

  
Варианта 2:  
1. **Текстовая часть вашего файла помещается в контекст нейросети** (например, gpt-4o-mini имеет контекст 128000 токенов).  
  
В таком случае **мы рекомендуем (следуя рекомендациям Antropic, создателей Claude) добавлять всю текстовую часть вашего файла в запрос к нейросети**  
  
Условно код выглядит так (в article подставьте текстовую часть вашего DOCX или PDF файла):  
  

```
context_prompt = f"""Here's an article:\n\n<article>
        {article}\n\n</article>\n\n"""
context_message = {"role": "system", "content": context_prompt}
question_message = {"role": "user", "content": "Напиши краткое содержание данной статьи"}
```

  
  
Таким же образом работает и наш сервис «Вопросы по файлу» – см. готовый пример ниже  
  

Чтобы получить текстовое содержимое вашего файла, вы можете использовать локальную конвертацию или воспользоваться нашей моделью utils/extract-text.

  
2. Файл (и база знаний) слишком большие и не помещаются в контекст.  
  
Тогда обратитесь к разделу **Демо: RAG** – там есть пример, основанный на embedding, который показывает, как добавлять потенциально релевантные части вашего файла в контекст запроса к нейросети.  
  

  

### Демо: аналог сервиса «Вопросы по файлу»

  

```
import time
import requests
import base64

VSEGPT_KEY = "sk-or-..."

# ---------------- Получаем текст файла ----------------

# Кодируем файл в base64
with open("example.pdf", "rb") as file:
    encoded_file = base64.b64encode(file.read()).decode('utf-8')

# Отправляем запрос
response = requests.post(
    "https://api.vsegpt.ru/v1/extract_text",
    headers = {
        "Authorization": f"Bearer {VSEGPT_KEY}",
        "X-Title": "File analysis demo"
    },
    json={
        "encoded_base64_file": encoded_file,
        "filename": "example.pdf",
        "model": "utils/extract-text-1.0" # вариант - utils/pdf-ocr-1.0 для оптического распознавания OCR PDF-документов
    }
)

if response.status_code != 200:
    print("Ошибка вызова: ", response.status_code, response.text)
    raise ValueError("")

# Получаем результат
article = response.json()["text"]
print("Текст файла:", article)

# ---------------- Задаем вопрос по файлу ----------------

# Ждем 1 секунду - VseGPT не позволяет посылать запросы чаще (чаще можно только на тарифе FAST)
print("Ждем 1 секунду...")
time.sleep(1.0)

# Формируем сообщения
question = "Напиши вкратце, о чем эта статья"

print("Вопрос:", question)

context_prompt = f"""Here's an article:\n\n<article>
        {article}\n\n</article>\n\n"""
context_message = {"role": "system", "content": context_prompt}
question_message = {"role": "user", "content": question}

# Подготовка данных для запроса
headers = {
    "X-Title": "File analysis demo",
    "Authorization": f"Bearer {VSEGPT_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-4o-mini",
    "messages": [context_message, question_message]
}

# Выполнение POST запроса
response = requests.post(
    "https://api.vsegpt.ru/v1/chat/completions",
    headers=headers,
    json=data
)

# Обработка ответа
response_data = response.json()
msg = response_data["choices"][0]["message"]["content"]

print("Ответ:", msg)
```

  
  

### Демо: RAG (поиск по базе знаний / серии документов с помощью эмбеддингов и векторной базы данных)

  

Вопрос: «Расстояние от Земли до Солнца?»  
Ответ: «Расстояние от Земли до Солнца составляет приблизительно 149,6 миллионов километров, что примерно равно астрономической единице.» (на основе данных файла Sun.txt)

  
RAG – набор методов, направленных на то, чтобы   
– а) выбирать из больших серий документов куски текста, соответствующих запросу пользователя  
– б) добавлять эти релевантные куски в запрос к нейросети – чтобы нейросеть отвечала, исходя из реальной информации из документов.  
  
Применяется в случае, когда у вас есть МНОГО документов, не влезающих в контекст и когда надо по ним отвечать на запросы пользователя.  
  
Ниже приведен пример реализации с помощью векторной базы данных FAISS (работает на CPU, т.е. везде) и API VseGPT:  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://github.com/janvarev/demo\_rag\_vsegpt](https://github.com/janvarev/demo_rag_vsegpt "Внешняя ссылка (откроется в новом окне)")  

### Демо: телеграм-бот, отвечающий на вопросы

  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://github.com/janvarev/Telegram-bot-vsegpt](https://github.com/janvarev/Telegram-bot-vsegpt "Внешняя ссылка (откроется в новом окне)")  
  

### Опенсорс: телеграм-бот Киберникто

  
Готовый к работе сложный телеграм-бот с множеством разных приемов для обработки входных сообщений.  
**Не демонстрационный**  
**Поддерживается сторонним разработчиком, не VseGPT**  
  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://github.com/solovieff/kibernikto](https://github.com/solovieff/kibernikto "Внешняя ссылка (откроется в новом окне)")

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Документация по API - особенности реализации и дополнительные возможности

Источник: https://vsegpt.ru/Docs/API/Special

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

   
  

- [Основные концепции API](https://vsegpt.ru/Docs/API)
- [Примеры кода (Python, CURL, Google Colab и пр.)](https://vsegpt.ru/Docs/API/Code)
- [Опенсорс примеры (RAG, телеграм-бот и пр.)](https://vsegpt.ru/Docs/API/Opensource)
- [Решение проблем API и список ошибок](https://vsegpt.ru/Docs/API/Errors)
- [Особенности реализации API](https://vsegpt.ru/Docs/API/Special)
- [Дополнительные возможности (Tools, MCP и пр.)](https://vsegpt.ru/Docs/API/AddFeatures)

 

[Особенности реализации](#h220-1)

[Нет поддержки function calls, но есть поддержка tools](#h220-2)

[n=1 – всегда возвращается один варианта текста/картинок](#h220-3)

[Неуказанные max\_tokens в chat/completions](#h220-4)

  

## Особенности реализации

  

### Нет поддержки function calls, но есть поддержка tools

  
С 20 августа 2024 функциональность function calls, как [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)устаревшая версия tool calls](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling "Внешняя ссылка (откроется в новом окне)"), больше не работает. Пожалуйста, используйте tool calls для реализации.  
  
Tool calls (вызовы tools) поддерживаются, как указано в [дополнительных фичах](https://vsegpt.ru/Docs/API/AddFeatures "Docs / API / Add Features")  
  

### n=1 – всегда возвращается один варианта текста/картинок

  
При генерации на сервисе, как правило, мы НЕ позволяем генерировать сразу несколько вариантов текста или изображений – это усложняет управление моделями.  
  
Поэтому при запросе принудительно устанавливается n=1 для числа генераций.  
  

### Неуказанные max\_tokens в chat/completions

  
Согласно стандарту, вам нужно указывать max\_tokens в запросе. max\_tokens определяет максимальное количество токенов ответа модели.  
  
Но на практике ряд endpoint, в том числе часть наших провайдеров позволяют его не указывать. Это позволяет не заморачиваться с расчетом размера контекста модели и пр. – однако при этом могут возникать странные проблемы (например, была история с генерацией в ответе 250к пробелов от модели Google – просто потому, что не был указан max\_tokens, а модель сама не остановила генерацию)  
  
Мы считаем, что указывать max\_tokens крайне желательно, но выбор остается за вами. Настроить поведение API при отсутствующем max\_tokens можно на [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)странице настроек](https://vsegpt.ru/User/SettingsModels "User / Settings Models")

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

# 2. Модели

## Текстовые (более 120)

Источник: https://vsegpt.ru/Docs/Models

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

 

# Текстовые (более 120)

  
 [Непонятно, что выбрать? Есть наш туториал >](/Tutorials/HowToChoose)   

туториал обновлен 5 марта 2025

  
  

[Текстовые модели (западные, Европа, США)](#h46-1)

[OpenAI: ChatGPT, GPT-5, GPT-4o-mini...](#h46-2)

[Anthropic: Claude Sonnet, Opus, Haiku](#h46-3)

[Perplexity: онлайн, с доступом к Интернету и фактической информации](#h46-4)

[Google: Gemini Pro, Flash](#h46-5)

[xAI: Grok 2, 3, 4](#h46-6)

[MistralAI: опенсорс + закрытые Tiny, Small, Medium](#h46-7)

[Cohere: с фокусом на RAG, function calling, tools](#h46-8)

[Amazon: Nova и пр.](#h46-9)

[Текстовые модели (восточные, Китай)](#h46-10)

[DeepSeek: V3, R1, 3.2 и пр.](#h46-11)

[Qwen – опенсорс модели от Tongyi Qianwen (Alibaba)](#h46-12)

[Z-AI – GLM 5, опенсорс модели от Z.AI](#h46-13)

[Minimax – модели от Minimax](#h46-14)

[Moonshot AI: Kimi K2, K2.5 и пр.](#h46-15)

[Российские: Сайга и Вихрь – альтернатива YaGPT и GigaChat](#h46-16)

[Опенсорс](#h46-17)

[Обычные опенсорс модели](#h46-18)

[Самые свежие опенсорс модели Open Models Fan (OMF) (бета-тест)](#h46-19)

[Примечания](#h46-20)

# Мировые новинки у нас

  

- [Все новинки](https://vsegpt.ru/Docs/ModelsNew "Docs / Models New")
- **20 августа, GLM 5.3** от Z-AI.
- **14 августа, Deepseek V4 Pro 0813** от Deepseek.
- **14 августа, Grok 4.6** от xAI.
- **14 августа, Gemini 3.7 Flash** от Google.
- **8 августа, Qwen 3.8 Max** от Qwen.
- **31 июля, Deepseek V4 Flash 0731** от Deepseek, в течение нескольких часов после публикации
- **25 июля, топовая Opus 5** от Anhtropic
- **22 июля, Gemini 3.6 Flash и 3.5 Flash Lite** от Google.
- **16 июля, Kimi K3** от MoonshotAI, в течение нескольких часов после выкладки API.
- **10 июля, топовые GPT-5.6 Luna, Terra, Sol** от OpenAI.
- **30 июня, топовая Sonnet 5** от Anhtropic, в течение нескольких часов после публикации
- **26 июня, GLM-5.2** от Z-AI
- **28 мая, топовая Opus 4.8** от Anhtropic
- **23 мая, учли постоянную 75% скидку на Deepseek V4 Pro** от Deepseek.
- **20 мая, Gemini 3.5 Flash и 3.1 Flash Lite** от Google.
- **17 мая, Grok 4.3** от xAI.
- **3 мая, GPT-5.5 и GPT-5.5 Pro** от OpenAI.
- **24 апреля, Deepseek V4 Flash и Pro** от Deepseek. Топовые дешевые модели.
- **22 апреля, GPT Image 2** от OpenAI. Топовая модель генерации изображений.
- **20 апреля, Kimi K2.6** от MoonshotAI. По метрикам соперничает с топами.
- **17 апреля, топовая Opus 4.7** от Anhtropic
- **10 апреля, Gemma 4** от Google.
- **7 апреля, GLM-5.1** от Z-AI, в течение нескольких часов после публикации. Топовая модель программирования.
- **25 марта, Xiaomi: MiMo-V2-Pro и Omni**
- **17 марта, GPT-5.4 mini и nano** от OpenAI, в течение 2 часов после публикации.
- **10 марта, Kling O3 и LTX 2.3** – топовые модели генерации видео.
- **6 марта, GPT-5.4 и GPT-5.4 Pro** от OpenAI.
- **3 марта, Gemini 3.1 Flash Lite Preview** от Google – легкая модель, в течение 3 часов после публикации.
- **27 февраля, Nano Banana 2** – создание и редактирование изображений от Google.
- **25 февраля, GPT-5.3 Codex** от OpenAI.
- **17 февраля, Sonnet 4.6** – обновленная модель от Anthropic, по метрикам приближается к Opus 4.5–4.6. *Добавили в течение 3 часов после публикации.*
- **6 февраля, Opus 4.6** – обновленная модель от Anthropic.
- **20 января, GPT-5.2 Codex** от OpenAI.
- **15 января, Flux 2 [klein] 4B и 9B** – работа с изображением (создание по тексту, редактирование), сопоставима с обычной Nano Banana.
- **12 января, поддержка Claude Code**. Сделали альтернативный доступ к нейросетям через Anthropic-совместимое API, и теперь можно использовать [Claude Code](https://vsegpt.ru/ExtTools/ClaudeCode "Ext Tools / Claude Code") для программирования.
- **17 декабря, Gemini 3.0 Flash Preview** от Google – легкая модель, чуть хуже топовой Gemini 3.0 Pro Preview.
- **12 декабря, GPT-5.2, GPT-5.2 Pro** от OpenAI.
- **8 декабря, Seedream 4.5** – работа с изображением (создание по тексту, редактирование), конкурент Nano Banana Pro.
- **2 декабря, DeepSeek 3.2** – обновленная модель от DeepSeek.
- **25 ноября, Opus 4.5** – обновленная модель от Anthropic.
- **20 ноября, Nano Banana Pro** – создание и редактирование изображений от Google, в течение 3 часов после публикации.
- **18 ноября, Gemini 3.0 Pro Preview** от Google, в течение 3 часов после публикации.
- **14 ноября, GPT-5.1** от OpenAI.
- **6 ноября, Kimi K2 Thinking** – в течение 2 часов после публикации. Опенсорс модель уровня GPT-5, согласно метрикам.
- **4 ноября, Kling 2.5**. Топовая модель генерации видео.
- **4 ноября, Sora 2** от OpenAI. Топовая модель генерации видео.
- **31 октября, Veo 3.1 Fast** от Google. Топовая модель генерации видео.
- **31 октября, Minimax M2** от Minimax. Топовая опенсорс модель.
- **22 октября, Grok 4 Fast** от xAI. Модель уровня GPT-5, но значительно быстрее и дешевле.
- **22 октября, GPT 5 Pro** от OpenAI. Самая дорогая и топовая модель.
- **16 октября, Haiku 4.5** – обновленная модель от Anthropic. По метрикам сопоставима с более старой Sonnet 4, но дешевле её практически в 5 раз!
- **29 сентября, Sonnet 4.5** – обновленная модель от Anthropic
- **29 сентября, DeepSeek Chat 3.2 Exp** – обновленная модель от DeepSeek со значительным понижением стоимости генерации
- [Более старые новости по подключенным моделям](https://vsegpt.ru/Docs/Models/OldNews "Docs/Models/Old News")

  
  

## Текстовые модели (западные, Европа, США)

### OpenAI: ChatGPT, GPT-5, GPT-4o-mini...

  

**Нейросети от мирового лидера, OpenAI.** Если вы только погружаетесь в тему текстовых нейросетей – оптимально выбрать ChatGPT (gpt-3.5-turbo) в качестве основного варианта. Если вам нужна бОльшая точность в рассуждениях – выберите GPT-4. GPT-4-Turbo обладает контекстом в 128 000 символов и подходит в том числе для обработки больших файлов – но она в меру дорогая.  
   
**Внимание:** для новых пользователей включена **автоматическая оптимизация запросов** при выборе сетeй OpenAI – выбирается самая эффективная и дешевая в своем классе. Если вы хотите точного соответствия модели вашему запросу, отключите оптимизацию в [![Вам запрещён доступ](https://vsegpt.ru/themes/bs5vsegpt/icons/lock.gif)Настройках](https://vsegpt.ru/User/SettingsModels "User / Settings Models")

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || OpenAI: GPT-6 Asta (Thinking XHigh) [?](#mar744taskfull) openai/gpt-6-astra-xhigh  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но дорогая tools structured-outputs   vision | 3.0 | 15.0 | 1000000 | 5 сен | да |
| OpenAI: GPT-6 Asta (Thinking High) [?](#mar743taskfull) openai/gpt-6-astra-high  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но дорогая tools structured-outputs   vision | 3.0 | 15.0 | 1000000 | 5 сен | да |
| OpenAI: GPT-6 Asta (Thinking Medium) [?](#mar742taskfull) openai/gpt-6-astra  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но дорогая tools structured-outputs   vision | 3.0 | 15.0 | 1000000 | 5 сен | да |
| OpenAI: GPT-6 Asta (Thinking Low) [?](#mar741taskfull) openai/gpt-6-astra-low  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но дорогая tools structured-outputs   vision | 3.0 | 15.0 | 1000000 | 5 сен | да |
| OpenAI: GPT-5.6 Luna (Альт вариант, Thinking High) [?](#mar721taskfull) openai/gpt-5.6-luna-alt-thinking-high  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К провайдер логирует данные tools structured-outputs   vision | 0.06 | 0.40 | 1000000 | 8 авг | да |
| OpenAI: GPT-5.6 Luna (Альт вариант) [?](#mar720taskfull) openai/gpt-5.6-luna-alt  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К провайдер логирует данные tools structured-outputs   vision | 0.06 | 0.40 | 1000000 | 8 авг | да |
| OpenAI: GPT-5.6 Sol Pro [?](#mar709taskfull) openai/gpt-5.6-sol-pro  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но ОЧЕНЬ дорогая tools structured-outputs   vision | 1.5 | 9.0 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Sol (Thinking High) [?](#mar708taskfull) openai/gpt-5.6-sol-thinking-high  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ, но дорогая tools structured-outputs   vision | 1.5 | 9.0 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Sol [?](#mar707taskfull) openai/gpt-5.6-sol  Профессиональный (не Тестовый) повышенная цена при контексте > 250К ТОП! tools structured-outputs   vision | 1.5 | 9.0 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Terra Pro [?](#mar706taskfull) openai/gpt-5.6-terra-pro  Профессиональный (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.75 | 4.5 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Terra (Thinking High) [?](#mar705taskfull) openai/gpt-5.6-terra-thinking-high  Профессиональный (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.75 | 4.5 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Terra [?](#mar704taskfull) openai/gpt-5.6-terra  Профессиональный (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.75 | 4.5 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Luna Pro [?](#mar703taskfull) openai/gpt-5.6-luna-pro  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.3 | 1.8 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Luna (Thinking High) [?](#mar702taskfull) openai/gpt-5.6-luna-thinking-high  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.3 | 1.8 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.6 Luna [?](#mar701taskfull) openai/gpt-5.6-luna  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К tools structured-outputs   vision | 0.3 | 1.8 | 1000000 | 10 июл | да |
| OpenAI: GPT-5.5-Pro [?](#mar668taskfull) openai/gpt-5.5-pro  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs   vision | 9.0 | 54.0 | 300000 | 3 мая | да |
| OpenAI: GPT-5.5 [?](#mar667taskfull) openai/gpt-5.5  Профессиональный (не Тестовый) повышенная цена при контексте > 250К топ tools structured-outputs   vision | 1.5 | 9.0 | 1000000 | 3 мая | да |
| OpenAI: GPT-5.4 Mini (Thinking) [?](#mar636taskfull) openai/gpt-5.4-mini-thinking-xhigh  Базовый и выше (не Тестовый) tools structured-outputs   vision | 0.20 | 1.20 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 Nano (Thinking XHigh) [?](#mar635taskfull) openai/gpt-5.4-nano-thinking-xhigh  Базовый и выше (не Тестовый) tools structured-outputs   vision | 0.06 | 0.35 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 Nano (Thinking High) [?](#mar634taskfull) openai/gpt-5.4-nano-thinking  tools structured-outputs   vision | 0.06 | 0.35 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 Nano [?](#mar633taskfull) openai/gpt-5.4-nano  tools structured-outputs   vision | 0.06 | 0.35 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 Mini (Thinking) [?](#mar632taskfull) openai/gpt-5.4-mini-thinking  Базовый и выше (не Тестовый) tools structured-outputs   vision | 0.20 | 1.20 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 Mini [?](#mar631taskfull) openai/gpt-5.4-mini  Базовый и выше (не Тестовый) tools structured-outputs   vision | 0.20 | 1.20 | 400000 | 17 мар | да |
| OpenAI: GPT-5.4 (1M контекста) [?](#mar629taskfull) openai/gpt-5.4-1m  Профессиональный (не Тестовый) топ tools structured-outputs   vision | 1.40 | 6.30 | 1000000 | 6 мар | да |
| OpenAI: GPT-5.4 Pro (Thinking High) [?](#mar619taskfull) openai/gpt-5.4-pro-high  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs | 9.0 | 54.0 | 256000 | 6 мар | да |
| OpenAI: GPT-5.4 Pro (Thinking) [?](#mar618taskfull) openai/gpt-5.4-pro  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs | 9.0 | 54.0 | 256000 | 6 мар | да |
| OpenAI: GPT-5.4 (X-High Thinking) [?](#mar617taskfull) openai/gpt-5.4-xhigh  Профессиональный (не Тестовый) топ tools structured-outputs | 0.70 | 4.20 | 256000 | 6 мар | да |
| OpenAI: GPT-5.4 [?](#mar616taskfull) openai/gpt-5.4  Профессиональный (не Тестовый) топ tools structured-outputs | 0.70 | 4.20 | 256000 | 6 мар | да |
| OpenAI: GPT-5.3 Chat [?](#mar615taskfull) openai/gpt-5.3-chat  Профессиональный топ tools structured-outputs | 0.48 | 3.80 | 128000 | 4 мар | да |
| OpenAI: GPT-5.3 Codex (Thinking, X-high) [?](#mar610taskfull) openai/gpt-5.3-codex-xhigh  Профессиональный (не Тестовый) топ программирование и общие задачи tools structured-outputs   vision | 0.52 | 3.90 | 400000 | 25 фев | да |
| OpenAI: GPT-5.3 Codex (Thinking) [?](#mar609taskfull) openai/gpt-5.3-codex  Профессиональный (не Тестовый) топ программирование и общие задачи tools structured-outputs   vision | 0.52 | 3.90 | 400000 | 25 фев | да |
| OpenAI: GPT-5.2 Codex (Thinking) [?](#mar580taskfull) openai/gpt-5.2-codex  Профессиональный (не Тестовый) топ программирование и общие задачи tools structured-outputs | 0.52 | 3.90 | 400000 | 20 янв | да |
| OpenAI: GPT-5.2 Pro (Thinking High) [?](#mar565taskfull) openai/gpt-5.2-pro-high  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs | 6.0 | 45.0 | 400000 | 12 дек 25 | да |
| OpenAI: GPT-5.2 Pro (Thinking) [?](#mar564taskfull) openai/gpt-5.2-pro  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs | 6.0 | 45.0 | 400000 | 12 дек 25 | да |
| OpenAI: GPT-5.2 (Thinking X-High) [?](#mar563taskfull) openai/gpt-5.2-xhigh  Профессиональный (не Тестовый) топ tools structured-outputs | 0.48 | 3.80 | 400000 | 12 дек 25 | да |
| OpenAI: GPT-5.2 (Thinking High) [?](#mar562taskfull) openai/gpt-5.2-high  Профессиональный топ tools structured-outputs | 0.48 | 3.80 | 400000 | 12 дек 25 | да |
| OpenAI: GPT-5.2 (Thinking) [?](#mar561taskfull) openai/gpt-5.2  Профессиональный топ tools structured-outputs | 0.48 | 3.80 | 400000 | 12 дек 25 | да |
| OpenAI: GPT-5.2 Chat [?](#mar560taskfull) openai/gpt-5.2-chat  Профессиональный топ tools structured-outputs | 0.48 | 3.80 | 128000 | 11 дек 25 | да |
| OpenAI: GPT-5.1 Codex Max (Thinking) [?](#mar557taskfull) openai/gpt-5.1-codex-max  Профессиональный (не Тестовый) топ программирование и общие задачи tools structured-outputs | 0.37 | 2.80 | 400000 | 8 дек 25 | да |
| OpenAI: GPT-5.1 Codex Mini (Thinking) [?](#mar540taskfull) openai/gpt-5.1-codex-mini  программирование и общие задачи tools structured-outputs | 0.08 | 0.56 | 400000 | 14 ноя 25 | да |
| OpenAI: GPT-5.1 Codex (Thinking) [?](#mar539taskfull) openai/gpt-5.1-codex  Профессиональный (не Тестовый) топ программирование и общие задачи tools structured-outputs | 0.37 | 2.80 | 400000 | 14 ноя 25 | да |
| OpenAI: GPT-5.1 (Thinking) [?](#mar538taskfull) openai/gpt-5.1  Профессиональный (не Тестовый) топ tools structured-outputs | 0.37 | 2.80 | 400000 | 14 ноя 25 | да |
| OpenAI: GPT-5 Pro (Thinking) [?](#mar503taskfull) openai/gpt-5-pro  Профессиональный (не Тестовый) топ, но ОЧЕНЬ дорогая tools structured-outputs | 4.5 | 28.0 | 400000 | 22 окт 25 | да |
| OpenAI: GPT-5 (Thinking) [?](#mar455taskfull) openai/gpt-5  Профессиональный (не Тестовый) топ tools structured-outputs | 0.15 | 1.30 | 400000 | 26 авг 25 | да |
| OpenAI: GPT-5 Chat (устарела, перенаправляется в GPT 5.4) [?](#mar448taskfull) openai/gpt-5-chat  Профессиональный топ structured-outputs | 0.15 | 1.30 | 400000 | 7 авг 25 | да |
| OpenAI: GPT-5 Thinking Mini [?](#mar447taskfull) openai/gpt-5-mini  tools structured-outputs | 0.037 | 0.30 | 400000 | 7 авг 25 | да |
| OpenAI: GPT-5 Nano [?](#mar446taskfull) openai/gpt-5-nano  Базовый и выше (не Тестовый) дешевая и с большим контекстом tools structured-outputs | 0.015 | 0.12 | 400000 | 7 авг 25 | да |
| OpenAI: gpt-oss-120b [?](#mar445taskfull) openai/gpt-oss-120b | 0.015 | 0.065 | 128000 | 7 авг 25 | нет |
| OpenAI: gpt-oss-120b (fast) [?](#mar444taskfull) openai/gpt-oss-120b-fast  tools | 0.021 | 0.085 | 128000 | 7 авг 25 | нет |
| OpenAI: gpt-oss-20b (fast) [?](#mar443taskfull) openai/gpt-oss-20b  tools | 0.014 | 0.06 | 128000 | 7 авг 25 | нет |
| OpenAI: o3 [?](#mar394taskfull) openai/o3  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика tools structured-outputs | 0.6 | 2.4 | 200000 | 7 июн 25 | да |
| OpenAI: GPT-4o (2024-11-20) Online HQ [?](#mar358taskfull) openai/gpt-4o-2024-11-20-online-hq  Профессиональный За вызов: 2.0 р. tools structured-outputs | 0.3 | 1.2 | 128000 | 14 мая 25 | да |
| OpenAI: GPT-4o Online HQ [?](#mar357taskfull) openai/gpt-4o-online-hq  Профессиональный За вызов: 2.0 р. топ от 13 мая tools | 0.6 | 1.8 | 128000 | 14 мая 25 | да |
| OpenAI: o4-mini-high (пресет для глубоких размышлений от o4-mini) [?](#mar338taskfull) openai/o4-mini-high  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика tools structured-outputs | 0.28 | 1.12 | 200000 | 16 апр 25 | да |
| OpenAI: o4-mini (для размышлений, не рек. для обычных задач) [?](#mar337taskfull) openai/o4-mini  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика tools structured-outputs | 0.28 | 1.12 | 200000 | 16 апр 25 | да |
| OpenAI: GPT-4.1 [?](#mar336taskfull) openai/gpt-4.1  Профессиональный топ от 14 апреля tools structured-outputs | 0.28 | 1.12 | 1000000 | 14 апр 25 | да |
| OpenAI: GPT-4.1 Mini [?](#mar335taskfull) openai/gpt-4.1-mini  tools structured-outputs | 0.06 | 0.24 | 1000000 | 14 апр 25 | да |
| OpenAI: GPT-4.1 Nano [?](#mar334taskfull) openai/gpt-4.1-nano  дешевая и с большим контекстом tools structured-outputs | 0.015 | 0.06 | 1000000 | 14 апр 25 | да |
| OpenAI: o3-mini-high (пресет для глубоких размышлений от o3-mini) [?](#mar273taskfull) openai/o3-mini-high  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика structured-outputs | 0.28 | 1.12 | 200000 | 14 фев 25 | да |
| OpenAI: o3-mini (для размышлений, не рек. для обычных задач) [?](#mar267taskfull) openai/o3-mini  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика structured-outputs | 0.28 | 1.12 | 200000 | 1 фев 25 | да |
| OpenAI: o1 (для размышлений, не рек. для обычных задач) [?](#mar238taskfull) openai/o1  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика tools structured-outputs | 3.5 | 14.0 | 128000 | 18 дек 24 | да |
| OpenAI: GPT-4o (2024-11-20) [?](#mar221taskfull) openai/gpt-4o-2024-11-20  Профессиональный tools structured-outputs | 0.3 | 1.2 | 128000 | 26 ноя 24 | да |
| OpenAI: o1-mini (не рек. для обычных задач) [?](#mar192taskfull) openai/o1-mini  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) размышления, математика | 0.6 | 2.7 | 128000 | 13 сен 24 | нет |
| OpenAI: GPT-4o (2024-08-06) [?](#mar172taskfull) openai/gpt-4o-2024-08-06  Профессиональный топ от 6 августа tools structured-outputs | 0.3 | 1.2 | 128000 | 6 авг 24 | да |
| OpenAI: GPT-4o (2024-05-13) openai/gpt-4o-2024-05-13  Профессиональный tools | 0.6 | 1.8 | 128000 | 13 мая 24 | да |
| OpenAI: GPT-4o mini [?](#mar149taskfull) openai/gpt-4o-mini  tools structured-outputs | 0.02 | 0.08 | 128000 | 18 июл 24 | да |
| OpenAI: GPT-4o [?](#mar115taskfull) openai/gpt-4o  Профессиональный топ от 13 мая tools | 0.6 | 1.8 | 128000 | 25 мая 24 | да |
| OpenAI: GPT-4 Turbo (gpt-4-turbo-2024-04-09) [?](#mar94taskfull) openai/gpt-4-turbo  Профессиональный топ! | 1.5 | 4.5 | 128000 | 10 апр 24 | да |
| OpenAI: GPT-4 [?](#mar9taskfull) openai/gpt-4  Профессиональный | 4.5 | 9 | 8191 | 14 дек 23 | да |
| OpenAI: GPT-3.5 Turbo 16k openai/gpt-3.5-turbo-16k | 0.45 | 0.6 | 16383 | 30 сен 23 | да |
| OpenAI: GPT-3.5 Turbo [?](#mar7taskfull) openai/gpt-3.5-turbo | 0.15 | 0.3 | 4095 | 7 ноя 23 | да |

X

### OpenAI: GPT-6 Asta (Thinking XHigh)

GPT-6 Astra — флагманская модель OpenAI, созданная для решения сложных комплексных задач. Она идеально подходит для глубокого анализа, разработки программного обеспечения, масштабных исследований, научной работы и создания документов, а также особенно эффективна в длительных автономных задачах, связанных с управлением компьютером и браузером.  
  
Размышляющая версия, режим Xhigh для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 2000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-6 Asta (Thinking High)

GPT-6 Astra — флагманская модель OpenAI, созданная для решения сложных комплексных задач. Она идеально подходит для глубокого анализа, разработки программного обеспечения, масштабных исследований, научной работы и создания документов, а также особенно эффективна в длительных автономных задачах, связанных с управлением компьютером и браузером.  
  
Размышляющая версия, режим high для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1500р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-6 Asta (Thinking Medium)

GPT-6 Astra — флагманская модель OpenAI, созданная для решения сложных комплексных задач. Она идеально подходит для глубокого анализа, разработки программного обеспечения, масштабных исследований, научной работы и создания документов, а также особенно эффективна в длительных автономных задачах, связанных с управлением компьютером и браузером.  
  
Размышляющая версия, режим medium для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-6 Asta (Thinking Low)

GPT-6 Astra — флагманская модель OpenAI, созданная для решения сложных комплексных задач. Она идеально подходит для глубокого анализа, разработки программного обеспечения, масштабных исследований, научной работы и создания документов, а также особенно эффективна в длительных автономных задачах, связанных с управлением компьютером и браузером.  
  
Размышляющая версия, режим low для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Luna (Альт вариант, Thinking High)

GPT-5.6 Luna — быстрая и экономичная модель из линейки GPT-5.6 компании OpenAI. Она оптимально подходит для задач с высокой нагрузкой и жёсткими требованиями к задержке, таких как чат, классификация и несложные агентные сценарии, обеспечивая достойные возможности рассуждения в своём ценовом сегменте.  
  
Альтернативный вариант (логирующий провайдер, дешевле).  
  
Размышляющая версия, режим high для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 150р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Luna (Альт вариант)

GPT-5.6 Luna — быстрая и экономичная модель из линейки GPT-5.6 компании OpenAI. Она оптимально подходит для задач с высокой нагрузкой и жёсткими требованиями к задержке, таких как чат, классификация и несложные агентные сценарии, обеспечивая достойные возможности рассуждения в своём ценовом сегменте.  
  
Альтернативный вариант (логирующий провайдер, дешевле)  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Sol Pro

GPT-5.6 Sol — флагманская модель в линейке GPT-5.6 от OpenAI. Версия Pro - обрабатывается с параметром reasoning.mode, установленным на pro, для более качественных ответов на сложные задачи.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 2000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Sol (Thinking High)

GPT-5.6 Sol — флагманская модель в линейке GPT-5.6 от OpenAI. Она оптимально подходит для сложных задач, требующих рассуждений, написания кода и агентных рабочих процессов, а также особенно хорошо справляется с задачами в командной строке, многоэтапным программированием и решением долгосрочных проблем.  
  
Размышляющая версия, режим high для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Sol

GPT-5.6 Sol — флагманская модель в линейке GPT-5.6 от OpenAI. Она оптимально подходит для сложных задач, требующих рассуждений, написания кода и агентных рабочих процессов, а также особенно хорошо справляется с задачами в командной строке, многоэтапным программированием и решением долгосрочных проблем.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 500р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Terra Pro

GPT-5.6 Terra — это сбалансированная модель из серии GPT-5.6 от OpenAI, занимающая промежуточное положение между флагманским уровнем Sol и экономичным уровнем Luna. Версия Pro - обрабатывается с параметром reasoning.mode, установленным на pro, для более качественных ответов на сложные задачи.  
  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Terra (Thinking High)

GPT-5.6 Terra — это сбалансированная модель из серии GPT-5.6 от OpenAI, занимающая промежуточное положение между флагманским уровнем Sol и экономичным уровнем Luna. Она подходит для повседневных задач в области программирования, логического мышления и автономных агентских сценариев, где важно найти баланс между возможностями и стоимостью, обеспечивая высокую производительность примерно вдвое дешевле, чем Sol.  
  
Размышляющая версия, режим high для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 500р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Terra

GPT-5.6 Terra — это сбалансированная модель из серии GPT-5.6 от OpenAI, занимающая промежуточное положение между флагманским уровнем Sol и экономичным уровнем Luna. Она подходит для повседневных задач в области программирования, логического мышления и автономных агентских сценариев, где важно найти баланс между возможностями и стоимостью, обеспечивая высокую производительность примерно вдвое дешевле, чем Sol.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 250р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Luna Pro

GPT-5.6 Luna — быстрая и экономичная модель из линейки GPT-5.6 компании OpenAI. Версия Pro - обрабатывается с параметром reasoning.mode, установленным на pro, для более качественных ответов на сложные задачи.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 300р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Luna (Thinking High)

GPT-5.6 Luna — быстрая и экономичная модель из линейки GPT-5.6 компании OpenAI. Она оптимально подходит для задач с высокой нагрузкой и жёсткими требованиями к задержке, таких как чат, классификация и несложные агентные сценарии, обеспечивая достойные возможности рассуждения в своём ценовом сегменте.  
  
Размышляющая версия, режим high для размышлений.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 150р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.6 Luna

GPT-5.6 Luna — быстрая и экономичная модель из линейки GPT-5.6 компании OpenAI. Она оптимально подходит для задач с высокой нагрузкой и жёсткими требованиями к задержке, таких как чат, классификация и несложные агентные сценарии, обеспечивая достойные возможности рассуждения в своём ценовом сегменте.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.5-Pro

GPT-5.5 Pro — это высокопроизводительная модель OpenAI, оптимизированная для глубокого рассуждения и точности при выполнении сложных, ответственных задач.   
  
Ввиду технических особенностей нашей реализации:  
- контекст ограничен до 300 000  
- на вход можно добавить только одну картинку до 100-150Кб  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 3000р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.5

GPT-5.5 — это передовая модель OpenAI, разработанная для сложных профессиональных задач. Она основана на GPT-5.4 и отличается более мощным логическим мышлением, повышенной надёжностью и улучшенной эффективностью использования токенов при решении сложных задач. Модель поддерживает контекстное окно объёмом более 1 млн токенов (922K входных, 128K выходных), а также текстовые и графические входные данные, что позволяет выполнять масштабные задачи в области логического вывода, программирования и мультимодальных рабочих процессов в рамках единой системы.  
**Повышенная цена при контексте > 250К**: x2.0 стоимость входа; x1.5 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Mini (Thinking)

GPT-5.4 mini привносит ключевые возможности GPT-5.4 в более быструю и эффективную модель, оптимизированную для высоконагруженных рабочих процессов. Она поддерживает текстовые и графические входные данные с высокой производительностью в области рассуждений, написания кода и использования инструментов, одновременно снижая задержку и стоимость для крупномасштабных развёртываний.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Nano (Thinking XHigh)

GPT-5.4 nano — наиболее лёгкий и экономичный вариант семейства GPT-5.4, оптимизированный для задач, критичных к скорости выполнения и требующих обработки больших объёмов данных. Модель поддерживает текстовые и графические входные данные и предназначена для сценариев с низкой задержкой, таких как классификация, извлечение данных, ранжирование и выполнение подзадач агентами.  
  
Модель ставит во главу угла отзывчивость и эффективность, а не глубокое рассуждение, что делает её идеальной для конвейеров, требующих быстрых и надёжных результатов в масштабе. GPT-5.4 nano хорошо подходит для фоновых задач, систем реального времени и распределённых агентных архитектур, где минимизация затрат и задержки имеет первостепенное значение.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Nano (Thinking High)

GPT-5.4 nano — наиболее лёгкий и экономичный вариант семейства GPT-5.4, оптимизированный для задач, критичных к скорости выполнения и требующих обработки больших объёмов данных. Модель поддерживает текстовые и графические входные данные и предназначена для сценариев с низкой задержкой, таких как классификация, извлечение данных, ранжирование и выполнение подзадач агентами.  
  
Модель ставит во главу угла отзывчивость и эффективность, а не глубокое рассуждение, что делает её идеальной для конвейеров, требующих быстрых и надёжных результатов в масштабе. GPT-5.4 nano хорошо подходит для фоновых задач, систем реального времени и распределённых агентных архитектур, где минимизация затрат и задержки имеет первостепенное значение.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Nano

GPT-5.4 nano — наиболее лёгкий и экономичный вариант семейства GPT-5.4, оптимизированный для задач, критичных к скорости выполнения и требующих обработки больших объёмов данных. Модель поддерживает текстовые и графические входные данные и предназначена для сценариев с низкой задержкой, таких как классификация, извлечение данных, ранжирование и выполнение подзадач агентами.  
  
Модель ставит во главу угла отзывчивость и эффективность, а не глубокое рассуждение, что делает её идеальной для конвейеров, требующих быстрых и надёжных результатов в масштабе. GPT-5.4 nano хорошо подходит для фоновых задач, систем реального времени и распределённых агентных архитектур, где минимизация затрат и задержки имеет первостепенное значение.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Mini (Thinking)

GPT-5.4 mini привносит ключевые возможности GPT-5.4 в более быструю и эффективную модель, оптимизированную для высоконагруженных рабочих процессов. Она поддерживает текстовые и графические входные данные с высокой производительностью в области рассуждений, написания кода и использования инструментов, одновременно снижая задержку и стоимость для крупномасштабных развёртываний.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Mini

GPT-5.4 mini привносит ключевые возможности GPT-5.4 в более быструю и эффективную модель, оптимизированную для высоконагруженных рабочих процессов. Она поддерживает текстовые и графические входные данные с высокой производительностью в области рассуждений, написания кода и использования инструментов, одновременно снижая задержку и стоимость для крупномасштабных развёртываний.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 (1M контекста)

GPT-5.4 — новейшая передовая модель OpenAI, объединяющая линейки Codex и GPT в единую систему. Она оснащена контекстным окном объёмом более 1 млн токенов (922 тыс. входных, 128 тыс. выходных) с поддержкой текстовых и графических входных данных, что обеспечивает высококонтекстное рассуждение, программирование и мультимодальный анализ в рамках единого рабочего процесса.  
  
Модель демонстрирует улучшенные показатели в области программирования, понимания документов, использования инструментов и следования инструкциям.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Pro (Thinking High)

GPT-5.4 Pro — самая продвинутая модель OpenAI, построенная на унифицированной архитектуре GPT-5.4 с расширенными возможностями рассуждения для сложных задач с высокими требованиями.   
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Модель НЕ поддерживает стриминг, используйте настройку без стриминга.  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 800р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 Pro (Thinking)

GPT-5.4 Pro — самая продвинутая модель OpenAI, построенная на унифицированной архитектуре GPT-5.4 с расширенными возможностями рассуждения для сложных задач с высокими требованиями.   
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Модель НЕ поддерживает стриминг, используйте настройку без стриминга.  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 800р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4 (X-High Thinking)

GPT-5.4 — новейшая передовая модель OpenAI, объединяющая линейки Codex и GPT в единую систему. Она оснащена контекстным окном объёмом более 1 млн токенов (922 тыс. входных, 128 тыс. выходных) с поддержкой текстовых и графических входных данных, что обеспечивает высококонтекстное рассуждение, программирование и мультимодальный анализ в рамках единого рабочего процесса.  
  
Модель демонстрирует улучшенные показатели в области программирования, понимания документов, использования инструментов и следования инструкциям.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.4

GPT-5.4 — новейшая передовая модель OpenAI, объединяющая линейки Codex и GPT в единую систему. Она оснащена контекстным окном объёмом более 1 млн токенов (922 тыс. входных, 128 тыс. выходных) с поддержкой текстовых и графических входных данных, что обеспечивает высококонтекстное рассуждение, программирование и мультимодальный анализ в рамках единого рабочего процесса.  
  
Модель демонстрирует улучшенные показатели в области программирования, понимания документов, использования инструментов и следования инструкциям.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.3 Chat

GPT-5.3 Chat — это обновление наиболее используемой модели ChatGPT, которое делает повседневные разговоры более плавными, полезными и практически направленными. Оно обеспечивает более точные ответы с улучшенной контекстуализацией и значительно сокращает количество необоснованных отказов, оговорок и излишне осторожных формулировок, способных нарушить естественный ход беседы.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.3 Codex (Thinking, X-high)

GPT-5.3-Codex — наиболее продвинутая агентная модель для написания кода от OpenAI, сочетающая в себе передовые возможности GPT-5.2-Codex в области разработки программного обеспечения с более широкими способностями к рассуждению и профессиональными знаниями GPT-5.2. Модель демонстрирует результаты на уровне лучших в отрасли по SWE-Bench Pro, а также высокую производительность на Terminal-Bench 2.0 и OSWorld-Verified, что отражает улучшенные навыки программирования на нескольких языках, работы с терминалом и взаимодействия с компьютером в реальных условиях. Модель оптимизирована для длительных рабочих процессов с использованием инструментов и поддерживает интерактивное управление в ходе выполнения задач, что делает её пригодной для сложных задач разработки, отладки, развёртывания и итеративной работы над продуктом.  
  
Версия с максимальным объемом размышлений (X-high). Больше размышлений могут сгенерировать больше токенов в ответе, что будет дороже, но обычно точнее.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.3 Codex (Thinking)

GPT-5.3-Codex — наиболее продвинутая агентная модель для написания кода от OpenAI, сочетающая в себе передовые возможности GPT-5.2-Codex в области разработки программного обеспечения с более широкими способностями к рассуждению и профессиональными знаниями GPT-5.2. Модель демонстрирует результаты на уровне лучших в отрасли по SWE-Bench Pro, а также высокую производительность на Terminal-Bench 2.0 и OSWorld-Verified, что отражает улучшенные навыки программирования на нескольких языках, работы с терминалом и взаимодействия с компьютером в реальных условиях. Модель оптимизирована для длительных рабочих процессов с использованием инструментов и поддерживает интерактивное управление в ходе выполнения задач, что делает её пригодной для сложных задач разработки, отладки, развёртывания и итеративной работы над продуктом.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 Codex (Thinking)

GPT-5.2-Codex — это улучшенная версия GPT-5.1-Codex, оптимизированная для программной инженерии и рабочих процессов кодирования. Она предназначена как для интерактивных сессий разработки, так и для длительного автономного выполнения сложных инженерных задач. Модель поддерживает создание проектов с нуля, разработку функций, отладку, крупномасштабный рефакторинг и проверку кода.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 Pro (Thinking High)

GPT-5.2 Pro — это самая продвинутая модель OpenAI, предлагающая значительные улучшения в агентном кодировании и производительности при работе с длинным контекстом по сравнению с GPT-5 Pro. Она оптимизирована для сложных задач, требующих пошагового рассуждения, следования инструкциям и точности в критически важных случаях использования.  
  
Вариант Thinking High - с большим числом размышлений при необходимости.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Модель НЕ поддерживает стриминг, используйте настройку без стриминга.  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 1200р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 Pro (Thinking)

GPT-5.2 Pro — это самая продвинутая модель OpenAI, предлагающая значительные улучшения в агентном кодировании и производительности при работе с длинным контекстом по сравнению с GPT-5 Pro. Она оптимизирована для сложных задач, требующих пошагового рассуждения, следования инструкциям и точности в критически важных случаях использования.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Модель НЕ поддерживает стриминг, используйте настройку без стриминга.  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 800р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 (Thinking X-High)

GPT-5.2 — это новейшая передовая модель в серии GPT-5, обеспечивающая более высокую агентную производительность и производительность при работе с длинным контекстом по сравнению с GPT-5.1. Она использует адаптивное рассуждение для динамического распределения вычислительных ресурсов, быстро отвечая на простые запросы и затрачивая больше времени на сложные задачи.  
  
Версия Thinking X-High с X-High пресетом на рассуждения (больше рассуждений при необходимости)  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 (Thinking High)

GPT-5.2 — это новейшая передовая модель в серии GPT-5, обеспечивающая более высокую агентную производительность и производительность при работе с длинным контекстом по сравнению с GPT-5.1. Она использует адаптивное рассуждение для динамического распределения вычислительных ресурсов, быстро отвечая на простые запросы и затрачивая больше времени на сложные задачи.  
  
Версия Thinking High с High пресетом на рассуждения (больше рассуждений при необходимости)  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 (Thinking)

GPT-5.2 — это новейшая передовая модель в серии GPT-5, обеспечивающая более высокую агентную производительность и производительность при работе с длинным контекстом по сравнению с GPT-5.1. Она использует адаптивное рассуждение для динамического распределения вычислительных ресурсов, быстро отвечая на простые запросы и затрачивая больше времени на сложные задачи.  
  
Созданная для широкого охвата задач, GPT-5.2 демонстрирует стабильное улучшение в математике, программировании, науке и при вызове инструментов, с более связными развёрнутыми ответами и повышенной надёжностью использования инструментов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.2 Chat

GPT-5.2 Chat (также известный как Instant) — это быстрый и облегченный член семейства 5.2, оптимизированный для чата с низкой задержкой при сохранении сильного общего интеллекта. Он использует адаптивное рассуждение для выборочного «обдумывания» более сложных запросов, повышая точность в математике, программировании и многошаговых задачах без замедления обычных разговоров. Модель по умолчанию более теплая и разговорная, с лучшим следованием инструкциям и более стабильными краткосрочными рассуждениями. GPT-5.2 Chat разработан для высокопроизводительных интерактивных задач, где скорость отклика и стабильность важнее глубокого обдумывания.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.1 Codex Max (Thinking)

GPT-5.1-Codex-Max — это новейшая агентная модель для программирования от OpenAI, разработанная для долгосрочных задач разработки программного обеспечения с высоким контекстом. Она основана на обновлённой версии стека рассуждений 5.1 и обучена на агентных рабочих процессах, охватывающих разработку программного обеспечения, математику и исследования.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.1 Codex Mini (Thinking)

GPT-5.1-Codex-Mini — это уменьшенная и более быстрая версия GPT-5.1-Codex.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.1 Codex (Thinking)

GPT-5.1-Codex — это специализированная версия GPT-5.1, оптимизированная для программной инженерии и рабочих процессов кодирования. Она разработана как для интерактивных сессий разработки, так и для длительного, самостоятельного выполнения сложных инженерных задач.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5.1 (Thinking)

GPT-5.1 — это новейшая передовая модель в серии GPT-5, предлагающая более сильные возможности рассуждения общего назначения, улучшенное следование инструкциям и более естественный разговорный стиль по сравнению с GPT-5. Модель использует адаптивное рассуждение для динамического распределения вычислительных ресурсов, быстро отвечая на простые запросы и уделяя больше внимания сложным задачам. Модель создаёт более чёткие и обоснованные объяснения с меньшим количеством жаргона, что облегчает понимание даже при работе с техническими или многоэтапными задачами.  
  
Созданная для широкого охвата задач, GPT-5.1 демонстрирует стабильные улучшения в математике, программировании и структурированном анализе, с более связными развёрнутыми ответами и улучшенной надёжностью использования инструментов. Модель также обладает усовершенствованной разговорной настройкой, обеспечивая более тёплые и интуитивные ответы без ущерба для точности. GPT-5.1 служит основным полнофункциональным преемником GPT-5.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Pro (Thinking)

GPT-5 Pro — это самая продвинутая модель OpenAI, предлагающая значительные улучшения в рассуждениях, качестве кода и пользовательском опыте.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Модель НЕ поддерживает стриминг, используйте настройку без стриминга.  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 800р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 (Thinking)

GPT-5 — это самая продвинутая модель OpenAI, предлагающая значительные улучшения в рассуждениях, качестве кода и пользовательском опыте.   
Данная версия размышляющая. Как описывают разработчики, можно углубить размышления модели, добавив фразу "think hard about this".  
  
Внимание: на некоторых запросах, которая GPT-5 считает простыми, она сама отключает размышления. К сожалению, это не регулируется.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Chat (устарела, перенаправляется в GPT 5.4)

GPT-5 Chat разработан для продвинутых, естественных, мультимодальных и контекстно-ориентированных диалогов для корпоративных приложений.  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Thinking Mini

GPT-5 Mini — это компактная версия GPT-5, разработанная для выполнения менее ресурсоемких задач рассуждения. Она обеспечивает те же преимущества в следовании инструкциям и настройке безопасности, что и GPT-5, но с уменьшенной задержкой и стоимостью. GPT-5 Mini является преемником модели o4-mini от OpenAI.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Nano

GPT-5-Nano — это самый маленький и быстрый вариант в системе GPT-5, оптимизированный для инструментов разработчиков, быстрых взаимодействий и сред с ультранизкой задержкой. Хотя он ограничен в глубине рассуждений по сравнению с более крупными аналогами, он сохраняет ключевые функции следования инструкциям и безопасности. Это преемник GPT-4.1-nano и предлагает легковесный вариант для чувствительных к стоимости или работающих в реальном времени приложений.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: gpt-oss-120b

gpt-oss-120b — это языковая модель с открытыми весами на 117 миллиардов параметров типа Mixture-of-Experts (MoE) от OpenAI, разработанная для высокоуровневых рассуждений, агентских задач и универсального промышленного применения. Она активирует 5,1 миллиарда параметров за один прямой проход и оптимизирована для работы на одном GPU H100 с нативной квантизацией MXFP4. Модель поддерживает настраиваемую глубину рассуждений, полный доступ к цепочке рассуждений и нативное использование инструментов.

Закрыть

X

### OpenAI: gpt-oss-120b (fast)

gpt-oss-120b — это языковая модель с открытыми весами на 117 миллиардов параметров типа Mixture-of-Experts (MoE) от OpenAI, разработанная для высокоуровневых рассуждений, агентских задач и универсального промышленного применения. Она активирует 5,1 миллиарда параметров за один прямой проход и оптимизирована для работы на одном GPU H100 с нативной квантизацией MXFP4. Модель поддерживает настраиваемую глубину рассуждений, полный доступ к цепочке рассуждений и нативное использование инструментов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: gpt-oss-20b (fast)

gpt-oss-20b — это модель с открытыми весами и 21 миллиардом параметров, выпущенная OpenAI под лицензией Apache 2.0. Она использует архитектуру Mixture-of-Experts (MoE) с 3,6 миллиардами активных параметров на один прямой проход, оптимизированную для вывода с низкой задержкой и развертывания на потребительском оборудовании или однопроцессорных GPU. Модель обучена в формате ответов OpenAI Harmony и поддерживает конфигурацию уровня рассуждений, тонкую настройку и агентные возможности, включая вызов функций, использование инструментов и структурированные выходные данные.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o3

ОБЩЕЕ ОПИСАНИЕ:  
Модели o3 оптимизированы для математики, науки, программирования и других задач, связанных с STEM. Они постоянно демонстрируют точность на уровне PhD в тестах по физике, химии и биологии.  
  
ОСОБЕННОСТИ БИЛЛИНГА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация.  
Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 150р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4o (2024-11-20) Online HQ

Версия GPT-4o от 20.11.2024 предлагает улучшенные возможности креативного письма с более естественным, увлекательным и индивидуальным подходом для повышения актуальности и удобства чтения. Модель выступает несколько хуже на логических задачах, но лучше - на задачах, требующих креативности.  
  
C расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Берется плата за вызов интернета (стоимость вызова модели) + дополнительная плата за найденные в интернете материалы в запросе (число символов во входе)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 16000 токенов**

Закрыть

X

### OpenAI: GPT-4o Online HQ

GPT-4o («o» от «omni») — это новейшая модель искусственного интеллекта OpenAI, поддерживающая как ввод текста, так и изображения, а также текстовый вывод. Он сохраняет уровень интеллекта GPT-4 Turbo, будучи в два раза быстрее и на 50 % экономичнее. GPT-4o также обеспечивает улучшенную производительность при обработке языков, отличных от английского, и расширенные визуальные возможности. Данные обучения: до октября 2023 г.  
  
C расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Берется плата за вызов интернета (стоимость вызова модели) + дополнительная плата за найденные в интернете материалы в запросе (число символов во входе)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o4-mini-high (пресет для глубоких размышлений от o4-mini)

ОБЩЕЕ ОПИСАНИЕ:  
OpenAI o4-mini — это компактная модель рассуждения в o-серии, оптимизированная для быстрой и экономичной производительности, сохраняющая при этом сильные мультимодальные и агентные возможности. Она поддерживает использование инструментов и демонстрирует конкурентоспособные показатели в рассуждениях и программировании по таким критериям, как AIME (99,5% с Python) и SWE-bench, превосходя своего предшественника o3-mini и даже приближаясь к o3 в некоторых областях.  
  
Несмотря на свой меньший размер, o4-mini демонстрирует высокую точность в задачах STEM, решении визуальных проблем (например, MathVista, MMMU) и редактировании кода. Она особенно хорошо подходит для сценариев с высокой пропускной способностью, где критичны задержки или стоимость. Благодаря эффективной архитектуре и усовершенствованному обучению с подкреплением, o4-mini может связывать инструменты, генерировать структурированные выходные данные и решать многоэтапные задачи с минимальной задержкой — часто менее чем за минуту.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o4-mini (для размышлений, не рек. для обычных задач)

ОБЩЕЕ ОПИСАНИЕ:  
OpenAI o4-mini — это компактная модель рассуждения в o-серии, оптимизированная для быстрой и экономичной производительности, сохраняющая при этом сильные мультимодальные и агентные возможности. Она поддерживает использование инструментов и демонстрирует конкурентоспособные показатели в рассуждениях и программировании по таким критериям, как AIME (99,5% с Python) и SWE-bench, превосходя своего предшественника o3-mini и даже приближаясь к o3 в некоторых областях.  
  
Несмотря на свой меньший размер, o4-mini демонстрирует высокую точность в задачах STEM, решении визуальных проблем (например, MathVista, MMMU) и редактировании кода. Она особенно хорошо подходит для сценариев с высокой пропускной способностью, где критичны задержки или стоимость. Благодаря эффективной архитектуре и усовершенствованному обучению с подкреплением, o4-mini может связывать инструменты, генерировать структурированные выходные данные и решать многоэтапные задачи с минимальной задержкой — часто менее чем за минуту.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4.1

GPT-4.1 — это флагманская большая языковая модель, оптимизированная для продвинутого следования инструкциям, реальной программной инженерии и рассуждений в длинном контексте. Она поддерживает контекстное окно в 1 миллион токенов и превосходит GPT-4o и GPT-4.5 в кодировании (54,6% SWE-bench Verified), соблюдении инструкций (87,4% IFEval) и мультимодальных тестах понимания. Она настроена на точные изменения кода, надежность агентов и высокую точность поиска в контексте больших документов, что делает ее идеальной для агентов, инструментов IDE и корпоративного поиска знаний.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 32000 токенов**

Закрыть

X

### OpenAI: GPT-4.1 Mini

GPT-4.1 Mini — модель среднего размера, обеспечивающая производительность, конкурирующую с GPT-4o при существенно меньшей задержке и стоимости. Она сохраняет контекстное окно в 1 миллион токенов и набирает 45,1% на сложных оценках инструкций, 35,8% на MultiChallenge и 84,1% на IFEval. Mini также демонстрирует сильные способности в программировании (например, 31,6% в полиглот-тесте на различия Aider) и понимании изображений, что делает её подходящей для интерактивных приложений с жёсткими требованиями к производительности.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 32000 токенов**

Закрыть

X

### OpenAI: GPT-4.1 Nano

Для задач, требующих низкой задержки, GPT-4.1 nano является самой быстрой и дешевой моделью в серии GPT-4.1. Она обеспечивает исключительную производительность при небольшом размере с контекстным окном в 1 миллион токенов и имеет показатели 80,1% в MMLU, 50,3% в GPQA и 9,8% в полиглотном кодировании Aider – даже выше, чем у GPT-4o mini. Она идеально подходит для таких задач, как классификация или автозаполнение.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 32000 токенов**

Закрыть

X

### OpenAI: o3-mini-high (пресет для глубоких размышлений от o3-mini)

Это вариант модели o3-mini с предустановленным пресетом high (больше размышлений, но дольше и больший расход токенов)  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o3-mini (для размышлений, не рек. для обычных задач)

ОБЩЕЕ ОПИСАНИЕ:  
OpenAI o3-mini - это экономичная языковая модель, оптимизированная для задач логического мышления в области STEM, особенно преуспевающая в науке, математике и программировании. Модель имеет три регулируемых уровня затрат на рассуждения (low, medium, high)  
  
При средних настройках уровня рассуждений o3-mini соответствует производительности более крупной модели o1 при сложных оценках рассуждений, таких как AIME и GPQA, сохраняя при этом меньшую задержку и стоимость.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o1 (для размышлений, не рек. для обычных задач)

ОБЩЕЕ ОПИСАНИЕ:  
Последнее и самое мощное семейство моделей от OpenAI, o1 разработано так, чтобы тратить больше времени на размышления перед ответом.  
  
Модели o1 оптимизированы для математики, науки, программирования и других задач, связанных с STEM. Они постоянно демонстрируют точность на уровне PhD в тестах по физике, химии и биологии.  
  
ОСОБЕННОСТИ БИЛЛИНГА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация.  
Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4o (2024-11-20)

Версия GPT-4o от 20.11.2024 предлагает улучшенные возможности креативного письма с более естественным, увлекательным и индивидуальным подходом для повышения актуальности и удобства чтения. Модель выступает несколько хуже на логических задачах, но лучше - на задачах, требующих креативности.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 16000 токенов**

Закрыть

X

### OpenAI: o1-mini (не рек. для обычных задач)

ОБЩЕЕ ОПИСАНИЕ:  
Последнее и самое мощное семейство моделей от OpenAI, o1 разработано так, чтобы тратить больше времени на размышления перед ответом.  
  
Модели o1 оптимизированы для математики, науки, программирования и других задач, связанных с STEM. Они постоянно демонстрируют точность на уровне PhD в тестах по физике, химии и биологии.  
  
RATE-LIMIT:  
В момент запуска (12-13 сентября) модель ОЧЕНЬ сильно ограничена в числе запросов и постоянно выдает ошибку 429 как экспериментальная модель. Позднее данные ограничения должны быть сняты.  
  
ОСОБЕННОСТИ БИЛЛИНГА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация.  
Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 30р.**

Закрыть

X

### OpenAI: GPT-4o (2024-08-06)

Версия GPT-4o от 2024-08-06 предлагает улучшенную производительность в структурированных выводах, с возможностью предоставления JSON-схемы в формате ответа.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4o mini

Самая последняя модель от OpenAI из семейства GPT-4o.  
Превосходит по цене и качеству GPT-3.5-Turbo, а также Claude 3 Haiku и Gemini Flash.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4o

GPT-4o («o» от «omni») — это новейшая модель искусственного интеллекта OpenAI, поддерживающая как ввод текста, так и изображения, а также текстовый вывод. Он сохраняет уровень интеллекта GPT-4 Turbo, будучи в два раза быстрее и на 50 % экономичнее. GPT-4o также обеспечивает улучшенную производительность при обработке языков, отличных от английского, и расширенные визуальные возможности. Данные обучения: до октября 2023 г.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-4 Turbo (gpt-4-turbo-2024-04-09)

Последняя модель GPT-4-Turbo.

Закрыть

X

### OpenAI: GPT-4

Самая мощная нейросетевая модель от OpenAI.

Закрыть

X

### OpenAI: GPT-3.5 Turbo

(В связи с отключением старых моделей OpenAI заменена на gpt-3.5-turbo-0613)

Закрыть

  

### Anthropic: Claude Sonnet, Opus, Haiku

  

**Нейросети от Anthropic** – основного конкурента OpenAI. Мы рекомендуем их пробовать, если нужна обработка больших текстов (файлов и пр.). Рекомендуем их нейросети Claude 3 – Haiku для дешевой и быстрой обработки большого контекста, Opus – для максимально качественной работы.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Anthropic: Claude Opus 5 (Thinking) [?](#mar717taskfull) anthropic/claude-opus-5-thinking  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 25 июл | да |
| Anthropic: Claude Opus 5 [?](#mar716taskfull) anthropic/claude-opus-5  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 25 июл | да |
| Anthropic: Claude Sonnet 5 (Thinking High) [?](#mar699taskfull) anthropic/claude-sonnet-5-thinking-high  Профессиональный (не Тестовый) топ от 30 июля tools structured-outputs   vision | 0.6 | 3.0 | 1000000 | 30 июн | да |
| Anthropic: Claude Sonnet 5 [?](#mar698taskfull) anthropic/claude-sonnet-5  Профессиональный (не Тестовый) топ от 30 июля tools structured-outputs   vision | 0.6 | 3.0 | 1000000 | 30 июн | да |
| Anthropic: Claude Opus 4.8 (Thinking) [?](#mar682taskfull) anthropic/claude-opus-4.8-thinking  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 28 мая | да |
| Anthropic: Claude Opus 4.8 [?](#mar681taskfull) anthropic/claude-opus-4.8  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 28 мая | да |
| Anthropic: Claude Opus 4.7 Thinking [?](#mar656taskfull) anthropic/claude-opus-4.7-thinking  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 17 апр | да |
| Anthropic: Claude Opus 4.7 [?](#mar655taskfull) anthropic/claude-opus-4.7  Профессиональный (не Тестовый) ТОП! tools structured-outputs   vision | 1.2 | 6.7 | 1000000 | 17 апр | да |
| Anthropic: Claude Sonnet 4.6 Deep Research 1.0 [?](#mar648taskfull) anthropic/claude-sonnet-4.6-deep-research-1.0  Профессиональный (не Тестовый) За вызов: 30.0 р. online, research примерная стоимость запроса 100-150 р. | 0.4 | 2.0 | 1000000 | 27 мар | да |
| Anthropic: Claude Sonnet 4.6 Online HQ [?](#mar647taskfull) anthropic/claude-sonnet-4.6-online-hq  Профессиональный (не Тестовый) За вызов: 2.0 р. онлайн | 0.4 | 2.0 | 1000000 | 27 мар | да |
| Anthropic: Claude Sonnet 4.6 (Thinking High, 1М контекста) [?](#mar596taskfull) anthropic/claude-sonnet-4.6-thinking-high  Профессиональный топ от 17 февраля tools structured-outputs | 0.4 | 2.0 | 1000000 | 17 фев | да |
| Anthropic: Claude Sonnet 4.6 (Thinking, 1M контекста) [?](#mar595taskfull) anthropic/claude-sonnet-4.6-thinking  Профессиональный топ от 17 февраля tools structured-outputs | 0.4 | 2.0 | 1000000 | 17 фев | да |
| Anthropic: Claude Sonnet 4.6 (1M контекста) [?](#mar594taskfull) anthropic/claude-sonnet-4.6  Профессиональный топ от 17 февраля tools structured-outputs | 0.4 | 2.0 | 1000000 | 17 фев | да |
| Anthropic: Claude Opus 4.6 (Thinking) [?](#mar588taskfull) anthropic/claude-opus-4.6-thinking  Профессиональный (не Тестовый) ТОП! tools structured-outputs | 0.75 | 3.4 | 1000000 | 6 фев | да |
| Anthropic: Claude Opus 4.6 [?](#mar587taskfull) anthropic/claude-opus-4.6  Профессиональный (не Тестовый) ТОП! tools structured-outputs | 0.75 | 3.4 | 1000000 | 6 фев | да |
| Anthropic: Claude Opus 4.5 (Thinking) [?](#mar549taskfull) anthropic/claude-opus-4.5-thinking  Профессиональный ТОП! tools structured-outputs | 0.75 | 3.4 | 200000 | 25 ноя 25 | да |
| Anthropic: Claude Opus 4.5 [?](#mar548taskfull) anthropic/claude-opus-4.5  Профессиональный ТОП! tools structured-outputs | 0.75 | 3.4 | 200000 | 25 ноя 25 | да |
| Anthropic: Claude Haiku 4.5 (Thinking) [?](#mar498taskfull) anthropic/claude-haiku-4.5-thinking  Профессиональный tools | 0.14 | 0.70 | 200000 | 16 окт 25 | да |
| Anthropic: Claude Haiku 4.5 [?](#mar497taskfull) anthropic/claude-haiku-4.5  Профессиональный tools | 0.14 | 0.70 | 200000 | 16 окт 25 | да |
| Anthropic: Claude Sonnet 4.5 1M context (Thinking) [?](#mar493taskfull) anthropic/claude-sonnet-4.5-1m-thinking  Профессиональный топ от 29 сентября tools structured-outputs | 0.7 | 2.6 | 1000000 | 29 сен 25 | да |
| Anthropic: Claude Sonnet 4.5 1M context [?](#mar492taskfull) anthropic/claude-sonnet-4.5-1m  Профессиональный топ от 29 сентября tools structured-outputs | 0.7 | 2.6 | 1000000 | 29 сен 25 | да |
| Anthropic: Claude Sonnet 4.5 (Thinking High) [?](#mar491taskfull) anthropic/claude-sonnet-4.5-thinking-high  Профессиональный топ от 29 сентября tools structured-outputs | 0.4 | 2.0 | 1000000 | 29 сен 25 | да |
| Anthropic: Claude Sonnet 4.5 (Thinking) [?](#mar490taskfull) anthropic/claude-sonnet-4.5-thinking  Профессиональный топ от 29 сентября tools structured-outputs | 0.4 | 2.0 | 1000000 | 29 сен 25 | да |
| Anthropic: Claude Sonnet 4.5 [?](#mar489taskfull) anthropic/claude-sonnet-4.5  Профессиональный топ от 29 сентября tools structured-outputs | 0.4 | 2.0 | 200000 | 29 сен 25 | да |
| Anthropic: Claude Sonnet 4 (1M контекста) Thinking [?](#mar450taskfull) anthropic/claude-sonnet-4-1m-thinking  Профессиональный (не Тестовый) топ от 22 мая tools | 0.65 | 2.6 | 1000000 | 13 авг 25 | да |
| Anthropic: Claude Sonnet 4 (1M контекста) [?](#mar449taskfull) anthropic/claude-sonnet-4-1m  Профессиональный (не Тестовый) топ от 22 мая tools | 0.65 | 2.6 | 1000000 | 13 авг 25 | да |
| Anthropic: Claude Opus 4.1 Thinking [?](#mar442taskfull) anthropic/claude-opus-4.1-thinking  Профессиональный ТОП! tools | 2.0 | 10.0 | 200000 | 7 авг 25 | да |
| Anthropic: Claude Opus 4.1 [?](#mar441taskfull) anthropic/claude-opus-4.1  Профессиональный ТОП! tools | 2.0 | 10.0 | 200000 | 7 авг 25 | да |
| Anthropic: Claude Opus 4 Deep Research 1.0 [?](#mar384taskfull) anthropic/claude-opus-4-deep-research-1.0  Профессиональный (не Тестовый) За вызов: 60.0 р. топ от 28 мая online, research примерная стоимость запроса 500-600 р. | 2.0 | 10.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Opus 4 Online HQ [?](#mar383taskfull) anthropic/claude-opus-4-online-hq  Профессиональный (не Тестовый) За вызов: 4.0 р. топ от 28 мая онлайн | 2.0 | 10.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Sonnet 4 Deep Research 1.0 [?](#mar382taskfull) anthropic/claude-sonnet-4-deep-research-1.0  Профессиональный (не Тестовый) За вызов: 30.0 р. топ от 28 мая online, research примерная стоимость запроса 100-150 р. | 0.4 | 2.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Sonnet 4 Deep Online [?](#mar381taskfull) anthropic/claude-sonnet-4-deep-online  Профессиональный (не Тестовый) За вызов: 12.0 р. топ от 28 мая онлайн примерная стоимость запроса 30-50 р. | 0.4 | 2.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Sonnet 4 Research [?](#mar380taskfull) anthropic/claude-sonnet-4-online-research  Профессиональный (не Тестовый) За вызов: 20.0 р. топ от 28 мая online, research примерная стоимость запроса 80-120 р. | 0.4 | 2.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Sonnet 4 Online HQ [?](#mar379taskfull) anthropic/claude-sonnet-4-online-hq  Профессиональный (не Тестовый) За вызов: 2.0 р. топ от 28 мая онлайн | 0.4 | 2.0 | 200000 | 28 мая 25 | да |
| Anthropic: Claude Opus 4 (Thinking High) [?](#mar376taskfull) anthropic/claude-opus-4-thinking-high  Профессиональный (не Тестовый) размышления tools | 2.0 | 10.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude Sonnet 4 (Thinking High) [?](#mar375taskfull) anthropic/claude-sonnet-4-thinking-high  Профессиональный (не Тестовый) топ от 22 мая размышления tools | 0.4 | 2.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude Opus 4 (Thinking) [?](#mar374taskfull) anthropic/claude-opus-4-thinking  Профессиональный (не Тестовый) ТОП! размышления tools | 2.0 | 10.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude Sonnet 4 (Thinking) [?](#mar373taskfull) anthropic/claude-sonnet-4-thinking  Профессиональный (не Тестовый) топ от 22 мая размышления tools | 0.4 | 2.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude Opus 4 [?](#mar372taskfull) anthropic/claude-opus-4  Профессиональный ТОП! tools | 2.0 | 10.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude Sonnet 4 [?](#mar371taskfull) anthropic/claude-sonnet-4  Профессиональный топ от 22 мая tools | 0.4 | 2.0 | 200000 | 22 мая 25 | да |
| Anthropic: Claude 3 Haiku [?](#mar84taskfull) anthropic/claude-3-haiku  дешевая и с большим контекстом tools | 0.0375 | 0.1875 | 200000 | 14 мар 24 | да |

X

### Anthropic: Claude Opus 5 (Thinking)

Claude Opus 5 — флагманская модель Anthropic для сложных задач, требующих глубокого рассуждения, написания кода и длительной агентной работы. Модель особенно хорошо справляется с комплексными задачами в области разработки программного обеспечения, проверкой кода и поиском ошибок, визуальным анализом графиков и документов, подготовкой сложных рабочих материалов, а также координацией параллельных субагентов.  
  
Модель уверенно следует инструкциям и работает с инструментами в рамках длительных задач, при этом оставаясь эффективной в режиме сниженной нагрузки для сценариев, где приоритетом являются скорость отклика и экономия токенов.  
  
Модель особенно сильна в многошаговых рассуждениях, сложном программировании и сквозной оркестрации проектов: работе с крупными кодовыми базами, многоэтапной отладке и длительно выполняющимися асинхронными агентными пайплайнами. Помимо написания кода, она справляется с интеллектуальными задачами: составлением документов, созданием презентаций и анализом данных, сохраняя высокое качество даже при очень больших объёмах выходных данных.  
  
Размышляющая версия.  
  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 800р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 5

Claude Opus 5 — флагманская модель Anthropic для сложных задач, требующих глубокого рассуждения, написания кода и длительной агентной работы. Модель особенно хорошо справляется с комплексными задачами в области разработки программного обеспечения, проверкой кода и поиском ошибок, визуальным анализом графиков и документов, подготовкой сложных рабочих материалов, а также координацией параллельных субагентов.  
  
Модель уверенно следует инструкциям и работает с инструментами в рамках длительных задач, при этом оставаясь эффективной в режиме сниженной нагрузки для сценариев, где приоритетом являются скорость отклика и экономия токенов.  
  
Модель особенно сильна в многошаговых рассуждениях, сложном программировании и сквозной оркестрации проектов: работе с крупными кодовыми базами, многоэтапной отладке и длительно выполняющимися асинхронными агентными пайплайнами. Помимо написания кода, она справляется с интеллектуальными задачами: составлением документов, созданием презентаций и анализом данных, сохраняя высокое качество даже при очень больших объёмах выходных данных.  
  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 400р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 5 (Thinking High)

Sonnet 5 — самая мощная модель класса Sonnet от Anthropic, демонстрирующая передовые результаты в программировании, работе с агентами и решении профессиональных задач.  
  
Размышляющая версия, уровень размышлений High.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 5

Sonnet 5 — самая мощная модель класса Sonnet от Anthropic, демонстрирующая передовые результаты в программировании, работе с агентами и решении профессиональных задач.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.8 (Thinking)

Claude Opus 4.8 — самая мощная из общедоступных моделей Anthropic в семействе Opus. Она поддерживает текстовые, графические и файловые входные данные с текстовым выводом, располагает возможностью рассуждения и контекстным окном в 1 миллион токенов. Модель идеально подходит для высокоавтономных агентов, долгосрочных агентных задач, работы со знаниями и задач, требующих памяти, — там, где важна согласованность на протяжении длительных сессий.  
  
Модель особенно сильна в многошаговых рассуждениях, сложном программировании и сквозной оркестрации проектов: работе с крупными кодовыми базами, многоэтапной отладке и длительно выполняющимися асинхронными агентными пайплайнами. Помимо написания кода, она справляется с интеллектуальными задачами: составлением документов, созданием презентаций и анализом данных, сохраняя высокое качество даже при очень больших объёмах выходных данных.  
  
Размышляющая версия.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.8

Claude Opus 4.8 — самая мощная из общедоступных моделей Anthropic в семействе Opus. Она поддерживает текстовые, графические и файловые входные данные с текстовым выводом, располагает возможностью рассуждения и контекстным окном в 1 миллион токенов. Модель идеально подходит для высокоавтономных агентов, долгосрочных агентных задач, работы со знаниями и задач, требующих памяти, — там, где важна согласованность на протяжении длительных сессий.  
  
Модель особенно сильна в многошаговых рассуждениях, сложном программировании и сквозной оркестрации проектов: работе с крупными кодовыми базами, многоэтапной отладке и длительно выполняющимися асинхронными агентными пайплайнами. Помимо написания кода, она справляется с интеллектуальными задачами: составлением документов, созданием презентаций и анализом данных, сохраняя высокое качество даже при очень больших объёмах выходных данных.  
  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.7 Thinking

Claude Opus 4.7 — это флагманская модель Anthropic, выпущенная в апреле 2026 года. Она превосходит Opus 4.6 в агентском кодинге (64.3% SWE-bench Pro, 87.6% SWE-bench Verified), знаниях (64.4% Finance Agent), долгосрочных задачах с 1M+ контекстом и зрении (до 2576 пикселей, 98.5% XBOW).  
  
Размышляющая версия.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.7

Claude Opus 4.7 — это флагманская модель Anthropic, выпущенная в апреле 2026 года. Она превосходит Opus 4.6 в агентском кодинге (64.3% SWE-bench Pro, 87.6% SWE-bench Verified), знаниях (64.4% Finance Agent), долгосрочных задачах с 1M+ контекстом и зрении (до 2576 пикселей, 98.5% XBOW).  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.   
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 Deep Research 1.0

**Модель позволяет одним запросом получить расширенный исследовательский отчет.**  
  
Версия Sonnet 4.6 Thinking с расширенным поиском по интернету и формированием полноценного отчета  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
В процессе запроса  
- выбираются наиболее релевантные источники  
- из их текста делается выжимка по пользовательскому запросу с помощью gpt-4o-mini, что увеличивает в 2-3 раза число фактической информации, по которой делается анализ. Вызовы gpt-4o-mini для всех источников будет показан в Активности пользователя и оплачивается дополнительно (около 0.5 р. за вызов)  
  
[Информация о research и примеры отчета](https://vsegpt.ru/ExtTools/Research)  
[Примеры отчета Deep 1.0 в PDF](https://vsegpt.ru/pdfs/research_5070_vs_4090_deep_10.pdf)  
  
**Особенности функционирования**  
  
- Будет рассмотрен только запрос пользователя. Предыдущий чат и инструкции будут проигнорированы.  
- При работе модель подменяет ваши предыдущие запросы и настройки собственным системным промтом и настройками максимальной генерации - т.е. входной промт будет большим, это нормально.  
- Research можно вызывать по API так же, как любую другую нейросетевую модель – просто передайте в последнем сообщении пользователя необходимый запрос.   
  
**Минимальный баланс для вызова модели: 250р.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 Online HQ

Версия Sonnet 4 с расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Средняя полная стоимость запроса (без истории чата) - 10-15 рублей за запрос.  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 (Thinking High, 1М контекста)

Claude Sonnet 4.6 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами.   
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 (Thinking, 1M контекста)

Claude Sonnet 4.6 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами.   
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 (1M контекста)

Claude Sonnet 4.6 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами.   
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.6 (Thinking)

Opus 4.6 — это самая мощная модель Anthropic для программирования и длительных профессиональных задач. Она создана для агентов, которые работают с целыми рабочими процессами, а не с отдельными запросами, что делает её особенно эффективной для больших кодовых баз, сложных рефакторингов и многоэтапной отладки, которая разворачивается со временем. Модель демонстрирует более глубокое контекстное понимание, более сильную декомпозицию задач и большую надёжность в сложных инженерных задачах по сравнению с предыдущими поколениями.  
  
Размышляющая версия.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.6

Opus 4.6 — это самая мощная модель Anthropic для программирования и длительных профессиональных задач. Она создана для агентов, которые работают с целыми рабочими процессами, а не с отдельными запросами, что делает её особенно эффективной для больших кодовых баз, сложных рефакторингов и многоэтапной отладки, которая разворачивается со временем. Модель демонстрирует более глубокое контекстное понимание, более сильную декомпозицию задач и большую надёжность в сложных инженерных задачах по сравнению с предыдущими поколениями.  
  
Помимо программирования, Opus 4.6 превосходно справляется с продолжительной интеллектуальной работой. Она создаёт документы, планы и анализы, близкие к готовым для продакшена, за один проход и сохраняет связность на протяжении очень длинных результатов и продолжительных сессий. Это делает её надёжным выбором по умолчанию для задач, требующих настойчивости, здравого суждения и доведения до конца, таких как техническое проектирование, планирование миграции и сквозное выполнение проектов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.5 (Thinking)

Claude Opus 4.5 — это передовая модель рассуждений от Anthropic, оптимизированная для сложной разработки программного обеспечения, агентных рабочих процессов и длительного использования компьютера. Она обладает мощными мультимодальными возможностями, конкурентоспособной производительностью в реальных тестах программирования и рассуждений, а также улучшенной устойчивостью к инъекциям промптов.   
  
Размышляющая версия.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.5

Claude Opus 4.5 — это передовая модель рассуждений от Anthropic, оптимизированная для сложной разработки программного обеспечения, агентных рабочих процессов и длительного использования компьютера. Она обладает мощными мультимодальными возможностями, конкурентоспособной производительностью в реальных тестах программирования и рассуждений, а также улучшенной устойчивостью к инъекциям промптов. Модель разработана для эффективной работы при различных уровнях усилий, что позволяет разработчикам балансировать между скоростью, глубиной и использованием токенов в зависимости от требований задачи.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Haiku 4.5 (Thinking)

Claude Haiku 4.5 — это самая быстрая и эффективная модель Anthropic, обеспечивающая интеллект, близкий к передовому уровню, при значительно меньших затратах и задержке по сравнению с более крупными моделями Claude. Соответствуя производительности Claude Sonnet 4 в задачах рассуждения, программирования и использования компьютера, Haiku 4.5 привносит возможности передового уровня в приложения реального времени и высоконагруженные приложения.  
  
Версия с размышлениями  
Модель представляет расширенное мышление в линейке Haiku; обеспечивая управляемую глубину рассуждений, сжатый или чередующийся вывод мыслей и рабочие процессы с использованием инструментов при полной поддержке инструментов программирования, bash, веб-поиска и использования компьютера. Набрав >73% в SWE-bench Verified, Haiku 4.5 входит в число лучших моделей программирования в мире, сохраняя при этом исключительную отзывчивость для подагентов, параллельного выполнения и масштабируемого развертывания.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Haiku 4.5

Claude Haiku 4.5 — это самая быстрая и эффективная модель Anthropic, обеспечивающая интеллект, близкий к передовому уровню, при значительно меньших затратах и задержке по сравнению с более крупными моделями Claude. Соответствуя производительности Claude Sonnet 4 в задачах рассуждения, программирования и использования компьютера, Haiku 4.5 привносит возможности передового уровня в приложения реального времени и высоконагруженные приложения.  
  
Модель представляет расширенное мышление в линейке Haiku; обеспечивая управляемую глубину рассуждений, сжатый или чередующийся вывод мыслей и рабочие процессы с использованием инструментов при полной поддержке инструментов программирования, bash, веб-поиска и использования компьютера. Набрав >73% в SWE-bench Verified, Haiku 4.5 входит в число лучших моделей программирования в мире, сохраняя при этом исключительную отзывчивость для подагентов, параллельного выполнения и масштабируемого развертывания.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.5 1M context (Thinking)

Claude Sonnet 4.5 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами. Она демонстрирует передовые результаты в тестах по программированию, таких как SWE-bench Verified, с улучшениями в области системного проектирования, безопасности кода и соответствия спецификациям.  
  
(Размышляющая версия модели)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.5 1M context

Claude Sonnet 4.5 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами. Она демонстрирует передовые результаты в тестах по программированию, таких как SWE-bench Verified, с улучшениями в области системного проектирования, безопасности кода и соответствия спецификациям.  
  
Версия на 1 миллион контекста  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.5 (Thinking High)

Claude Sonnet 4.5 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами. Она демонстрирует передовые результаты в тестах по программированию, таких как SWE-bench Verified, с улучшениями в области системного проектирования, безопасности кода и соответствия спецификациям.  
  
(Размышляющая версия модели, High уровень размышлений)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.5 (Thinking)

Claude Sonnet 4.5 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами. Она демонстрирует передовые результаты в тестах по программированию, таких как SWE-bench Verified, с улучшениями в области системного проектирования, безопасности кода и соответствия спецификациям.  
  
(Размышляющая версия модели)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.5

Claude Sonnet 4.5 — самая совершенная модель Sonnet от Anthropic на сегодняшний день, оптимизированная для работы с реальными агентами и программными процессами. Она демонстрирует передовые результаты в тестах по программированию, таких как SWE-bench Verified, с улучшениями в области системного проектирования, безопасности кода и соответствия спецификациям.  
  
Это версия на 200К контекста, версия на 1M контекста идет отдельно.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4 (1M контекста) Thinking

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  
  
Версия на 1 миллион контекста, несколько дороже. Размышляющая.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4 (1M контекста)

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  
  
Версия на 1 миллион контекста, несколько дороже.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.1 Thinking

Claude Opus 4.1 — это обновленная версия флагманской модели Anthropic, предлагающая улучшенную производительность в программировании, рассуждениях и агентных задачах. Она достигает 74,5% на SWE-bench Verified и демонстрирует заметные улучшения в рефакторинге многофайлового кода, точности отладки и детально-ориентированных рассуждениях. Модель поддерживает расширенное мышление до 64К токенов и оптимизирована для задач, включающих исследования, анализ данных и рассуждения с использованием инструментов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.1

Claude Opus 4.1 — это обновленная версия флагманской модели Anthropic, предлагающая улучшенную производительность в программировании, рассуждениях и агентных задачах. Она достигает 74,5% на SWE-bench Verified и демонстрирует заметные улучшения в рефакторинге многофайлового кода, точности отладки и детально-ориентированных рассуждениях. Модель поддерживает расширенное мышление до 64К токенов и оптимизирована для задач, включающих исследования, анализ данных и рассуждения с использованием инструментов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4 Deep Research 1.0

**Модель позволяет одним запросом получить расширенный исследовательский отчет.**  
  
Версия Opus 4 Thinking с расширенным поиском по интернету и формированием полноценного отчета  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
В процессе запроса  
- выбираются наиболее релевантные источники  
- из их текста делается выжимка по пользовательскому запросу с помощью gpt-4o-mini, что увеличивает в 2-3 раза число фактической информации, по которой делается анализ. Вызовы gpt-4o-mini для всех источников будет показан в Активности пользователя и оплачивается дополнительно (около 0.5 р. за вызов)  
  
[Информация о research и примеры отчета](https://vsegpt.ru/ExtTools/Research)  
[Примеры отчета Deep 1.0 в PDF](https://vsegpt.ru/pdfs/research_5070_vs_4090_deep_10.pdf)  
  
**Особенности функционирования**  
  
- Будет рассмотрен только запрос пользователя. Предыдущий чат и инструкции будут проигнорированы.  
- При работе модель подменяет ваши предыдущие запросы и настройки собственным системным промтом и настройками максимальной генерации - т.е. входной промт будет большим, это нормально.  
- Research можно вызывать по API так же, как любую другую нейросетевую модель – просто передайте в последнем сообщении пользователя необходимый запрос.   
  
**Минимальный баланс для вызова модели: 1000р.**

Закрыть

X

### Anthropic: Claude Opus 4 Online HQ

Версия Opus 4 с расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Средняя полная стоимость запроса (без истории чата) - 50-65 рублей за запрос.  
**Минимальный баланс для вызова модели: 250р.**

Закрыть

X

### Anthropic: Claude Sonnet 4 Deep Research 1.0

**Модель позволяет одним запросом получить расширенный исследовательский отчет.**  
  
Версия Sonnet 4 Thinking с расширенным поиском по интернету и формированием полноценного отчета  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
В процессе запроса  
- выбираются наиболее релевантные источники  
- из их текста делается выжимка по пользовательскому запросу с помощью gpt-4o-mini, что увеличивает в 2-3 раза число фактической информации, по которой делается анализ. Вызовы gpt-4o-mini для всех источников будет показан в Активности пользователя и оплачивается дополнительно (около 0.5 р. за вызов)  
  
[Информация о research и примеры отчета](https://vsegpt.ru/ExtTools/Research)  
[Примеры отчета Deep 1.0 в PDF](https://vsegpt.ru/pdfs/research_5070_vs_4090_deep_10.pdf)  
  
**Особенности функционирования**  
  
- Будет рассмотрен только запрос пользователя. Предыдущий чат и инструкции будут проигнорированы.  
- При работе модель подменяет ваши предыдущие запросы и настройки собственным системным промтом и настройками максимальной генерации - т.е. входной промт будет большим, это нормально.  
- Research можно вызывать по API так же, как любую другую нейросетевую модель – просто передайте в последнем сообщении пользователя необходимый запрос.   
  
**Минимальный баланс для вызова модели: 250р.**

Закрыть

X

### Anthropic: Claude Sonnet 4 Deep Online

Версия Sonnet 4 с расширенным поиском по интернету и анализом источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
В процессе запроса  
- выбираются наиболее релевантные источники  
- из их текста делается выжимка по пользовательскому запросу с помощью gpt-4o-mini, что увеличивает в 2-3 раза число фактической информации, по которой делается анализ. Вызовы gpt-4o-mini для всех источников будет показан в Активности пользователя и оплачивается дополнительно (около 0.5 р. за вызов)  
  
Средняя полная стоимость запроса (без истории чата) - 30-50 рублей за запрос.  
**Минимальный баланс для вызова модели: 70р.**

Закрыть

X

### Anthropic: Claude Sonnet 4 Research

**Модель позволяет одним запросом получить расширенный исследовательский отчет.**  
  
Версия Sonnet 4 Thinking с расширенным поиском по интернету и формированием полноценного отчета  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Средняя полная стоимость запроса (без истории чата) - 80-120 рублей за запрос.  
  
[Информация о research и примеры отчета](https://vsegpt.ru/ExtTools/Research)  
[Примеры отчета в PDF](https://vsegpt.ru/pdfs/research_5070_vs_4090.pdf)  
  
**Особенности функционирования**  
  
- Будет рассмотрен только запрос пользователя. Предыдущий чат и инструкции будут проигнорированы.  
- При работе модель подменяет ваши предыдущие запросы и настройки собственным системным промтом и настройками максимальной генерации - т.е. входной промт будет большим, это нормально.  
- Research можно вызывать по API так же, как любую другую нейросетевую модель – просто передайте в последнем сообщении пользователя необходимый запрос.   
  
  
**Минимальный баланс для вызова модели: 200р.**

Закрыть

X

### Anthropic: Claude Sonnet 4 Online HQ

Версия Sonnet 4 с расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
Средняя полная стоимость запроса (без истории чата) - 10-15 рублей за запрос.  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Anthropic: Claude Opus 4 (Thinking High)

Claude Opus 4 признан лучшей в мире моделью для программирования на момент выпуска, обеспечивая стабильную производительность при выполнении сложных, длительных задач и агентных рабочих процессов. Он устанавливает новые эталоны в программной инженерии, достигая ведущих результатов в SWE-bench (72,5%) и Terminal-bench (43,2%). Opus 4 поддерживает расширенные агентные рабочие процессы, обрабатывая тысячи шагов задач непрерывно в течение часов без ухудшения производительности.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4 (Thinking High)

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4 (Thinking)

Claude Opus 4 признан лучшей в мире моделью для программирования на момент выпуска, обеспечивая стабильную производительность при выполнении сложных, длительных задач и агентных рабочих процессов. Он устанавливает новые эталоны в программной инженерии, достигая ведущих результатов в SWE-bench (72,5%) и Terminal-bench (43,2%). Opus 4 поддерживает расширенные агентные рабочие процессы, обрабатывая тысячи шагов задач непрерывно в течение часов без ухудшения производительности.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4 (Thinking)

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4

Claude Opus 4 признан лучшей в мире моделью для программирования на момент выпуска, обеспечивая стабильную производительность при выполнении сложных, длительных задач и агентных рабочих процессов. Он устанавливает новые эталоны в программной инженерии, достигая ведущих результатов в SWE-bench (72,5%) и Terminal-bench (43,2%). Opus 4 поддерживает расширенные агентные рабочие процессы, обрабатывая тысячи шагов задач непрерывно в течение часов без ухудшения производительности.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude 3 Haiku

Claude 3 Haiku — самая быстрая и компактная модель Anthropic, обеспечивающая практически мгновенное реагирование. Быстрая и точная целевая производительность.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 4096 токенов**

Закрыть

  

### Perplexity: онлайн, с доступом к Интернету и фактической информации

  

**Нейросети от Perplexity**, сфокусированные на более точным следованиям фактам. Онлайн-модели (online в конце) перед запросом предположительно запрашивают свежие данные в Интернете, после чего формируют ответ – и, например, могут отвечать о погоде сегодня, о курсе доллара и пр. Также модели можно передавать ссылку на конкретную страницу в Интернете и с высокой вероятностью получить релевантный ответ.  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)Наша новость на Хабре о моделях Perplexity](https://habr.com/ru/news/778552/ "Внешняя ссылка (откроется в новом окне)")  
  
**Внимание:** онлайн-модель дополнительно тарифицируется по каждому запросу (т.к. идет вызов онлайн-поиска). Модель НЕ поддерживает чат – каждый запрос учитывает только последнее сообщение пользователя.  
  
**Рекомендация:** поскольку Perplexity постоянно выпускает новые модели и удаляет обработку старых, рекомендуется установить в ваших приложениях ID псевдонима для малой или большой модели – тогда сервис сам перенаправит ваш запрос в самую последнюю версию (по ней и будет происходить тарификация)

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Perplexity: Sonar Reasoning Pro [?](#mar378taskfull) perplexity/sonar-reasoning-pro-online  Профессиональный (не Тестовый) За вызов: 8.0 р. онлайн | 0.30 | 1.20 | 128000 | 28 мая 25 | нет |
| Perplexity: Sonar Pro [?](#mar377taskfull) perplexity/sonar-pro-online  Профессиональный (не Тестовый) За вызов: 8.0 р. онлайн | 0.45 | 2.20 | 128000 | 28 мая 25 | нет |
| Perplexity: Sonar [?](#mar266taskfull) perplexity/sonar-online  За вызов: 0.85 р. рекомендуется онлайн | 0.15 | 0.15 | 128000 | 31 янв 25 | нет |
| Perplexity, последняя большая онлайн модель (перенаправляет в нужный ID) perplexity/latest-large-online  рекомендуется онлайн | 0 | 0 | 32000 | 8 авг 24 | нет |
| Perplexity, последняя малая онлайн модель (перенаправляет в нужный ID) perplexity/latest-small-online  онлайн | 0 | 0 | 32000 | 8 авг 24 | нет |

X

### Perplexity: Sonar Reasoning Pro

Улучшенная модель рассуждений с возможностями многоэтапного решения проблем и поиска в реальном времени.

Закрыть

X

### Perplexity: Sonar Pro

Для предприятий, ищущих более продвинутые возможности, API Sonar Pro может обрабатывать углубленные многошаговые запросы с дополнительной расширяемостью, например, в среднем в два раза больше цитат на поиск, чем Sonar. Кроме того, благодаря большему контекстному окну, он может обрабатывать более длинные и нюансированные поисковые запросы и последующие вопросы.

Закрыть

X

### Perplexity: Sonar

Сонар - легкий, доступный, быстрый и простой в использовании инструмент, теперь с функцией цитирования и возможностью настройки источников.

Закрыть

  
  

### Google: Gemini Pro, Flash

  

**Нейросети от Google**. Достаточно **дешевые**.  
Рекомендуются последние версии Gemini, однако пользователи жалуются, что даже при не очень большом контексте (5К+ символов) Google относительно часто возвращает ошибки и очень маленькие ответы (июнь 2024).  
В случае, если нужна точность, рекомендуем модели Claude 3 с большим контекстом.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Gemini 3.8 Flash (Thinking High) [?](#mar740taskfull) google/gemini-3.8-flash-high  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.225 | 1.125 | 1000000 | 2 сен | нет |
| Gemini 3.8 Flash (Thinking Minimal) [?](#mar739taskfull) google/gemini-3.8-flash-minimal  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.225 | 1.125 | 1000000 | 2 сен | нет |
| Gemini 3.7 Flash (Thinking High) [?](#mar724taskfull) google/gemini-3.7-flash-high  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.225 | 1.125 | 1000000 | 14 авг | нет |
| Gemini 3.7 Flash (Thinking Minimal) [?](#mar723taskfull) google/gemini-3.7-flash-minimal  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.225 | 1.125 | 1000000 | 14 авг | нет |
| Gemini 3.6 Flash (Thinking High) [?](#mar715taskfull) google/gemini-3.6-flash-high  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.45 | 2.25 | 1000000 | 22 июл | нет |
| Gemini 3.6 Flash (Thinking Minimal) [?](#mar714taskfull) google/gemini-3.6-flash-minimal  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.45 | 2.25 | 1000000 | 22 июл | нет |
| Gemini 3.5 Flash Lite (Thinking High) [?](#mar713taskfull) google/gemini-3.5-flash-lite-high  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.09 | 0.75 | 1000000 | 22 июл | нет |
| Gemini 3.5 Flash Lite (Thinking Minimal) [?](#mar712taskfull) google/gemini-3.5-flash-lite-minimal  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.09 | 0.75 | 1000000 | 22 июл | нет |
| Gemini 3.5 Flash (Thinking High) [?](#mar680taskfull) google/gemini-3.5-flash-high  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.45 | 2.70 | 1000000 | 20 мая | нет |
| Gemini 3.5 Flash (Thinking Minimal) [?](#mar679taskfull) google/gemini-3.5-flash-minimal  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.45 | 2.70 | 1000000 | 20 мая | нет |
| Gemini 3.5 Flash (Thinking Medium) [?](#mar678taskfull) google/gemini-3.5-flash  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.45 | 2.70 | 1000000 | 20 мая | нет |
| Gemini 3.1 Flash Lite (Thinking High) [?](#mar677taskfull) google/gemini-3.1-flash-lite-thinking-high  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.075 | 0.45 | 1000000 | 20 мая | нет |
| Gemini 3.1 Flash Lite (Thinking) [?](#mar676taskfull) google/gemini-3.1-flash-lite-thinking  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.075 | 0.45 | 1000000 | 20 мая | нет |
| Gemini 3.1 Flash Lite [?](#mar675taskfull) google/gemini-3.1-flash-lite  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.075 | 0.45 | 1000000 | 20 мая | нет |
| Google: Gemma 4 26B A4B (Thinking) [?](#mar654taskfull) google/gemma-4-26b-a4b-it-thinking  tools structured-outputs   vision | 0.04 | 0.13 | 260000 | 10 апр | нет |
| Google: Gemma 4 26B A4B [?](#mar653taskfull) google/gemma-4-26b-a4b-it  tools structured-outputs   vision | 0.04 | 0.13 | 260000 | 10 апр | нет |
| Google: Gemma 4 31B (Thinking) [?](#mar652taskfull) google/gemma-4-31b-it-thinking  tools structured-outputs   vision | 0.045 | 0.13 | 260000 | 10 апр | нет |
| Google: Gemma 4 31B [?](#mar651taskfull) google/gemma-4-31b-it  tools structured-outputs   vision | 0.045 | 0.13 | 260000 | 10 апр | нет |
| Gemini 3.1 Flash Lite Preview (Thinking High) [?](#mar614taskfull) google/gemini-3.1-flash-lite-pre-thinking  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.075 | 0.45 | 1000000 | 3 мар | нет |
| Gemini 3.1 Flash Lite Preview [?](#mar613taskfull) google/gemini-3.1-flash-lite-pre  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.075 | 0.45 | 1000000 | 3 мар | нет |
| Google: Gemini 3.1 Pro Preview (версия на 1М контекста) [?](#mar605taskfull) google/gemini-3.1-pro-preview-1m  Профессиональный (не Тестовый) топ tools structured-outputs   vision | 1.10 | 4.95 | 1000000 | 20 фев | нет |
| Google: Gemini 3.1 Pro Preview (версия на 200К контекста) [?](#mar604taskfull) google/gemini-3.1-pro-preview  Профессиональный (не Тестовый) топ tools structured-outputs | 0.55 | 3.30 | 200000 | 20 фев | нет |
| Google: Gemini 3 Flash Preview (Thinking) [?](#mar568taskfull) google/gemini-3-flash-pre-thinking  Базовый и выше (не Тестовый) tools structured-outputs | 0.15 | 0.90 | 1000000 | 17 дек 25 | нет |
| Google: Gemini 3 Flash Preview [?](#mar567taskfull) google/gemini-3-flash-pre  Базовый и выше (не Тестовый) tools structured-outputs | 0.15 | 0.90 | 1000000 | 17 дек 25 | нет |
| Google: Gemini 2.5 Flash Lite [?](#mar432taskfull) google/gemini-2.5-flash-lite  дешевая и с большим контекстом tools structured-outputs | 0.015 | 0.06 | 1000000 | 23 июл 25 | нет |
| Google: Gemini 2.5 Flash (Thinking) [?](#mar401taskfull) google/gemini-2.5-flash-thinking  tools structured-outputs | 0.09 | 0.75 | 1000000 | 17 июн 25 | нет |
| Google: Gemini 2.5 Flash [?](#mar400taskfull) google/gemini-2.5-flash  tools structured-outputs | 0.09 | 0.75 | 1000000 | 17 июн 25 | нет |
| Google: Gemini 2.5 Pro [?](#mar397taskfull) google/gemini-2.5-pro  Профессиональный tools structured-outputs | 0.37 | 3.0 | 1000000 | 17 июн 25 | нет |
| Google: Gemini 2.5 Pro Preview (обновлена 5 июня) [?](#mar393taskfull) google/gemini-2.5-pro-preview  Профессиональный tools structured-outputs | 0.37 | 3.0 | 1000000 | 5 июн 25 | нет |
| Google: Gemini 2.5 Flash Preview 05 20 (c 16 июля отключена, перенаправляется в 2.5 Flash) [?](#mar366taskfull) google/gemini-2.5-flash-pre-05-20  дешевая и с большим контекстом tools structured-outputs | 0.018 | 0.07 | 1000000 | 20 мая 25 | нет |
| Google: Gemini 2.5 Flash Preview (c 16 июля отключена, перенаправляется в 2.5 Flash) [?](#mar339taskfull) google/gemini-2.5-flash-pre  дешевая и с большим контекстом structured-outputs | 0.018 | 0.07 | 1000000 | 18 апр 25 | нет |
| Google: Gemini 2.5 Pro Preview (03-25) [?](#mar320taskfull) google/gemini-2.5-pro-preview-03-25  Профессиональный tools structured-outputs | 0.18 | 1.90 | 1000000 | 6 мая 25 | нет |
| Gemma 3 27B (опенсорс) [?](#mar293taskfull) google/gemma-3-27b-it | 0.05 | 0.08 | 128000 | 13 мар 25 | нет |
| Gemini 1.5 Flash-8B (выключена, перенаправляется в Flash 2.5 Lite) [?](#mar207taskfull) google/gemini-flash-1.5-8b  дешевая и с большим контекстом tools | 0.015 | 0.04 | 1000000 | 7 окт 24 | нет |
| Gemma 2 27B (опенсорс) [?](#mar146taskfull) google/gemma-2-27b-it | 0.10 | 0.10 | 8192 | 17 июл 24 | нет |
| Google: Gemini Flash 1.5 (отключена, перенаправляется в Gemini 2.5 Flash Lite) [?](#mar117taskfull) google/gemini-flash-1.5  дешевая и с большим контекстом | 0.017 | 0.05 | 1000000 | 25 сен 24 | нет |

X

### Gemini 3.8 Flash (Thinking High)

Gemini 3.8 Flash — самая интеллектуальная Flash-модель от Google, демонстрирующая значительный прогресс по сравнению с 3.7 Flash в области разработки программного обеспечения, агентных задач и многошагового рассуждения.  
  
Уровень размышления High для продуманных ответов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.8 Flash (Thinking Minimal)

Gemini 3.8 Flash — самая интеллектуальная Flash-модель от Google, демонстрирующая значительный прогресс по сравнению с 3.7 Flash в области разработки программного обеспечения, агентных задач и многошагового рассуждения.  
  
Минимальный уровень размышления - рекомендуется для быстрого и дешевого получения основного ответа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 50р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.7 Flash (Thinking High)

Gemini 3.7 Flash — это мультимодальная модель от Google, созданная для быстрых агентных рабочих процессов, написания кода и сложных многоэтапных рассуждений. Она разработана для задач, требующих высокой скорости отклика и надёжного решения многошаговых проблем.  
  
Уровень размышления High для продуманных ответов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.7 Flash (Thinking Minimal)

Gemini 3.7 Flash — это мультимодальная модель от Google, созданная для быстрых агентных рабочих процессов, написания кода и сложных многоэтапных рассуждений. Она разработана для задач, требующих высокой скорости отклика и надёжного решения многошаговых проблем.  
  
Минимальный уровень размышления - рекомендуется для быстрого и дешевого получения основного ответа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 50р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.6 Flash (Thinking High)

Gemini 3.6 Flash — высокопроизводительная модель от Google, предназначенная для написания кода, автономных рабочих процессов, а также разработки веб-сайтов и приложений. Она создана для получения качественных результатов с минимальным количеством лишних правок и оговорок, а также для сокращения расхода токенов и числа обращений к модели, необходимых для выполнения задачи.  
  
Уровень размышления High для продуманных ответов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 200р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.6 Flash (Thinking Minimal)

Gemini 3.6 Flash — высокопроизводительная модель от Google, предназначенная для написания кода, автономных рабочих процессов, а также разработки веб-сайтов и приложений. Она создана для получения качественных результатов с минимальным количеством лишних правок и оговорок, а также для сокращения расхода токенов и числа обращений к модели, необходимых для выполнения задачи.  
  
Минимальный уровень размышления - рекомендуется для быстрого и дешевого получения основного ответа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 100р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.5 Flash Lite (Thinking High)

Gemini 3.5 Flash-Lite — высокопроизводительная модель от Google с расширенными агентными возможностями. Она идеально подходит для субагентов, выполняющих конкретные задачи в рамках сложных многоагентных рабочих процессов.  
  
Уровень размышления High для продуманных ответов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.5 Flash Lite (Thinking Minimal)

Gemini 3.5 Flash-Lite — высокопроизводительная модель от Google с расширенными агентными возможностями. Она идеально подходит для субагентов, выполняющих конкретные задачи в рамках сложных многоагентных рабочих процессов.  
  
Минимальный уровень размышления - рекомендуется для быстрого и дешевого получения основного ответа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.5 Flash (Thinking High)

Gemini 3.5 Flash — это высокоэффективная мультимодальная модель Google, обеспечивающая возможности кодирования и рассуждения, близкие к уровню Pro, при стоимости и скорости уровня Flash.  
  
Максимальный уровень размышления для максимально продуманных ответов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.5 Flash (Thinking Minimal)

Gemini 3.5 Flash — это высокоэффективная мультимодальная модель Google, обеспечивающая возможности кодирования и рассуждения, близкие к уровню Pro, при стоимости и скорости уровня Flash.  
  
Минимальный уровень размышления - рекомендуется для быстрого и дешевого получения основного ответа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.5 Flash (Thinking Medium)

Gemini 3.5 Flash — это высокоэффективная мультимодальная модель Google, обеспечивающая возможности кодирования и рассуждения, близкие к уровню Pro, при стоимости и скорости уровня Flash.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.1 Flash Lite (Thinking High)

Gemini 3.1 Flash Lite — это общедоступная высокоэффективная мультимодальная модель Google, оптимизированная для задач с низкой задержкой и высокой нагрузкой.  
  
Уровень размышления: высокий.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.1 Flash Lite (Thinking)

Gemini 3.1 Flash Lite — это общедоступная высокоэффективная мультимодальная модель Google, оптимизированная для задач с низкой задержкой и высокой нагрузкой.  
  
Уровень размышления: низкий, может и не использоваться в процессе принятия решения.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.1 Flash Lite

Gemini 3.1 Flash Lite — это общедоступная высокоэффективная мультимодальная модель Google, оптимизированная для задач с низкой задержкой и высокой нагрузкой.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemma 4 26B A4B (Thinking)

Gemma 4 26B A4B IT — это инструктивно-настроенная модель на основе архитектуры «Смесь экспертов» (MoE) от Google DeepMind. Несмотря на 25,2 млрд общих параметров, во время инференса на каждый токен активируется лишь 3,8 млрд из них — обеспечивая качество, сопоставимое с моделями на ~31 млрд параметров, при значительно меньших вычислительных затратах. Поддерживает мультимодальный ввод, включая текст и изображения.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemma 4 26B A4B

Gemma 4 26B A4B IT — это инструктивно-настроенная модель на основе архитектуры «Смесь экспертов» (MoE) от Google DeepMind. Несмотря на 25,2 млрд общих параметров, во время инференса на каждый токен активируется лишь 3,8 млрд из них — обеспечивая качество, сопоставимое с моделями на ~31 млрд параметров, при значительно меньших вычислительных затратах. Поддерживает мультимодальный ввод, включая текст и изображения.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemma 4 31B (Thinking)

Gemma 4 31B Instruct — это плотная мультимодальная модель Google DeepMind с 30,7 млрд параметров, поддерживающая текстовый и визуальный ввод с текстовым выводом. Модель обладает контекстным окном в 256 тысяч токенов, настраиваемым режимом мышления/рассуждения, встроенным вызовом функций и многоязычной поддержкой более 140 языков. Демонстрирует высокие результаты в задачах программирования, логического мышления и понимания документов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemma 4 31B

Gemma 4 31B Instruct — это плотная мультимодальная модель Google DeepMind с 30,7 млрд параметров, поддерживающая текстовый и визуальный ввод с текстовым выводом. Модель обладает контекстным окном в 256 тысяч токенов, настраиваемым режимом мышления/рассуждения, встроенным вызовом функций и многоязычной поддержкой более 140 языков. Демонстрирует высокие результаты в задачах программирования, логического мышления и понимания документов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.1 Flash Lite Preview (Thinking High)

Gemini 3.1 Flash Lite Preview — это высокоэффективная модель Google, оптимизированная для сценариев с большим объёмом задач. Она превосходит Gemini 2.5 Flash Lite по общему качеству и приближается к уровню производительности Gemini 2.5 Flash по ключевым возможностям. Улучшения охватывают обработку аудиовхода/ASR, ранжирование фрагментов RAG, перевод, извлечение данных и дополнение кода.  
  
Размышляющая версия; к сожалению, в ней временно не поддерживается стриминг.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemini 3.1 Flash Lite Preview

Gemini 3.1 Flash Lite Preview — это высокоэффективная модель Google, оптимизированная для сценариев с большим объёмом задач. Она превосходит Gemini 2.5 Flash Lite по общему качеству и приближается к уровню производительности Gemini 2.5 Flash по ключевым возможностям. Улучшения охватывают обработку аудиовхода/ASR, ранжирование фрагментов RAG, перевод, извлечение данных и дополнение кода.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3.1 Pro Preview (версия на 1М контекста)

Gemini 3.1 Pro — это апдейт передовой ИИ-модели Google Gemini 3 Pro. Улучшения в первую очередь касаются эффективности использования токенов и агентных вызовов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3.1 Pro Preview (версия на 200К контекста)

Gemini 3.1 Pro — это апдейт передовой ИИ-модели Google Gemini 3 Pro. Улучшения в первую очередь касаются эффективности использования токенов и агентных вызовов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3 Flash Preview (Thinking)

Gemini 3 Flash Preview — это высокоскоростная модель, разработанная для агентных рабочих процессов, многоходовых чатов и помощи в программировании. Она обеспечивает рассуждения и производительность использования инструментов почти на уровне Pro при существенно более низкой задержке, чем у более крупных вариантов Gemini, что делает её хорошо подходящей для интерактивной разработки, длительных циклов работы агентов и совместных задач по программированию. По сравнению с Gemini 2.5 Flash она обеспечивает широкие улучшения качества в области рассуждений, мультимодального понимания и надёжности.  
  
Размышляющая версия.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3 Flash Preview

Gemini 3 Flash Preview — это высокоскоростная модель, разработанная для агентных рабочих процессов, многоходовых чатов и помощи в программировании. Она обеспечивает рассуждения и производительность использования инструментов почти на уровне Pro при существенно более низкой задержке, чем у более крупных вариантов Gemini, что делает её хорошо подходящей для интерактивной разработки, длительных циклов работы агентов и совместных задач по программированию. По сравнению с Gemini 2.5 Flash она обеспечивает широкие улучшения качества в области рассуждений, мультимодального понимания и надёжности.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash Lite

Gemini 2.5 Flash-Lite — это облегченная модель рассуждений в семействе Gemini 2.5, оптимизированная для сверхнизкой задержки и экономической эффективности. Она обеспечивает улучшенную пропускную способность, более быструю генерацию токенов и лучшую производительность по сравнению с более ранними моделями Flash в рамках общих тестов.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash (Thinking)

Gemini 2.5 Flash — передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "размышления", позволяющие предоставлять ответы с большей точностью и нюансированной обработкой контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash

Gemini 2.5 Flash — передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "размышления", позволяющие предоставлять ответы с большей точностью и нюансированной обработкой контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Pro

Gemini 2.5 Pro — это передовая ИИ-модель Google, разработанная для решения сложных задач в области рассуждений, программирования, математики и науки. Она использует возможности "мышления", что позволяет ей формулировать ответы с повышенной точностью и учетом нюансов контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Pro Preview (обновлена 5 июня)

Gemini 2.5 Pro — это передовая ИИ-модель Google, разработанная для решения сложных задач в области рассуждений, программирования, математики и науки. Она использует возможности "мышления", что позволяет ей формулировать ответы с повышенной точностью и учетом нюансов контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash Preview 05 20 (c 16 июля отключена, перенаправляется в 2.5 Flash)

Gemini 2.5 Flash — это передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "мышления", позволяющие ей предоставлять ответы с большей точностью и учитывать нюансы контекста.  
  
Примечание: Эта модель доступна в двух вариантах: с мышлением и без мышления. Стоимость выходных данных значительно варьируется в зависимости от того, активна ли функция мышления.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash Preview (c 16 июля отключена, перенаправляется в 2.5 Flash)

Gemini 2.5 Flash — это передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "мышления", позволяющие ей предоставлять ответы с большей точностью и учитывать нюансы контекста.  
  
Примечание: Эта модель доступна в двух вариантах: с мышлением и без мышления. Стоимость выходных данных значительно варьируется в зависимости от того, активна ли функция мышления.  
  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Pro Preview (03-25)

Gemini 2.5 Pro — это передовая ИИ-модель Google, разработанная для решения сложных задач в области рассуждений, программирования, математики и науки. Она использует возможности "мышления", что позволяет ей формулировать ответы с повышенной точностью и учетом нюансов контекста.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemma 3 27B (опенсорс)

Gemma 3 27B - это новейшая модель Google с открытым исходным кодом, преемник Gemma 2. Она обрабатывает контекстные окна до 128 тысяч токенов, понимает более 140 языков и предлагает улучшенные возможности в математике, рассуждениях и чате, включая структурированные выходные данные и вызов функций.   
  
Модели Gemma хорошо подходят для различных задач генерации текста, включая ответы на вопросы, обобщение и рассуждение.  
  
Нормально работает на русском языке (рекомендуется температура пониже)

Закрыть

X

### Gemini 1.5 Flash-8B (выключена, перенаправляется в Flash 2.5 Lite)

Gemini 1.5 Flash-8B оптимизирован для скорости и эффективности, обеспечивая улучшенную производительность в небольших задачах с подсказками, таких как чат, транскрипция и перевод. Благодаря сниженной задержке он очень эффективен для операций в режиме реального времени и в больших масштабах. Эта модель ориентирована на экономически эффективные решения при сохранении высокого качества результатов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemma 2 27B (опенсорс)

Gemma 2 27B от Google - это открытая модель, созданная на основе тех же исследований и технологий, которые использовались для создания моделей Gemini.  
  
Модели Gemma хорошо подходят для различных задач генерации текста, включая ответы на вопросы, обобщение и рассуждение.  
  
Нормально работает на русском языке (рекомендуется температура пониже)

Закрыть

X

### Google: Gemini Flash 1.5 (отключена, перенаправляется в Gemini 2.5 Flash Lite)

Gemini 1.5 Flash — это базовая модель, которая хорошо справляется с различными мультимодальными задачами, такими как визуальное понимание, классификация, обобщение и создание контента из изображений, аудио и видео. Он умеет обрабатывать визуальные и текстовые данные, такие как фотографии, документы, инфографика и снимки экрана.  
  
Gemini 1.5 Flash предназначен для выполнения объемных и высокочастотных задач, где стоимость и задержка имеют значение. При выполнении большинства распространенных задач Flash обеспечивает качество, сравнимое с другими моделями Gemini Pro, при значительно меньших затратах. Flash хорошо подходит для таких приложений, как чат-помощники и создание контента по требованию, где скорость и масштаб имеют значение.

Закрыть

  

### xAI: Grok 2, 3, 4

  

**Модели Grok от компании Элона Maска xAI**.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Grok 4.6 от xAI [?](#mar725taskfull) x-ai/grok-4.6  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.6 | 1.8 | 500000 | 14 авг | нет |
| Grok 4.5 от xAI [?](#mar710taskfull) x-ai/grok-4.5  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.6 | 1.8 | 500000 | 16 июл | нет |
| Grok 4.3 от xAI (Thinking) [?](#mar671taskfull) x-ai/grok-4.3-thinking  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.37 | 0.74 | 2000000 | 17 мая | нет |
| Grok 4.3 от xAI [?](#mar670taskfull) x-ai/grok-4.3  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.37 | 0.74 | 2000000 | 17 мая | нет |
| Grok 4.20 Beta от xAI (Thinking) [?](#mar639taskfull) x-ai/grok-4.20-beta-thinking  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.60 | 1.80 | 2000000 | 25 мар | нет |
| Grok 4.20 Beta от xAI [?](#mar638taskfull) x-ai/grok-4.20-beta  Профессиональный (не Тестовый) повышенная цена при контексте > 200К tools structured-outputs   vision | 0.60 | 1.80 | 2000000 | 25 мар | нет |

X

### Grok 4.6 от xAI

Grok 4.6 — самая умная модель SpaceXAI с передовыми показателями в программировании, интеллектуальном труде и точных науках.  
**Повышенная цена при контексте > 200К**: x2.0 стоимость входа; x2.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 400р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Grok 4.5 от xAI

Grok 4.5 — самая умная модель SpaceXAI с передовыми возможностями в области программирования, интеллектуального труда и точных наук.  
**Повышенная цена при контексте > 200К**: x2.0 стоимость входа; x2.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 400р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Grok 4.3 от xAI (Thinking)

Grok 4.3 — это модель рассуждений от xAI. Она принимает текстовые и графические входные данные с текстовым выводом и подходит для агентных рабочих процессов, задач следования инструкциям и приложений, требующих высокой фактической точности.  
  
Размышляющая версия.  
**Повышенная цена при контексте > 200К**: x2.0 стоимость входа; x2.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Grok 4.3 от xAI

Grok 4.3 — это модель рассуждений от xAI. Она принимает текстовые и графические входные данные с текстовым выводом и подходит для агентных рабочих процессов, задач следования инструкциям и приложений, требующих высокой фактической точности.  
**Повышенная цена при контексте > 200К**: x2.0 стоимость входа; x2.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Grok 4.20 Beta от xAI (Thinking)

Grok 4.20 Beta — новейшая флагманская модель xAI с лидирующей в отрасли скоростью и возможностями агентного вызова инструментов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Повышенная цена при контексте > 200К**: x3.0 стоимость входа; x3.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Grok 4.20 Beta от xAI

Grok 4.20 Beta — новейшая флагманская модель xAI с лидирующей в отрасли скоростью и возможностями агентного вызова инструментов.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Повышенная цена при контексте > 200К**: x3.0 стоимость входа; x3.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

  
  

### MistralAI: опенсорс + закрытые Tiny, Small, Medium

  

Закрытые, предоставляемые по API нейросети от компании Mistral, известной своими опенсорс моделями. Mistral Medium по оценкам производителя в работе сравнима с Claude 2 и GPT 4. Также здесь присутствуют ссылки на её оригинальные опенсорс модели.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Mistral: Mistral Medium 3.1 [?](#mar451taskfull) mistralai/mistral-medium-3.1  tools structured-outputs | 0.06 | 0.30 | 260000 | 14 авг 25 | нет |
| Mistral: Mistral Small 3.2 24B [?](#mar403taskfull) mistralai/mistral-small-3.2-24b-instruct  tools structured-outputs | 0.015 | 0.045 | 128000 | 25 июн 25 | нет |
| Mistral Medium 3 [?](#mar355taskfull) mistralai/mistral-medium-3  tools structured-outputs | 0.06 | 0.30 | 131000 | 8 мая 25 | нет |
| Mistral: Mistral NeMo 12B [?](#mar160taskfull) mistralai/mistral-nemo  поддерживает русский общие вопросы tools | 0.05 | 0.05 | 128000 | 19 июл 24 | нет |
| Mistral: Mixtral 8x22B Instruct [?](#mar101taskfull) mistralai/mixtral-8x22b-instruct | 0.15 | 0.15 | 65536 | 18 апр 24 | нет |
| Mistral: Mistral Large 2 [?](#mar73taskfull) mistralai/mistral-large  Профессиональный | 0.45 | 1.35 | 128000 | 24 июл 24 | нет |

X

### Mistral: Mistral Medium 3.1

Mistral Medium 3.1 — это обновленная версия Mistral Medium 3, высокопроизводительной языковой модели корпоративного уровня, разработанной для обеспечения передовых возможностей при значительно сниженных операционных затратах. Она сочетает в себе современные возможности рассуждения и мультимодальную производительность с в 8 раз более низкой стоимостью по сравнению с традиционными крупными моделями, что делает её подходящей для масштабируемых развертываний в профессиональных и промышленных сценариях использования.  
  
Модель превосходно работает в таких областях, как программирование, STEM-рассуждения и корпоративная адаптация. Она поддерживает гибридные развертывания, развертывания на собственных серверах и в VPC, и оптимизирована для интеграции в пользовательские рабочие процессы. Mistral Medium 3.1 предлагает конкурентоспособную точность по сравнению с более крупными моделями, такими как Claude Sonnet 3.5/3.7, Llama 4 Maverick и Command R+, при этом сохраняя широкую совместимость в облачных средах.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Mistral: Mistral Small 3.2 24B

Mistral-Small-3.2-24B-Instruct-2506 - это обновленная модель с 24 миллиардами параметров от Mistral, оптимизированная для выполнения инструкций, снижения повторений и улучшения вызова функций. По сравнению с версией 3.1, версия 3.2 значительно повышает точность на WildBench и Arena Hard, сокращает бесконечные генерации и обеспечивает прирост в задачах использования инструментов и структурированного вывода.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Mistral Medium 3

Mistral Medium 3 — это высокопроизводительная языковая модель корпоративного уровня, разработанная для обеспечения передовых возможностей при значительно сниженных операционных затратах. Она сочетает современные возможности рассуждения и мультимодальную производительность с затратами в 8 раз ниже по сравнению с традиционными большими моделями, что делает её подходящей для масштабируемого внедрения в профессиональных и промышленных сценариях использования.  
  
Модель превосходит в таких областях, как программирование, STEM-рассуждения и адаптация для предприятий. Mistral Medium 3 предлагает конкурентоспособную точность по сравнению с более крупными моделями, такими как Claude Sonnet 3.5/3.7, Llama 4 Maverick и Command R+, сохраняя при этом широкую совместимость с различными облачными средами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Mistral: Mistral NeMo 12B

Mistral AI представила Mistral NeMo, 12-миллиардную модель, разработанную в сотрудничестве с NVIDIA. Mistral NeMo предлагает большой контекст до 128 тысяч токенов.  
  
Модель тренировалась на многоязычных данных, и, что довольно приятно, графики включают в себя оценки эффективности на русском языке.  
  
Наша новость на Хабре: https://habr.com/ru/news/829822/  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Mistral: Mixtral 8x22B Instruct

Официальный Instruct-файнтюн Mistral для версии Mixtral 8x22B. Он использует 39 миллиардов активных параметров из 141 миллиарда, обеспечивая беспрецедентную экономическую эффективность для своего размера.

Закрыть

X

### Mistral: Mistral Large 2

Это флагманская модель Mistral AI, Mistral Large 2 (версия mistral-large-2407). Она основана на прототипе с закрытым исходным кодом и превосходно справляется с рассуждениями, кодом, JSON, чатом и многим другим.

Закрыть

  

### Cohere: с фокусом на RAG, function calling, tools

  

Модели от Cohere с фокусом на RAG, function calling, tools.   
Доступны в виде OpenSource версий, но у нас предоставляются через API с модерацией.   
*Используя данные модели, вы соглашаетесь с [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)ToS Cohere](https://docs.cohere.com/docs/c4ai-acceptable-use-policy "Внешняя ссылка (откроется в новом окне)")*

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Cohere: Command R+ (август 2024) [?](#mar190taskfull) cohere/command-r-plus-08-2024  Профессиональный общие вопросы и ролеплей | 0.38 | 1.5 | 128000 | 31 авг 24 | нет |
| Cohere: Command R (август 2024) [?](#mar189taskfull) cohere/command-r-08-2024  общие вопросы и ролеплей | 0.025 | 0.09 | 128000 | 31 авг 24 | нет |
| Cohere: Command R7B (12-2024) [?](#mar236taskfull) cohere/command-r7b-12-2024  За вызов: 0.005 р. | 0.01 | 0.025 | 128000 | 16 дек 24 | нет |

X

### Cohere: Command R+ (август 2024)

command-r-plus-08-2024 - это обновление Command R+ с примерно на 50% более высокой пропускной способностью и на 25% меньшей задержкой по сравнению с предыдущей версией Command R+

Закрыть

X

### Cohere: Command R (август 2024)

command-r-08-2024 - это обновление Command R с улучшенной производительностью для многоязычной генерации с дополнением извлечения (RAG) и использования инструментов. В более широком смысле, она лучше справляется с математикой, кодом и рассуждениями и конкурентоспособна с предыдущей версией более крупной модели Command R+.

Закрыть

X

### Cohere: Command R7B (12-2024)

Command R7B (12-2024) - это небольшое, быстрое обновление модели Command R+, выпущенное в декабре 2024 года. Она отлично справляется с RAG, использованием инструментов, агентами и подобными задачами, требующими сложных рассуждений и множества этапов.

Закрыть

  

### Amazon: Nova и пр.

  

Серия языковых моделей от Amazon (начиная с декабря 2024).  
   
Модели отличаются большим контекстом (до 300 000 токенов)

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Amazon: Nova Pro 1.0 [?](#mar225taskfull) amazon/nova-pro-v1  Профессиональный | 0.15 | 0.50 | 300000 | 6 дек 24 | да |
| Amazon: Nova Lite 1.0 [?](#mar224taskfull) amazon/nova-lite-v1  tools | 0.02 | 0.04 | 300000 | 6 дек 24 | да |
| Amazon: Nova Micro 1.0 [?](#mar223taskfull) amazon/nova-micro-v1  tools | 0.012 | 0.03 | 128000 | 6 дек 24 | да |

X

### Amazon: Nova Pro 1.0

Amazon Nova Pro 1.0 - это многофункциональная мультимодальная модель от Amazon, ориентированная на обеспечение сочетания точности, скорости и экономичности для широкого спектра задач. По состоянию на декабрь 2024 года она достигает передовых результатов в ключевых тестах, включая визуальные вопросы и ответы (TextVQA) и понимание видео (VATEX).  
  
Amazon Nova Pro демонстрирует высокие способности в обработке как визуальной, так и текстовой информации, а также в анализе финансовых документов.

Закрыть

X

### Amazon: Nova Lite 1.0

Amazon Nova Lite 1.0 - это очень бюджетная мультимодальная модель от Amazon.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Amazon: Nova Micro 1.0

Amazon Nova Micro 1.0 - это текстовая модель, обеспечивающая самую низкую задержку ответов среди семейства моделей Amazon Nova при очень низкой стоимости. С контекстной длиной в 128 тысяч токенов и оптимизацией для скорости и экономичности, Amazon Nova Micro отлично справляется с такими задачами, как суммаризация текста, перевод, классификация контента, интерактивный чат и мозговой штурм. Она обладает базовыми способностями к математическим вычислениям и программированию.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

  
  

## Текстовые модели (восточные, Китай)

### DeepSeek: V3, R1, 3.2 и пр.

  

**Нашумевшие нейросети от DeepSeek**. Достаточно **дешевые**.  
Они крайне дешевые в своем классе – но только при использовании самого провайдера DeepSeek, который логирует запросы (и в конце января DeepSeek не смог переварить интерес к своим моделям и лег)  
Поэтому мы также поддерживаем альтернативных провайдеров для DeepSeek (постфикс alt) – они дороже, но не декларируют логирование данных и в целом часто устойчивее.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || DeepSeek V4 Flash Vision Exp (от сторонних провайдеров) [?](#mar734taskfull) deepseek/deepseek-v4-flash-vision-exp  Базовый и выше (не Тестовый) провайдер логирует данные общие вопросы и программирование tools   vision | 0.066 | 0.20 | 1000000 | 21 авг | нет |
| DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, размышляющая, FAST - до 200 ток/сек) [?](#mar729taskfull) deepseek/deepseek-v4-flash-0731-alt-thinking-fast  общие вопросы и программирование tools structured-outputs | 0.08 | 0.16 | 1000000 | 18 авг | нет |
| DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, FAST - около 200 ток/сек) [?](#mar728taskfull) deepseek/deepseek-v4-flash-0731-alt-fast  общие вопросы и программирование tools structured-outputs | 0.08 | 0.16 | 1000000 | 18 авг | нет |
| DeepSeek V4 Pro 0813 1.6T (Альтернативные провайдеры, Thinking) [?](#mar727taskfull) deepseek/deepseek-v4-pro-0813-alt-thinking  Профессиональный (не Тестовый) общие вопросы и программирование tools structured-outputs | 0.40 | 1.20 | 1000000 | 14 авг | нет |
| DeepSeek V4 Pro 0813 1.6T (Альтернативные провайдеры) [?](#mar726taskfull) deepseek/deepseek-v4-pro-0813-alt  Профессиональный (не Тестовый) общие вопросы и программирование tools structured-outputs | 0.40 | 1.20 | 1000000 | 14 авг | нет |
| DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, размышляющая) [?](#mar719taskfull) deepseek/deepseek-v4-flash-0731-alt-thinking  общие вопросы и программирование tools structured-outputs | 0.04 | 0.08 | 1000000 | 8 авг | нет |
| DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры) [?](#mar718taskfull) deepseek/deepseek-v4-flash-0731-alt  общие вопросы и программирование tools structured-outputs | 0.04 | 0.08 | 1000000 | 8 авг | нет |
| DeepSeek V4 Pro 1.6T (Альтернативные провайдеры, размышляющая) [?](#mar688taskfull) deepseek/deepseek-v4-pro-alt-thinking  Профессиональный (не Тестовый) общие вопросы и программирование tools structured-outputs | 0.50 | 1.00 | 1000000 | 12 июн | нет |
| DeepSeek V4 Pro 1.6T (Альтернативные провайдеры) [?](#mar687taskfull) deepseek/deepseek-v4-pro-alt  Профессиональный (не Тестовый) общие вопросы и программирование tools structured-outputs | 0.50 | 1.00 | 1000000 | 12 июн | нет |
| DeepSeek V4 Flash 284B (Альтернативные провайдеры, Thinking) [?](#mar666taskfull) deepseek/deepseek-v4-flash-alt-thinking  общие вопросы и программирование tools structured-outputs | 0.04 | 0.08 | 1000000 | 27 апр | нет |
| DeepSeek V4 Flash 284B (Альтернативные провайдеры) [?](#mar665taskfull) deepseek/deepseek-v4-flash-alt  общие вопросы и программирование tools structured-outputs | 0.04 | 0.08 | 1000000 | 27 апр | нет |
| DeepSeek V4 Pro 0813 1.6T (официальный, Thinking) [?](#mar664taskfull) deepseek/deepseek-v4-pro-thinking  Профессиональный (не Тестовый) провайдер логирует данные очень дешевая общие вопросы и программирование tools | 0.20 | 0.60 | 1000000 | 13 авг | нет |
| DeepSeek V4 Pro 0813 1.6T (официальный) [?](#mar663taskfull) deepseek/deepseek-v4-pro  Профессиональный (не Тестовый) провайдер логирует данные очень дешевая общие вопросы и программирование tools | 0.20 | 0.60 | 1000000 | 13 авг | нет |
| DeepSeek V4.1 Flash 0731 284B (Thinking, официальный) [?](#mar662taskfull) deepseek/deepseek-v4-flash-thinking  провайдер логирует данные общие вопросы и программирование tools | 0.05 | 0.20 | 1000000 | 10 сен | нет |
| DeepSeek V4.1 Flash (обновлена 10 сентября 2026, официальный) [?](#mar661taskfull) deepseek/deepseek-v4-flash  провайдер логирует данные общие вопросы и программирование tools | 0.05 | 0.20 | 1000000 | 10 сен | нет |
| DeepSeek V3.1 671B (альт провайдер, быстрая версия) [?](#mar582taskfull) deepseek/deepseek-chat-3.1-alt-fast  быстрая общие вопросы и программирование tools structured-outputs | 0.08 | 0.25 | 162000 | 27 янв | нет |
| DeepSeek V3.2 671B (альт провайдер, быстрее) [?](#mar566taskfull) deepseek/deepseek-v3.2-alt-faster  общие вопросы и программирование tools structured-outputs | 0.09 | 0.25 | 162000 | 16 дек 25 | нет |
| DeepSeek V3.2 671B (альт провайдер, Thinking) [?](#mar555taskfull) deepseek/deepseek-v3.2-alt-thinking  общие вопросы и программирование tools | 0.045 | 0.07 | 162000 | 2 дек 25 | нет |
| DeepSeek V3.2 671B (альт провайдер) [?](#mar554taskfull) deepseek/deepseek-v3.2-alt  общие вопросы и программирование tools | 0.045 | 0.07 | 162000 | 2 дек 25 | нет |
| DeepSeek V3.2 Exp 671B Thinking (альт провайдер) [?](#mar495taskfull) deepseek/deepseek-v3.2-exp-alt-thinking  общие вопросы и программирование tools | 0.045 | 0.07 | 162000 | 2 окт 25 | нет |
| DeepSeek V3.2 Exp 671B (альт провайдер) [?](#mar494taskfull) deepseek/deepseek-v3.2-exp-alt  общие вопросы и программирование tools | 0.045 | 0.07 | 162000 | 2 окт 25 | нет |
| DeepSeek V3.1 Terminus 671B (альт провайдер, Thinking) [?](#mar480taskfull) deepseek/deepseek-chat-3.1-terminus-alt-thinking  общие вопросы и программирование tools structured-outputs | 0.07 | 0.22 | 162000 | 25 сен 25 | нет |
| DeepSeek V3.1 Terminus 671B (альт провайдер) [?](#mar479taskfull) deepseek/deepseek-chat-3.1-terminus-alt  общие вопросы и программирование tools structured-outputs | 0.07 | 0.22 | 162000 | 25 сен 25 | нет |
| DeepSeek R1 (05-28, конкурент o1, для размышлений, альтернативный провайдер) [?](#mar385taskfull) deepseek/deepseek-r1-alt-0528  Профессиональный общие вопросы | 0.075 | 0.30 | 128000 | 29 мая 25 | нет |
| DeepSeek V3 0324 600B (альтернативные провайдеры) [?](#mar309taskfull) deepseek/deepseek-chat-0324-alt  общие вопросы и программирование | 0.16 | 0.16 | 128000 | 25 мар 25 | нет |
| DeepSeek R1 дистиллят на базе LLama 3.3 70B (для размышлений) [?](#mar261taskfull) deepseek/deepseek-r1-distill-llama-70b  Профессиональный общие вопросы | 0.12 | 0.12 | 128000 | 28 янв 25 | нет |
| DeepSeek R1 (конкурент o1, для размышлений, не рекомендуется для обычного пользования) [?](#mar251taskfull) deepseek/deepseek-r1  Профессиональный провайдер логирует данные общие вопросы | 0.20 | 0.80 | 65536 | 20 янв 25 | нет |
| DeepSeek V3 600B (альтернативные провайдеры) [?](#mar248taskfull) deepseek/deepseek-chat-alt  устарела, переходите на deepseek/deepseek-chat-0324-alt общие вопросы и программирование | 0.16 | 0.16 | 128000 | 14 янв 25 | нет |
| DeepSeek V4.1 Flash (обновлена 10 сентября 2026, официальный) [?](#mar135taskfull) deepseek/deepseek-chat  провайдер логирует данные общие вопросы tools | 0.05 | 0.15 | 1000000 | 10 сен | нет |
| DeepSeek-Coder-V2 236B MoE (v2.5) (теперь универсальная модель, перенаправляется в DeepSeek Chat) [?](#mar134taskfull) deepseek/deepseek-coder  топ программирование провайдер логирует данные | 0.04 | 0.05 | 128000 | 11 сен 24 | нет |

X

### DeepSeek V4 Flash Vision Exp (от сторонних провайдеров)

DeepSeek V4 Flash Vision Exp — это экспериментальная версия модели DeepSeek V4 Flash 0731 от DeepSeek с поддержкой зрения. Она добавляет возможность понимания изображений, сохраняя при этом все текстовые возможности базовой модели: работу с агентами, логическое мышление и обширные знания об окружающем мире. Модель построена на разреженной архитектуре смеси экспертов с 13 миллиардами активных параметров из 284 миллиардов общих.  
  
Модель оптимально подходит для анализа документов и графиков, ответов на вопросы по изображениям, а также для мультимодальных агентных сценариев, в которых текст и изображения чередуются между собой.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, размышляющая, FAST - до 200 ток/сек)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  
Версия от 0731 от 31 июля.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, FAST - около 200 ток/сек)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  
Версия от 0731 от 31 июля.  
Альтернативные провайдеры, быстрая версия - до 200 токенов в секунду.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 0813 1.6T (Альтернативные провайдеры, Thinking)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Версия от 8 августа 2026.   
Альтернативные провайдеры - декларируют, что не логируют данные.  
Размышляющая версия.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 0813 1.6T (Альтернативные провайдеры)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Версия от 8 августа 2026.  
Альтернативные провайдеры - декларируют, что не логируют данные.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры, размышляющая)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  
Версия от 0731 от 31 июля.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 0731 284B (Альтернативные провайдеры)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  
Версия от 0731 от 31 июля.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 1.6T (Альтернативные провайдеры, размышляющая)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Альтернативные провайдеры - декларируют, что не логируют данные.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 1.6T (Альтернативные провайдеры)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Альтернативные провайдеры - декларируют, что не логируют данные.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 284B (Альтернативные провайдеры, Thinking)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Flash 284B (Альтернативные провайдеры)

DeepSeek V4 Flash — это оптимизированная по эффективности модель класса Mixture-of-Experts от DeepSeek с общим количеством параметров 284 млрд и 13 млрд активируемых параметров, поддерживающая контекстное окно размером 1 млн токенов. Модель разработана для быстрого инференса и высокопроизводительных рабочих нагрузок при сохранении высокого уровня производительности в задачах рассуждения и написания кода.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 0813 1.6T (официальный, Thinking)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Версия от 13 августа 2026  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4 Pro 0813 1.6T (официальный)

DeepSeek V4 Pro — это крупномасштабная модель на основе архитектуры Mixture-of-Experts от DeepSeek с 1,6 триллиона общих параметров и 49 миллиардами активируемых параметров, поддерживающая контекстное окно в 1 миллион токенов. Она разработана для сложных задач рассуждения, программирования и долгосрочных агентных рабочих процессов, демонстрируя высокую производительность в тестах по базовым знаниям, математике и разработке программного обеспечения.  
  
Версия от 13 августа 2026  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4.1 Flash 0731 284B (Thinking, официальный)

DeepSeek V4.1 Flash — это разреженная модель на основе архитектуры mixture-of-experts от DeepSeek, представляющая экономичный уровень линейки V4.1. По данным DeepSeek, она превосходит V4 Pro по производительности, скорости и времени выполнения задач, поэтому занимает место выше предыдущего флагмана, а не ниже него.  
  
Модель оптимально подходит для задач программирования, логического мышления и агентных рабочих процессов, а также особенно эффективна при выполнении долгосрочных задач, требующих многошагового завершения.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V4.1 Flash (обновлена 10 сентября 2026, официальный)

DeepSeek V4.1 Flash — это разреженная модель на основе архитектуры mixture-of-experts от DeepSeek, представляющая экономичный уровень линейки V4.1. По данным DeepSeek, она превосходит V4 Pro по производительности, скорости и времени выполнения задач, поэтому занимает место выше предыдущего флагмана, а не ниже него.  
  
Модель оптимально подходит для задач программирования, логического мышления и агентных рабочих процессов, а также особенно эффективна при выполнении долгосрочных задач, требующих многошагового завершения.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.1 671B (альт провайдер, быстрая версия)

DeepSeek-V3.1 — это большая гибридная модель для рассуждений (671 млрд параметров, 37 млрд активных), которая поддерживает как режимы с размышлениями, так и без них через шаблоны промптов. Она расширяет базовую модель DeepSeek-V3 двухфазным процессом обучения для работы с длинным контекстом, достигая до 128 тыс. токенов.  
  
Модель улучшает использование инструментов, генерацию кода и эффективность рассуждений, достигая производительности, сопоставимой с DeepSeek-R1 на сложных бенчмарках, при этом отвечая быстрее. Она поддерживает структурированный вызов инструментов, код-агентов и поисковых агентов, что делает её подходящей для исследований, программирования и агентных рабочих процессов.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.2 671B (альт провайдер, быстрее)

DeepSeek-V3.2 — это обновление DeepSeek V3.1 на новой архитектуре с пониженной стоимостью и почти таким же качеством.   
  
Отличия от обычной версии:  
- Более быстрый провайдер.  
- Дороже  
- Поддержка structured outputs  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.2 671B (альт провайдер, Thinking)

DeepSeek-V3.2 — это обновление DeepSeek V3.1 на новой архитектуре с пониженной стоимостью и почти таким же качеством.   
Размышляющая версия.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.2 671B (альт провайдер)

DeepSeek-V3.2 — это обновление DeepSeek V3.1 на новой архитектуре с пониженной стоимостью и почти таким же качеством.   
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.2 Exp 671B Thinking (альт провайдер)

DeepSeek-V3.2 Exp — это обновление DeepSeek V3.1 на новой архитектуре с пониженной стоимостью и почти таким же качеством.  
  
Размышляющая версия.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.2 Exp 671B (альт провайдер)

DeepSeek-V3.2 Exp — это обновление DeepSeek V3.1 на новой архитектуре с пониженной стоимостью и почти таким же качеством.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.1 Terminus 671B (альт провайдер, Thinking)

DeepSeek-V3.1 Terminus — это обновление DeepSeek V3.1, которое сохраняет исходные возможности модели, одновременно устраняя проблемы, о которых сообщали пользователи, включая согласованность языка и возможности агента, что дополнительно оптимизирует производительность модели в кодировании и поисковых агентах. Это большая гибридная модель рассуждений (671 млрд параметров, 37 млрд активных), поддерживающая режимы мышления и без мышления. Она расширяет базовую модель DeepSeek-V3 с помощью двухфазного процесса обучения с длинным контекстом, достигая до 128 тысяч токенов, и использует микромасштабирование FP8 для эффективного вывода.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek V3.1 Terminus 671B (альт провайдер)

DeepSeek-V3.1 Terminus — это обновление DeepSeek V3.1, которое сохраняет исходные возможности модели, одновременно устраняя проблемы, о которых сообщали пользователи, включая согласованность языка и возможности агента, что дополнительно оптимизирует производительность модели в кодировании и поисковых агентах. Это большая гибридная модель рассуждений (671 млрд параметров, 37 млрд активных), поддерживающая режимы мышления и без мышления. Она расширяет базовую модель DeepSeek-V3 с помощью двухфазного процесса обучения с длинным контекстом, достигая до 128 тысяч токенов, и использует микромасштабирование FP8 для эффективного вывода.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek R1 (05-28, конкурент o1, для размышлений, альтернативный провайдер)

DeepSeek-R1 - это новейшая модель от команды DeepSeek, нацеленная на размышления с рассуждениями. Апдейт от 28 мая - цена ниже, качество выше.  
  
  
**Максимальный размер выходной генерации для модели: 163000 токенов**

Закрыть

X

### DeepSeek V3 0324 600B (альтернативные провайдеры)

Дотренированная версия DeepSeek V3 от 24 марта 2025 - несколько лучшие результаты по всем метрикам.  
  
Версия от альтернативных провайдеров.   
  
**Максимальный размер выходной генерации для модели: 2000 токенов**

Закрыть

X

### DeepSeek R1 дистиллят на базе LLama 3.3 70B (для размышлений)

DeepSeek R1 Distill Llama 70B - это дистиллированная большая языковая модель, основанная на Llama-3.3-70B-Instruct, использующая выходные данные DeepSeek R1.   
  
При использовании рекомендуется добавлять в системный промт фразу "Think step by step"  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### DeepSeek R1 (конкурент o1, для размышлений, не рекомендуется для обычного пользования)

DeepSeek-R1 - это новейшая модель от команды DeepSeek, нацеленная на размышления с рассуждениями.  
  
ОСОБЕННОСТИ БИЛЛИНГА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация.  
Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

Закрыть

X

### DeepSeek V3 600B (альтернативные провайдеры)

Версия от альтернативных провайдеров.   
  
**Максимальный размер выходной генерации для модели: 2000 токенов**

Закрыть

X

### DeepSeek V4.1 Flash (обновлена 10 сентября 2026, официальный)

DeepSeek V4.1 Flash — это новая модель от DeepSeek, значительно превосходящая версию V4 Flash и даже V4 Pro по внутренним оценкам производителя.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### DeepSeek-Coder-V2 236B MoE (v2.5) (теперь универсальная модель, перенаправляется в DeepSeek Chat)

Мы представляем DeepSeek-Coder-V2, открытую языковую модель Mixture-of-Experts (MoE), которая достигает результатов, сопоставимых с GPT4-Turbo в задачах, связанных с кодом. Модель была дообучена на 6 триллионах токенов и улучшила свои способности в программировании и математическом рассуждении, сохраняя при этом производительность в общих языковых задачах. DeepSeek-Coder-V2 поддерживает 338 языков программирования и 32К контекст.  
  
Всего параметров: 236B, активных: 21B  
  
Хостинг осуществляется разработчиком DeepSeek, который отмечает, что ваши данные могут быть залогированы и использованы для тренировки.

Закрыть

  
  

### Qwen – опенсорс модели от Tongyi Qianwen (Alibaba)

  

Серия языковых моделей от Tongyi Qianwen (Alibaba group, Китай).  
Старшие модели показывают неплохое знание русского языка – но рекомендуется ставить температуру пониже (около 0.2) и явно прописывать «отвечать на русском языке».  
   
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)Блог-запись о запуске моделей](https://qwenlm.github.io/blog/qwen1.5/ "Внешняя ссылка (откроется в новом окне)")  
   
Используя эти модели, вы соглашаетесь с [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)Tongyi Qianwen LICENSE AGREEMENT](https://huggingface.co/Qwen/Qwen1.5-110B-Chat/blob/main/LICENSE "Внешняя ссылка (откроется в новом окне)")  
Для модели 110B также доступна translate-версия.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Qwen: Qwen3.8 27B (Thinking High, быстрая) [?](#mar733taskfull) qwen/qwen3.8-27b-thinking-high  Базовый и выше (не Тестовый) tools   vision | 0.12 | 0.90 | 1000000 | 20 авг | нет |
| Qwen: Qwen3.8 27B (Non-thinking, быстрая) [?](#mar732taskfull) qwen/qwen3.8-27b  Базовый и выше (не Тестовый) tools   vision | 0.12 | 0.90 | 1000000 | 20 авг | нет |
| Qwen: Qwen3.8 Max (0902) [?](#mar722taskfull) qwen/qwen3.8-max  Профессиональный (не Тестовый) tools | 0.6 | 1.8 | 1000000 | 5 сен | нет |
| Qwen: Qwen3.7 Max [?](#mar684taskfull) qwen/qwen3.7-max  Профессиональный (не Тестовый) tools | 0.75 | 2.25 | 1000000 | 10 июн | нет |
| Qwen: Qwen3.7 Plus [?](#mar683taskfull) qwen/qwen3.7-plus  Базовый и выше (не Тестовый) повышенная цена при контексте > 250К tools   vision | 0.12 | 0.48 | 1000000 | 10 июн | нет |
| Qwen: Qwen3 VL 235B A22B Instruct [?](#mar674taskfull) qwen/qwen3-vl-235b-a22b-instruct  Профессиональный (не Тестовый) tools structured-outputs   vision | 0.075 | 0.57 | 256000 | 24 сен 25 | нет |
| Qwen: Qwen3.6 35B A3B (Thinking) [?](#mar673taskfull) qwen/qwen3.6-35b-a3b-thinking  Базовый и выше (не Тестовый) tools structured-outputs   vision | 0.045 | 0.30 | 256000 | 20 мая | нет |
| Qwen: Qwen3.6 35B A3B (Non-thinking) [?](#mar672taskfull) qwen/qwen3.6-35b-a3b  tools structured-outputs   vision | 0.045 | 0.30 | 256000 | 20 мая | нет |
| Qwen: Qwen3.5 397B A17B (Non-thinking) [?](#mar606taskfull) qwen/qwen3.5-397b-a17b  программирование tools | 0.09 | 0.54 | 256000 | 20 фев | нет |
| Qwen: Qwen3.5 Plus (от 2026-02-15, версия на 1M контекста) [?](#mar603taskfull) qwen/qwen3.5-plus-2026-02-15-1m  Базовый и выше (не Тестовый) программирование tools | 0.18 | 1.00 | 1000000 | 20 фев | нет |
| Qwen: Qwen3.5 Plus (от 2026-02-15) [?](#mar602taskfull) qwen/qwen3.5-plus-2026-02-15  программирование tools | 0.06 | 0.36 | 256000 | 20 фев | нет |
| Qwen: Qwen3.5 397B A17B [?](#mar601taskfull) qwen/qwen3.5-397b-a17b-thinking  программирование tools | 0.09 | 0.54 | 256000 | 20 фев | нет |
| Qwen: Qwen3 Coder Next [?](#mar599taskfull) qwen/qwen3-coder-next  программирование tools structured-outputs | 0.022 | 0.12 | 256000 | 20 фев | нет |
| Qwen: Qwen3 Max [?](#mar484taskfull) qwen/qwen3-max  tools | 0.18 | 0.95 | 128000 | 25 сен 25 | нет |
| Qwen: Qwen3 Coder Flash [?](#mar483taskfull) qwen/qwen3-coder-flash  программирование tools | 0.045 | 0.22 | 32000 | 25 сен 25 | нет |
| Qwen: Qwen3 Next 80B A3B [?](#mar477taskfull) qwen/qwen3-next-80b-a3b  tools structured-outputs | 0.022 | 0.22 | 262000 | 18 сен 25 | нет |
| Qwen: Qwen3 30B A3B Instruct 2507 [?](#mar440taskfull) qwen/qwen3-30b-a3b-instruct-2507 | 0.03 | 0.12 | 128000 | 31 июл 25 | нет |
| Qwen: Qwen3 235B A22B Thinking 2507 [?](#mar436taskfull) qwen/qwen3-235b-a22b-07-25-thinking  Профессиональный tools | 0.045 | 0.45 | 128000 | 25 июл 25 | нет |
| Qwen3 Coder 480B A35B (с поддержкой tools) [?](#mar435taskfull) qwen/qwen3-coder-tools  программирование и общие задачи tools | 0.30 | 0.47 | 256000 | 23 июл 25 | нет |
| Qwen3 Coder 480B A35B [?](#mar434taskfull) qwen/qwen3-coder  программирование и общие задачи | 0.30 | 0.30 | 256000 | 23 июл 25 | нет |
| Qwen: Qwen3 235B A22B 2507 [?](#mar431taskfull) qwen/qwen3-235b-a22b-07-25  Профессиональный | 0.035 | 0.12 | 256000 | 22 июл 25 | нет |
| Qwen: Qwen3 30B A3B [?](#mar349taskfull) qwen/qwen3-30b  опциональные размышления | 0.015 | 0.055 | 41000 | 29 апр 25 | нет |
| Qwen: Qwen3 14B [?](#mar348taskfull) qwen/qwen3-14b  За вызов: 0.003 р. опциональные размышления | 0.012 | 0.033 | 41000 | 29 апр 25 | нет |
| Qwen: Qwen3 32B [?](#mar347taskfull) qwen/qwen3-32b  опциональные размышления | 0.015 | 0.055 | 41000 | 29 апр 25 | нет |
| Qwen: Qwen3 235B A22B [?](#mar346taskfull) qwen/qwen3-235b  Профессиональный опциональные размышления | 0.035 | 0.12 | 41000 | 29 апр 25 | нет |
| Qwen2.5 72B Instruct (с поддержкой structured outputs) [?](#mar240taskfull) qwen/qwen-2.5-72b-structured  Профессиональный structured-outputs | 0.22 | 0.22 | 32000 | 19 дек 24 | нет |
| Qwen2.5 Coder 32B Instruct [?](#mar219taskfull) qwen/qwen-2.5-coder-32b-instruct  недорогая для программирования программирование и общие вопросы | 0.05 | 0.05 | 128000 | 12 ноя 24 | нет |
| Qwen2.5 72B Instruct [?](#mar194taskfull) qwen/qwen-2.5-72b-instruct  ролеплей и общие вопросы | 0.60 | 0.60 | 128000 | 21 сен 24 | нет |
| Qwen: Qwen-Plus [?](#mar269taskfull) qwen/qwen-plus  tools | 0.06 | 0.18 | 128000 | 1 фев 25 | нет |

X

### Qwen: Qwen3.8 27B (Thinking High, быстрая)

Qwen3.8 27B — это открытая полновесная мультимодальная языковая модель от Qwen. Она подходит для написания кода, профессиональных рабочих процессов, исследований, мультимодального взаимодействия, а также для длительных задач с использованием агентов.  
  
Версия с размышлениями уровня High.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.8 27B (Non-thinking, быстрая)

Qwen3.8 27B — это открытая полновесная мультимодальная языковая модель от Qwen. Она подходит для написания кода, профессиональных рабочих процессов, исследований, мультимодального взаимодействия, а также для длительных задач с использованием агентов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.8 Max (0902)

Qwen3.8 Max — это флагманская модель в серии Qwen3.8 от Alibaba, пришедшая на смену предварительной версии Qwen3.8 Max Preview и ставшая полноценным общедоступным релизом. Это мультимодальная модель с поддержкой сложных рассуждений, визуального понимания, программирования и автономных рабочих процессов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 300р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.7 Max

Qwen3.7-Max — флагманская модель в линейке Qwen3.7 от Alibaba. Она работает с текстовыми данными на входе и выходе и ориентирована прежде всего на агентные сценарии использования, демонстрируя особую эффективность в задачах программирования, офисной работы и повышения продуктивности, а также в долгосрочном автономном выполнении задач. По сравнению с предыдущими поколениями Qwen модель показывает заметно лучшие результаты в области кодирования и агентных возможностей.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.7 Plus

Qwen3.7-Plus — это экономичная модель из серии Qwen3.7 компании Alibaba. Она поддерживает ввод текста и изображений с выводом в текстовом формате. Модель развивает текстовые возможности всей серии, получив комплексное улучшение в области работы с визуальным контентом и естественным языком, при этом сохраняя полноценный интеллект агентного уровня для задач программирования, работы с инструментами и повышения продуктивности. Её отличительная черта — мультимодальные возможности гибридного интерактивного агента: модель способна воспринимать сцены реального мира, читать содержимое экрана и взаимодействовать с графическими интерфейсами, генерировать код на основе визуальных примеров, а также выполнять сквозную навигацию внутри мобильных приложений.  
**Повышенная цена при контексте > 250К**: x3.0 стоимость входа; x3.0 стоимость выхода  
(т.е. если ваши входные данные будут превышать указанный размер, стоимость будет повышена в указанное число раз)

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 VL 235B A22B Instruct

Qwen3-VL-235B-A22B Instruct — это мультимодальная модель с открытыми весами, объединяющая мощную генерацию текста с визуальным пониманием изображений и видео. Модель Instruct ориентирована на общее применение в области зрения и языка (VQA, разбор документов, извлечение данных из графиков и таблиц, многоязычное OCR). Серия делает акцент на устойчивом восприятии (распознавание разнообразных реальных и синтетических категорий), пространственном понимании (2D/3D-заземление) и долгосрочном визуальном осмыслении, демонстрируя конкурентоспособные результаты на публичных мультимодальных бенчмарках как по восприятию, так и по рассуждению.  
  
Помимо анализа, Qwen3-VL поддерживает агентное взаимодействие и использование инструментов: модель способна следовать сложным инструкциям в многоизображенческих многоходовых диалогах; привязывать текст к временной шкале видео для точных темпоральных запросов; а также управлять элементами графического интерфейса для решения задач автоматизации. Модели также обеспечивают визуальные рабочие процессы программирования — преобразование набросков или макетов в код и помощь в отладке интерфейсов — сохраняя при этом высокую производительность в режиме работы только с текстом, сопоставимую с флагманскими языковыми моделями Qwen3. Это делает Qwen3-VL пригодным для производственных сценариев, охватывающих документальный ИИ, многоязычное OCR, помощь в разработке программного обеспечения и интерфейсов, пространственные и воплощённые задачи, а также исследования в области агентов на основе зрения и языка.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.6 35B A3B (Thinking)

Qwen3.6-35B-A3B — это мультимодальная модель с открытыми весами от Alibaba Cloud, имеющая 35 миллиардов параметров в общей сложности и 3 миллиарда активных параметров на токен. Она использует гибридную разреженную архитектуру смеси экспертов, сочетающую линейное внимание Gated DeltaNet со стандартными слоями стробируемого внимания, что обеспечивает эффективный инференс при значительно меньших вычислительных затратах.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.6 35B A3B (Non-thinking)

Qwen3.6-35B-A3B — это мультимодальная модель с открытыми весами от Alibaba Cloud, имеющая 35 миллиардов параметров в общей сложности и 3 миллиарда активных параметров на токен. Она использует гибридную разреженную архитектуру смеси экспертов, сочетающую линейное внимание Gated DeltaNet со стандартными слоями стробируемого внимания, что обеспечивает эффективный инференс при значительно меньших вычислительных затратах.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.5 397B A17B (Non-thinking)

Серия Qwen3.5 397B-A17B — модель, построенная на гибридной архитектуре, которая интегрирует механизм линейного внимания с разреженной моделью смеси экспертов, достигая более высокой эффективности вывода.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.5 Plus (от 2026-02-15, версия на 1M контекста)

Версия Qwen 3.5 Plus с расширенным контекстом и улучшенными характеристиками.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.5 Plus (от 2026-02-15)

Версия Qwen 3.5 Plus с расширенным контекстом и улучшенными характеристиками.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3.5 397B A17B

Серия Qwen3.5 397B-A17B — модель, построенная на гибридной архитектуре, которая интегрирует механизм линейного внимания с разреженной моделью смеси экспертов, достигая более высокой эффективности вывода.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 Coder Next

Qwen3-Coder-Next — это открытая языковая модель, оптимизированная для кодирующих агентов и локальных рабочих процессов разработки. Она использует разреженную MoE-архитектуру с 80 млрд общих параметров и только 3 млрд активированных на токен, обеспечивая производительность, сопоставимую с моделями с в 10–20 раз большими активными вычислениями, что делает её идеальной для экономичного развёртывания агентов с постоянной работой.  
  
Модель обучена с сильным акцентом на агентные задачи и надёжно справляется с долгосрочными задачами кодирования, сложным использованием инструментов и восстановлением после ошибок выполнения. Благодаря нативному контекстному окну в 256 тыс. токенов она органично интегрируется в реальные CLI и IDE-окружения и хорошо адаптируется к распространённым агентным каркасам, используемым современными инструментами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 Max

Qwen3-Max — это обновленная версия серии Qwen3, предлагающая значительные улучшения в рассуждениях, следовании инструкциям, многоязычной поддержке и охвате редких знаний по сравнению с версией января 2025 года. Она обеспечивает более высокую точность в задачах по математике, программированию, логике и естественным наукам, более надежно следует сложным инструкциям на китайском и английском языках, снижает галлюцинации и создает более качественные ответы для открытых вопросов и ответов, письма и разговоров. Модель поддерживает более 100 языков с улучшенным переводом и здравым смыслом, оптимизирована для генерации с использованием извлечения информации (RAG) и вызова инструментов, хотя и не включает специальный режим "мышления".  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 Coder Flash

Qwen3 Coder Flash — это быстрая и экономичная версия проприетарной модели Qwen3 Coder Plus от Alibaba. Это мощная модель-агент для программирования, специализирующаяся на автономном программировании через вызов инструментов и взаимодействие с окружающей средой, сочетающая профессионализм в кодировании с универсальными возможностями общего назначения.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 Next 80B A3B

Qwen3-Next-80B-A3B-Instruct — это настроенная на работу с инструкциями чат-модель из серии Qwen3-Next, оптимизированная для быстрых, стабильных ответов без следов "размышлений". Она ориентирована на сложные задачи в области рассуждений, генерации кода, ответов на вопросы на основе знаний и многоязычного использования, сохраняя при этом надежность в согласованности и форматировании. По сравнению с предыдущими инструктивными вариантами Qwen3, она фокусируется на более высокой производительности и стабильности при работе с ультрадлинными входными данными и многоходовыми диалогами, что делает ее хорошо подходящей для RAG, использования инструментов и агентных рабочих процессов, требующих последовательных окончательных ответов, а не видимой цепочки рассуждений.  
  
(Поддержка structured\_output под вопросом)  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen: Qwen3 30B A3B Instruct 2507

Qwen3-30B-A3B-Instruct-2507 — это языковая модель со смесью экспертов с 30,5 млрд параметров от Qwen, с 3,3 млрд активных параметров на инференс. Она работает в режиме без рассуждений и предназначена для высококачественного следования инструкциям, многоязычного понимания и агентного использования инструментов. Дообученная на данных инструкций, она демонстрирует конкурентоспособную производительность в тестах на рассуждение (AIME, ZebraLogic), программирование (MultiPL-E, LiveCodeBench) и выравнивание (IFEval, WritingBench). Она превосходит свой вариант без инструкций в субъективных и открытых задачах, сохраняя при этом сильную производительность в фактических и программных задачах.

Закрыть

X

### Qwen: Qwen3 235B A22B Thinking 2507

Qwen3-235B-A22B-Thinking-2507 — это высокопроизводительная языковая модель с открытыми весами типа Mixture-of-Experts (MoE), оптимизированная для сложных задач рассуждения. Она активирует 22 миллиарда из своих 235 миллиардов параметров за один прямой проход и изначально поддерживает контекст до 262 144 токенов. Этот вариант "только для размышлений" улучшает структурированные логические рассуждения, математику, науку и генерацию длинных текстов, демонстрируя сильную производительность в тестах AIME, SuperGPQA, LiveCodeBench и MMLU-Redux. Модель использует специальный режим рассуждения () и предназначена для генерации выходных данных с большим количеством токенов (до 81 920 токенов) в сложных областях.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen3 Coder 480B A35B (с поддержкой tools)

Qwen3-Coder-480B-A35B-Instruct — это модель генерации кода типа "Смесь экспертов" (MoE), разработанная командой Qwen. Она оптимизирована для агентных задач программирования, таких как вызов функций, использование инструментов и рассуждения в длинном контексте над репозиториями. Модель содержит 480 миллиардов общих параметров, с 35 миллиардами активных на один прямой проход (8 из 160 экспертов).  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen3 Coder 480B A35B

Qwen3-Coder-480B-A35B-Instruct — это модель генерации кода типа "Смесь экспертов" (MoE), разработанная командой Qwen. Она оптимизирована для агентных задач программирования, таких как вызов функций, использование инструментов и рассуждения в длинном контексте над репозиториями. Модель содержит 480 миллиардов общих параметров, с 35 миллиардами активных на один прямой проход (8 из 160 экспертов).

Закрыть

X

### Qwen: Qwen3 235B A22B 2507

Qwen3-235B-A22B-Instruct-2507 — это многоязычная языковая модель со смесью экспертов, настроенная на выполнение инструкций и основанная на архитектуре Qwen3-235B, с 22 миллиардами активных параметров на один проход вперед. Она оптимизирована для универсальной генерации текста, включая следование инструкциям, логические рассуждения, математику, код и использование инструментов. Модель поддерживает нативную длину контекста 262K и не реализует «режим мышления» (блоки ).  
  
По сравнению с базовой версией, эта модель демонстрирует значительные улучшения в охвате знаний, рассуждениях с длинным контекстом, бенчмарках кодирования и согласованности с открытыми задачами. Она особенно сильна в многоязычном понимании, математических рассуждениях (например, AIME, HMMT) и оценках согласованности, таких как Arena-Hard и WritingBench.

Закрыть

X

### Qwen: Qwen3 30B A3B

Qwen3, последнее поколение в серии больших языковых моделей Qwen, представлен как в плотной архитектуре, так и в архитектуре смеси экспертов (MoE), что позволяет ему превосходно справляться с задачами рассуждения, многоязычной поддержки и продвинутыми агентскими задачами. Его уникальная способность плавно переключаться между режимом размышления для сложных рассуждений и режимом без размышлений для эффективного диалога обеспечивает универсальную высококачественную производительность.  
  
Значительно превосходя предыдущие модели, такие как QwQ и Qwen2.5, Qwen3 демонстрирует превосходные возможности в математике, программировании, логических рассуждениях, творческом письме и интерактивном диалоге. Вариант Qwen3-30B-A3B включает 30,5 миллиардов параметров (3,3 миллиарда активированных), 48 слоев, 128 экспертов (8 активируются для каждой задачи).  
  
Вы можете включить режим "без размышлений", добавив к запросу фразу /no\_think, или включить его обратно, добавив фразу /think

Закрыть

X

### Qwen: Qwen3 14B

Qwen3-14B - это плотная причинная языковая модель с 14,8 миллиардами параметров из серии Qwen3, разработанная как для сложных рассуждений, так и для эффективного диалога. Она поддерживает плавное переключение между режимом "размышления" для таких задач, как математика, программирование и логический вывод, и режимом "без размышлений" для общения общего назначения. Модель настроена для следования инструкциям, использования инструментов агентами, креативного письма и многоязычных задач на более чем 100 языках и диалектах.  
  
Вы можете включить режим "без размышлений", добавив к запросу фразу /no\_think, или включить его обратно, добавив фразу /think

Закрыть

X

### Qwen: Qwen3 32B

Qwen3-32B — это плотная причинно-следственная языковая модель с 32,8 миллиардами параметров из серии Qwen3, оптимизированная как для сложных рассуждений, так и для эффективного диалога. Она поддерживает беспрепятственное переключение между режимом "мышления" для таких задач, как математика, программирование и логический вывод, и режимом "без мышления" для более быстрого, универсального общения. Модель демонстрирует высокую производительность в выполнении инструкций, использовании агентских инструментов, творческом письме и многоязычных задачах, охватывая более 100 языков и диалектов.  
  
Вы можете включить режим "без размышлений", добавив к запросу фразу /no\_think, или включить его обратно, добавив фразу /think

Закрыть

X

### Qwen: Qwen3 235B A22B

Qwen3-235B-A22B - это модель на основе смеси экспертов (MoE) с 235 миллиардами параметров, разработанная Qwen, активирующая 22 миллиарда параметров за один прямой проход. Она поддерживает плавное переключение между режимом "размышления" для сложных задач рассуждения, математики и программирования, и режимом "без размышления" для эффективного общего взаимодействия. Модель демонстрирует сильную способность к рассуждению, многоязычную поддержку (более 100 языков и диалектов), продвинутое следование инструкциям и возможности вызова инструментов агента.   
  
Вы можете включить режим "без размышлений", добавив к запросу фразу /no\_think, или включить его обратно, добавив фразу /think

Закрыть

X

### Qwen2.5 72B Instruct (с поддержкой structured outputs)

Версия с поддержкой structured outputs  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Qwen2.5 Coder 32B Instruct

Qwen2.5-Coder - это новейшая серия специализированных языковых моделей Qwen для работы с кодом (ранее известных как CodeQwen). Qwen2.5-Coder предлагает следующие улучшения по сравнению с CodeQwen1.5:  
  
Значительные улучшения в генерации кода, логическом анализе кода и исправлении ошибок.  
Более комплексная основа для практических приложений, таких как Код-агенты. Не только улучшение возможностей программирования, но и сохранение сильных сторон в математике и общих компетенциях.

Закрыть

X

### Qwen2.5 72B Instruct

Qwen2.5 72B - это последняя серия больших языковых моделей Qwen. Qwen2.5 приносит следующие улучшения по сравнению с Qwen2:  
  
Значительно больше знаний и значительно улучшенные возможности в кодировании и математике благодаря нашим специализированным экспертным моделям в этих областях.  
  
Значительные улучшения в следовании инструкциям, генерации длинных текстов (более 8 тысяч токенов), понимании структурированных данных (например, таблиц) и генерации структурированных выходных данных, особенно JSON. Более устойчива к разнообразию системных подсказок, улучшая реализацию ролевых игр и настройку условий для чат-ботов.  
  
Поддержка длинного контекста до 128 тысяч токенов и возможность генерировать до 8 тысяч токенов.  
  
Многоязычная поддержка более 29 языков, включая китайский, английский, французский, испанский, португальский, немецкий, итальянский, русский, японский, корейский, вьетнамский, тайский, арабский и другие.  
  
Использование этой модели регулируется ЛИЦЕНЗИОННЫМ СОГЛАШЕНИЕМ Tongyi Qianwen.

Закрыть

X

### Qwen: Qwen-Plus

Qwen-Plus предоставляет сбалансированное сочетание производительности, скорости и стоимости.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

  

### Z-AI – GLM 5, опенсорс модели от Z.AI

  

Серия языковых моделей от Z.AI (Китай).

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Z.AI: GLM 5.3 Flash (Thinking Max) [?](#mar737taskfull) z-ai/glm-5.3-flash-max  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.035 | 0.10 | 1000000 | 28 авг | нет |
| Z.AI: GLM 5.3 Flash (Thinking Low) [?](#mar736taskfull) z-ai/glm-5.3-flash-low  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.035 | 0.10 | 1000000 | 28 авг | нет |
| Z.AI: GLM 5.3 (Thinking Max, ВРЕМЕННО ВЫКЛЮЧЕНА) [?](#mar731taskfull) z-ai/glm-5.3-max  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 1000000 | 20 авг | нет |
| Z.AI: GLM 5.3 (Thinking Low) [?](#mar730taskfull) z-ai/glm-5.3-low  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 1000000 | 20 авг | нет |
| Z.AI: GLM 5.2 (Thinking High) [?](#mar695taskfull) z-ai/glm-5.2-thinking-high  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 1000000 | 26 июн | нет |
| Z.AI: GLM 5.2 (Non-thinking) [?](#mar694taskfull) z-ai/glm-5.2  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 1000000 | 26 июн | нет |
| Z.AI: GLM 4.7 (MoE 355B всего, 23B активных) (X-Fast, до 300-500 ток/сек) [?](#mar693taskfull) z-ai/glm-4.7-xfast  Базовый и выше (не Тестовый) быстрая tools structured-outputs | 0.25 | 0.38 | 200000 | 26 июн | нет |
| Z.AI: GLM 5.1 (Thinking) [?](#mar650taskfull) z-ai/glm-5.1-thinking  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 200000 | 7 апр | нет |
| Z.AI: GLM 5.1 (Non-thinking) [?](#mar649taskfull) z-ai/glm-5.1  Базовый и выше (не Тестовый) программирование tools structured-outputs | 0.40 | 1.30 | 200000 | 7 апр | нет |
| Z.AI: GLM 5 (Non-thinking) [?](#mar607taskfull) z-ai/glm-5  программирование tools | 0.15 | 0.39 | 200000 | 20 фев | нет |
| Z.AI: GLM 5 (Thinking) [?](#mar600taskfull) z-ai/glm-5-thinking  программирование tools | 0.15 | 0.39 | 200000 | 20 фев | нет |
| Z.AI: GLM 4.7 (MoE 355B всего, 23B активных, обновлена до fast) [?](#mar573taskfull) z-ai/glm-4.7  быстрая tools structured-outputs | 0.09 | 0.32 | 200000 | 27 янв | нет |
| Z.AI: GLM 4.6 (MoE 355B всего, 23B активных) [?](#mar496taskfull) z-ai/glm-4.6  Профессиональный возможный топ по цена/качество tools | 0.09 | 0.32 | 200000 | 2 окт 25 | нет |
| Z.AI: GLM 4.5 (MoE 355B всего, 23B активных) [?](#mar439taskfull) z-ai/glm-4.5  Профессиональный возможный топ по цена/качество tools | 0.09 | 0.32 | 128000 | 29 июл 25 | нет |
| Z.AI: GLM 4.5 Air (MoE 106B всего, 12B активных) [?](#mar438taskfull) z-ai/glm-4.5-air  tools | 0.03 | 0.16 | 128000 | 29 июл 25 | нет |

X

### Z.AI: GLM 5.3 Flash (Thinking Max)

GLM-5.3-Flash — это нативная мультимодальная модель от Z.ai. Она оптимизирована для эффективного написания кода и выполнения сложных агентных задач с длинным горизонтом планирования. Гибридная архитектура на основе разреженного и линейного механизмов внимания обеспечивает точную обработку длинного контекста при одновременном снижении вычислительной нагрузки.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.3 Flash (Thinking Low)

GLM-5.3-Flash — это нативная мультимодальная модель от Z.ai. Она оптимизирована для эффективного написания кода и выполнения сложных агентных задач с длинным горизонтом планирования. Гибридная архитектура на основе разреженного и линейного механизмов внимания обеспечивает точную обработку длинного контекста при одновременном снижении вычислительной нагрузки.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.3 (Thinking Max, ВРЕМЕННО ВЫКЛЮЧЕНА)

GLM 5.3 — это крупномасштабная модель рассуждений от Z.ai. Она поддерживает текстовый ввод и вывод с контекстным окном в 1 миллион токенов и подходит для агентных рабочих процессов с длительным горизонтом планирования, разработки программного обеспечения на уровне проектов и сложной многошаговой автоматизации.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.3 (Thinking Low)

GLM 5.3 — это крупномасштабная модель рассуждений от Z.ai. Она поддерживает текстовый ввод и вывод с контекстным окном в 1 миллион токенов и подходит для агентных рабочих процессов с длительным горизонтом планирования, разработки программного обеспечения на уровне проектов и сложной многошаговой автоматизации.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.2 (Thinking High)

GLM 5.2 — это крупномасштабная модель рассуждений от Z.ai. Она поддерживает текстовый ввод и вывод с контекстным окном в 1 миллион токенов и подходит для агентных рабочих процессов с длительным горизонтом планирования, разработки программного обеспечения на уровне проектов и сложной многошаговой автоматизации.  
  
Размышляющая версия, режим high для размышлений.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.2 (Non-thinking)

GLM 5.2 — это крупномасштабная модель рассуждений от Z.ai. Она поддерживает текстовый ввод и вывод с контекстным окном в 1 миллион токенов и подходит для агентных рабочих процессов с длительным горизонтом планирования, разработки программного обеспечения на уровне проектов и сложной многошаговой автоматизации.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.7 (MoE 355B всего, 23B активных) (X-Fast, до 300-500 ток/сек)

GLM-4.7 — это новейшая флагманская модель Z.AI с улучшениями в двух ключевых областях: расширенные возможности программирования и более стабильное многоэтапное рассуждение/выполнение. Модель демонстрирует значительные улучшения в выполнении сложных агентных задач, обеспечивая при этом более естественное общение и превосходную эстетику интерфейса.  
  
Специальные провайдеры с высокими скоростями до 300-500 токенов в секунду.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.1 (Thinking)

GLM-5.1 обеспечивает значительный скачок в возможностях программирования, с особенно существенными улучшениями в решении долгосрочных задач. В отличие от предыдущих моделей, ориентированных на взаимодействие в рамках нескольких минут, GLM-5.1 способен самостоятельно и непрерывно работать над одной задачей более 8 часов, автономно планируя, выполняя и совершенствуя себя на протяжении всего процесса, в итоге предоставляя полноценные результаты инженерного уровня.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
Модель обучена с сильным акцентом на агентные задачи и надёжно справляется с долгосрочными задачами кодирования, сложным использованием инструментов и восстановлением после ошибок выполнения. Благодаря нативному контекстному окну в 256 тыс. токенов она органично интегрируется в реальные CLI и IDE-окружения и хорошо адаптируется к распространённым агентным каркасам, используемым современными инструментами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5.1 (Non-thinking)

GLM-5.1 обеспечивает значительный скачок в возможностях программирования, с особенно существенными улучшениями в решении долгосрочных задач. В отличие от предыдущих моделей, ориентированных на взаимодействие в рамках нескольких минут, GLM-5.1 способен самостоятельно и непрерывно работать над одной задачей более 8 часов, автономно планируя, выполняя и совершенствуя себя на протяжении всего процесса, в итоге предоставляя полноценные результаты инженерного уровня.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
Модель обучена с сильным акцентом на агентные задачи и надёжно справляется с долгосрочными задачами кодирования, сложным использованием инструментов и восстановлением после ошибок выполнения. Благодаря нативному контекстному окну в 256 тыс. токенов она органично интегрируется в реальные CLI и IDE-окружения и хорошо адаптируется к распространённым агентным каркасам, используемым современными инструментами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5 (Non-thinking)

GLM-5 — это флагманская модель с открытым исходным кодом от Z.ai, разработанная для проектирования сложных систем и долгосрочных агентных рабочих процессов. Созданная для опытных разработчиков, она обеспечивает производительность промышленного уровня при решении крупномасштабных задач программирования, конкурируя с ведущими проприетарными моделями. Благодаря продвинутому агентному планированию, глубокому внутреннему анализу и итеративной самокоррекции, GLM-5 выходит за рамки генерации кода к созданию полноценных систем и автономному выполнению.  
  
Модель обучена с сильным акцентом на агентные задачи и надёжно справляется с долгосрочными задачами кодирования, сложным использованием инструментов и восстановлением после ошибок выполнения. Благодаря нативному контекстному окну в 256 тыс. токенов она органично интегрируется в реальные CLI и IDE-окружения и хорошо адаптируется к распространённым агентным каркасам, используемым современными инструментами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 5 (Thinking)

GLM-5 — это флагманская модель с открытым исходным кодом от Z.ai, разработанная для проектирования сложных систем и долгосрочных агентных рабочих процессов. Созданная для опытных разработчиков, она обеспечивает производительность промышленного уровня при решении крупномасштабных задач программирования, конкурируя с ведущими проприетарными моделями. Благодаря продвинутому агентному планированию, глубокому внутреннему анализу и итеративной самокоррекции, GLM-5 выходит за рамки генерации кода к созданию полноценных систем и автономному выполнению.  
  
Модель обучена с сильным акцентом на агентные задачи и надёжно справляется с долгосрочными задачами кодирования, сложным использованием инструментов и восстановлением после ошибок выполнения. Благодаря нативному контекстному окну в 256 тыс. токенов она органично интегрируется в реальные CLI и IDE-окружения и хорошо адаптируется к распространённым агентным каркасам, используемым современными инструментами.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.7 (MoE 355B всего, 23B активных, обновлена до fast)

GLM-4.7 — это новейшая флагманская модель Z.AI с улучшениями в двух ключевых областях: расширенные возможности программирования и более стабильное многоэтапное рассуждение/выполнение. Модель демонстрирует значительные улучшения в выполнении сложных агентных задач, обеспечивая при этом более естественное общение и превосходную эстетику интерфейса.  
  
Обновлены провайдеры, в идеале скорость должна достигать свыше 100 ток/сек.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.6 (MoE 355B всего, 23B активных)

По сравнению с GLM-4.5, эта модель предлагает несколько ключевых улучшений:  
- Увеличенное контекстное окно: Контекстное окно расширено со 128 тысяч до 200 тысяч токенов, что позволяет модели справляться с более сложными агентными задачами.  
- Превосходная производительность в программировании: Модель достигает более высоких показателей в тестах по программированию и демонстрирует лучшую производительность в реальных приложениях  
- Улучшенное рассуждение: GLM-4.6 показывает явное улучшение в производительности рассуждений и поддерживает использование инструментов во время вывода, что приводит к более сильным общим возможностям.  
- Более способные агенты: GLM-4.6 демонстрирует более сильную производительность в использовании инструментов и агентах, основанных на поиске, и более эффективно интегрируется в агентные фреймворки.  
- Усовершенствованное написание текстов: Лучше соответствует человеческим предпочтениям в стиле и читаемости, и более естественно ведет себя в сценариях ролевых игр.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.5 (MoE 355B всего, 23B активных)

GLM-4.5 — это наша новейшая флагманская базовая модель, специально разработанная для агентных приложений. Она использует архитектуру смеси экспертов (MoE) и поддерживает длину контекста до 128 тысяч токенов. GLM-4.5 обеспечивает значительно улучшенные возможности в области рассуждений, генерации кода и согласования с агентами. Она поддерживает гибридный режим вывода с двумя опциями: «режим мышления», предназначенный для сложных рассуждений и использования инструментов, и «режим без мышления», оптимизированный для мгновенных ответов.  
  
Для включения режима "без размышлений" добавьте в промт фразу /nothink  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.5 Air (MoE 106B всего, 12B активных)

GLM-4.5-Air — это облегченная версия нашего новейшего флагманского семейства моделей, специально созданная для приложений, ориентированных на агентов. Как и GLM-4.5, она использует архитектуру смеси экспертов (MoE), но с более компактным размером параметров. GLM-4.5-Air также поддерживает гибридные режимы вывода, предлагая «режим размышления» для продвинутого рассуждения и использования инструментов, а также «режим без размышления» для взаимодействия в реальном времени.  
  
Для включения режима "без размышлений" добавьте в промт фразу /nothink  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

  

### Minimax – модели от Minimax

  

Серия языковых моделей от Minimax (Китай).

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || MiniMax: MiniMax M3 [?](#mar685taskfull) minimax/minimax-m3  Базовый и выше (не Тестовый) tools   vision | 0.09 | 0.36 | 1000000 | 10 июн | нет |
| MiniMax: MiniMax M2.7 [?](#mar640taskfull) minimax/minimax-m2.7  tools | 0.045 | 0.18 | 200000 | 25 мар | нет |
| MiniMax: MiniMax M2.5 [?](#mar591taskfull) minimax/minimax-m2.5  tools | 0.045 | 0.18 | 196000 | 13 фев | нет |
| MiniMax: MiniMax M2.1 [?](#mar574taskfull) minimax/minimax-m2.1  tools | 0.045 | 0.18 | 196000 | 23 дек 25 | нет |
| MiniMax: MiniMax M2 [?](#mar509taskfull) minimax/minimax-m2  tools | 0.045 | 0.18 | 196000 | 31 окт 25 | нет |
| MiniMax: MiniMax M1 (Thinking) [?](#mar402taskfull) minimax/minimax-m1  Профессиональный размышления | 0.08 | 0.33 | 1000000 | 18 июн 25 | нет |
| MiniMax: MiniMax-01 [?](#mar249taskfull) minimax/minimax-01  Профессиональный большой контекст | 0.03 | 0.20 | 1000000 | 17 янв 25 | нет |

X

### MiniMax: MiniMax M3

MiniMax-M3 — это мультимодальная базовая модель от MiniMax. Она поддерживает контекстное окно в 1 миллион токенов и хорошо подходит для длительных агентных задач, написания кода и работы с инструментами. В её основе лежит механизм MiniMax Sparse Attention (MSA), который заменяет полное внимание на выборку KV-блоков, снижая вычислительные затраты на каждый токен при большом контексте — примерно в 20 раз дешевле по сравнению с предыдущим поколением при 1 миллионе токенов, при этом значительно ускоряя обработку и генерацию без потери качества на большинстве задач.  
  
Модель обучена как нативно мультимодальная — на перемежающихся данных и настроена для многоходовых сценариев, близких к реальным условиям эксплуатации, с помощью интерактивного фреймворка на основе симулятора пользователя. Она ориентирована на длительные многошаговые задачи, а не на однократное выполнение запросов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MiniMax: MiniMax M2.7

MiniMax-M2.7 — это большая языковая модель нового поколения, разработанная для автономной продуктивности в реальных условиях и непрерывного совершенствования. Созданная для активного участия в собственной эволюции, M2.7 интегрирует передовые агентные возможности посредством многоагентного взаимодействия, что позволяет ей планировать, выполнять и уточнять сложные задачи в динамических средах.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MiniMax: MiniMax M2.5

MiniMax-M2.5 — это передовая большая языковая модель, разработанная для реальной продуктивной работы. Обученная в разнообразных сложных цифровых рабочих средах реального мира, M2.5 развивает экспертные навыки программирования M2.1, расширяясь в область общей офисной работы, достигая беглости в создании и работе с файлами Word, Excel и PowerPoint, переключении контекста между различными программными средами и работе в разных командах агентов и людей. Набрав 80,2% в SWE-Bench Verified, 51,3% в Multi-SWE-Bench и 76,3% в BrowseComp, M2.5 также более эффективна в использовании токенов, чем предыдущие поколения, будучи обученной оптимизировать свои действия и результаты посредством планирования.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MiniMax: MiniMax M2.1

MiniMax-M2.1 — это легкая, современная большая языковая модель, оптимизированная для программирования, агентных рабочих процессов и разработки современных приложений. Всего с 10 миллиардами активированных параметров она обеспечивает значительный скачок в реальной производительности, сохраняя при этом исключительную задержку, масштабируемость и экономическую эффективность.  
  
По сравнению с предшественником M2.1 выдает более чистые и лаконичные результаты, а также обеспечивает более быстрое воспринимаемое время отклика. Модель демонстрирует ведущую многоязычную производительность в программировании для основных систем и языков приложений, достигая 49,4% на Multi-SWE-Bench и 72,5% на SWE-Bench Multilingual, и служит универсальным агентным «мозгом» для IDE, инструментов программирования и помощи общего назначения.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MiniMax: MiniMax M2

MiniMax-M2 — это компактная высокоэффективная большая языковая модель, оптимизированная для сквозного кодирования и агентных рабочих процессов. С 10 миллиардами активированных параметров (230 миллиардов всего) она обеспечивает интеллект, близкий к передовому, в области общих рассуждений, использования инструментов и выполнения многошаговых задач, сохраняя при этом низкую задержку и эффективность развертывания.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MiniMax: MiniMax M1 (Thinking)

MiniMax-M1 — это крупномасштабная модель рассуждений с открытыми весами, разработанная для расширенного контекста и высокоэффективного вывода. Она использует гибридную архитектуру Mixture-of-Experts (MoE) в сочетании с пользовательским механизмом "молниеносного внимания", что позволяет ей обрабатывать длинные последовательности — до 1 миллиона токенов — при сохранении конкурентоспособной эффективности FLOP. С 456 миллиардами общих параметров и 45,9 миллиардами активных параметров на токен, этот вариант оптимизирован для сложных многоэтапных задач рассуждения.  
  
Обученная с помощью специального конвейера обучения с подкреплением (CISPO), M1 превосходно справляется с пониманием длинного контекста, программной инженерией, агентным использованием инструментов и математическими рассуждениями. Тесты показывают высокую производительность в FullStackBench, SWE-bench, MATH, GPQA и TAU-Bench, часто превосходя другие открытые модели, такие как DeepSeek R1 и Qwen3-235B.

Закрыть

X

### MiniMax: MiniMax-01

В серии MiniMax-01 мы совершили смелую инновацию: впервые в крупном масштабе мы внедрили новый механизм Lightning Attention, предлагая альтернативу традиционной архитектуре Transformer. Эта модель насчитывает впечатляющие 456 миллиардов параметров, из которых 45,9 миллиардов параметров активируются при каждом выводе. Её общая производительность находится на уровне ведущих мировых моделей, при этом она эффективно обрабатывает самую длинную в мире контекстную длину до 4 миллионов токенов (в рамках сервиса доступен контекст до 1 млн токенов)

Закрыть

  

### Moonshot AI: Kimi K2, K2.5 и пр.

  

Серия языковых моделей от Moonshot AI (Китай).

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || MoonshotAI: Kimi K3 (Fast, X2 к скорости) [?](#mar735taskfull) moonshotai/kimi-k3-fast  Профессиональный (не Тестовый) tools structured-outputs   vision | 1.35 | 6.75 | 1000000 | 28 авг | нет |
| MoonshotAI: Kimi K3 [?](#mar711taskfull) moonshotai/kimi-k3  Профессиональный (не Тестовый) tools structured-outputs   vision | 0.9 | 4.5 | 1000000 | 16 июл | нет |
| MoonshotAI: Kimi K2.7 Code [?](#mar686taskfull) moonshotai/kimi-k2.7-code  программирование и общие задачи tools structured-outputs   vision | 0.27 | 1.20 | 262000 | 12 июн | нет |
| MoonshotAI: Kimi K2.6 (Thinking) [?](#mar658taskfull) moonshotai/kimi-k2.6-thinking  программирование и общие задачи tools structured-outputs   vision | 0.27 | 1.20 | 262000 | 20 апр | нет |
| MoonshotAI: Kimi K2.6 [?](#mar657taskfull) moonshotai/kimi-k2.6  программирование и общие задачи tools structured-outputs   vision | 0.27 | 1.20 | 262000 | 20 апр | нет |
| MoonshotAI: Kimi K2.5 [?](#mar585taskfull) moonshotai/kimi-k2.5  программирование и общие задачи tools structured-outputs   vision | 0.18 | 0.90 | 262000 | 29 янв | нет |
| MoonshotAI: Kimi K2 от 5 сентября (1T параметров), быстрая, до 400 ток/сек [?](#mar470taskfull) moonshotai/kimi-k2-0905-fast  программирование и общие задачи tools structured-outputs | 0.14 | 0.45 | 256000 | 9 сен 25 | нет |
| MoonshotAI: Kimi K2 от 5 сентября (1T параметров) [?](#mar469taskfull) moonshotai/kimi-k2-0905  программирование и общие задачи tools structured-outputs | 0.08 | 0.37 | 256000 | 9 сен 25 | нет |
| MoonshotAI: Kimi K2 (1T параметров) [?](#mar422taskfull) moonshotai/kimi-k2  программирование и общие задачи tools structured-outputs | 0.075 | 0.35 | 128000 | 12 июл 25 | нет |

X

### MoonshotAI: Kimi K3 (Fast, X2 к скорости)

Kimi K3 — это сверхмасштабная мультимодальная модель рассуждения с открытыми весами от Moonshot AI. Она предназначена для решения сложных задач в области программирования, работы со знаниями и долгосрочных агентных процессов, а также особенно хорошо справляется с навигацией по крупным репозиториям, использованием инструментов, отладкой и итеративной работой с изображениями, логами, тестами и обратной связью от среды выполнения. В её архитектуре используются KDA и остаточные связи в механизме внимания для повышения вычислительной эффективности.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 400р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K3

Kimi K3 — это сверхмасштабная мультимодальная модель рассуждения с открытыми весами от Moonshot AI. Она предназначена для решения сложных задач в области программирования, работы со знаниями и долгосрочных агентных процессов, а также особенно хорошо справляется с навигацией по крупным репозиториям, использованием инструментов, отладкой и итеративной работой с изображениями, логами, тестами и обратной связью от среды выполнения. В её архитектуре используются KDA и остаточные связи в механизме внимания для повышения вычислительной эффективности.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 400р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2.7 Code

MoonshotAI: Kimi K2.7 Code — это модель семейства Kimi K2 от Moonshot AI, ориентированная на программирование и предназначенная для надёжного выполнения задач разработки от начала до конца в рамках длинного контекста. Модель построена на нативной мультимодальной архитектуре смеси экспертов, поддерживает текстовый и графический ввод и всегда работает в режиме «размышления», сохраняя полное содержимое цепочки рассуждений на протяжении всего многоходового диалога. Контекстное окно объёмом 256 тысяч токенов позволяет решать сложные долгосрочные задачи программирования, декомпозировать агентские задания и вести многоходовые диалоги. Модель активирует 32 миллиарда параметров из примерно 1 триллиона общего числа.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2.6 (Thinking)

Апдейт Kimi K2.  
Kimi K2.6 — это мультимодальная модель нового поколения от Moonshot AI, разработанная для решения долгосрочных задач в области программирования, генерации пользовательских интерфейсов на основе кода, а также оркестрации мультиагентных систем. Модель справляется со сложными комплексными задачами разработки на Python, Rust и Go, а также способна преобразовывать текстовые запросы и визуальные данные в готовые к производственному использованию интерфейсы. Архитектура на основе роя агентов масштабируется до сотен параллельных субагентов для автономной декомпозиции задач — позволяя создавать документы, веб-сайты и таблицы за один запуск без участия человека.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2.6

Апдейт Kimi K2.  
Kimi K2.6 — это мультимодальная модель нового поколения от Moonshot AI, разработанная для решения долгосрочных задач в области программирования, генерации пользовательских интерфейсов на основе кода, а также оркестрации мультиагентных систем. Модель справляется со сложными комплексными задачами разработки на Python, Rust и Go, а также способна преобразовывать текстовые запросы и визуальные данные в готовые к производственному использованию интерфейсы. Архитектура на основе роя агентов масштабируется до сотен параллельных субагентов для автономной декомпозиции задач — позволяя создавать документы, веб-сайты и таблицы за один запуск без участия человека.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2.5

Апдейт Kimi K2.  
Kimi K2 — это крупномасштабная языковая модель типа Mixture-of-Experts (MoE), разработанная компанией Moonshot AI, содержащая 1 триллион параметров с 32 миллиардами активных параметров на один прямой проход. Она оптимизирована для агентных возможностей, включая продвинутое использование инструментов, рассуждения и синтез кода. Kimi K2 превосходно справляется с широким спектром тестов, особенно в области программирования (LiveCodeBench, SWE-bench), рассуждений (ZebraLogic, GPQA) и использования инструментов (Tau2, AceBench).  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2 от 5 сентября (1T параметров), быстрая, до 400 ток/сек

Kimi K2 0905 — это сентябрьское обновление Kimi K2 0711. Это крупномасштабная языковая модель Mixture-of-Experts (MoE), разработанная Moonshot AI, с общим количеством параметров в 1 триллион, из которых 32 миллиарда активны при каждом прямом проходе. Она поддерживает обработку длинного контекста до 256 тысяч токенов, что является увеличением по сравнению с предыдущими 128 тысячами.  
  
Это обновление улучшает агентное программирование с повышенной точностью и лучшей обобщающей способностью для различных структур, а также совершенствует фронтенд-разработку, создавая более эстетичные и функциональные результаты для веб-приложений, 3D и связанных задач. Kimi K2 оптимизирована для агентных возможностей, включая продвинутое использование инструментов, рассуждение и синтез кода. Она превосходно справляется с тестами по программированию (LiveCodeBench, SWE-bench), логическому мышлению (ZebraLogic, GPQA) и использованию инструментов (Tau2, AceBench).   
  
Рекомендуется температура ниже 1 - около 0.7-0.9, чтобы избежать некорректных символов при генерации.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2 от 5 сентября (1T параметров)

Kimi K2 0905 — это сентябрьское обновление Kimi K2 0711. Это крупномасштабная языковая модель Mixture-of-Experts (MoE), разработанная Moonshot AI, с общим количеством параметров в 1 триллион, из которых 32 миллиарда активны при каждом прямом проходе. Она поддерживает обработку длинного контекста до 256 тысяч токенов, что является увеличением по сравнению с предыдущими 128 тысячами.  
  
Это обновление улучшает агентное программирование с повышенной точностью и лучшей обобщающей способностью для различных структур, а также совершенствует фронтенд-разработку, создавая более эстетичные и функциональные результаты для веб-приложений, 3D и связанных задач. Kimi K2 оптимизирована для агентных возможностей, включая продвинутое использование инструментов, рассуждение и синтез кода. Она превосходно справляется с тестами по программированию (LiveCodeBench, SWE-bench), логическому мышлению (ZebraLogic, GPQA) и использованию инструментов (Tau2, AceBench).   
  
Рекомендуется температура ниже 1 - около 0.7-0.9, чтобы избежать некорректных символов при генерации.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### MoonshotAI: Kimi K2 (1T параметров)

Kimi K2 — это крупномасштабная языковая модель типа Mixture-of-Experts (MoE), разработанная компанией Moonshot AI, содержащая 1 триллион параметров с 32 миллиардами активных параметров на один прямой проход. Она оптимизирована для агентных возможностей, включая продвинутое использование инструментов, рассуждения и синтез кода. Kimi K2 превосходно справляется с широким спектром тестов, особенно в области программирования (LiveCodeBench, SWE-bench), рассуждений (ZebraLogic, GPQA) и использования инструментов (Tau2, AceBench).  
  
Рекомендуется температура ниже 1 - около 0.7-0.9, чтобы избежать некорректных символов при генерации.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

  
  

## Российские: Сайга и Вихрь – альтернатива YaGPT и GigaChat

  

**Сайга – третья модель, сфокусированная на российском языке после моделей от Яндекса (YaGPT) и Сбера (GigaChat)** – и сравнима с ними. Подробнее об истории возникновения – в нашей статье на Хабре: [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)https://habr.com/ru/articles/767588/](https://habr.com/ru/articles/767588/ "Внешняя ссылка (откроется в новом окне)")   
   
Также здесь представлены модели от команды VikhrModels, которая также с 2024 года начала дотренировывать опенсорсные модели на русских данных. Они также рекомендуются к знакомству – по метрикам они не хуже gpt-3.5 и могут приближаться к gpt-4o-mini.  
   
*Серия моделей OMF включает в себя «холодный старт» – т.е. загрузку по мере запроса. Если на первый запрос вы не получили ответ по таймауту, просто подождите 1–2 минуты и попробуйте снова – весьма вероятно, что модель загрузится.*

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Saiga Gemma 3 12B (российский разработчик) [?](#mar350taskfull) OMF-R-IlyaGusev/saiga\_gemma3\_12b  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/IlyaGusev/saiga_gemma3_12b) | 0.10 | 0.10 | 16000 | 30 апр 25 | нет |
| SAINEMO-reMIX (микс русскоязычных моделей) [?](#mar237taskfull) OMF-R-Moraliane/SAINEMO-reMIX  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/Moraliane/SAINEMO-reMIX) | 0.10 | 0.10 | 16000 | 16 дек 24 | нет |
| Сайга MistralNemo 12B v1 (российский разработчик) [?](#mar216taskfull) OMF-R-IlyaGusev/saiga\_nemo\_12b  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/IlyaGusev/saiga_nemo_12b) | 0.10 | 0.10 | 8192 | 3 ноя 24 | нет |
| Vikhr-Nemo-12B-Instruct-R-21-09-24 (российский разработчик) [?](#mar198taskfull) OMF-R-Vikhr-Nemo-12B-Instruct-R-21-09-24  Open Models Fan За вызов: 0.15 р. [Hugging Face](https://huggingface.co/Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24) | 0.10 | 0.10 | 16000 | 22 сен 24 | нет |
| Vikhr-Llama3.1-8B-Instruct-R-21-09-24 (российский разработчик) [?](#mar197taskfull) OMF-R-Vikhr-Llama3.1-8B-Instruct-R-21-09-24  Open Models Fan За вызов: 0.10 р. [Hugging Face](https://huggingface.co/Vikhrmodels/Vikhr-Llama3.1-8B-Instruct-R-21-09-24) | 0.10 | 0.10 | 16000 | 22 сен 24 | нет |
| Saiga/Llama3 8B (российский разработчик) [?](#mar150taskfull) OMF-R-IlyaGusev/saiga\_llama3\_8b  Open Models Fan За вызов: 0.10 р. [Hugging Face](https://huggingface.co/IlyaGusev/saiga_llama3_8b) | 0.10 | 0.10 | 8192 | 19 июл 24 | нет |

X

### Saiga Gemma 3 12B (российский разработчик)

Версия Сайги на базе MistralNemo 12B. Автор: Илья Гусев  
  
Уникальная фича модели — расцензурированность и ориентация на role-play.  
Обучена на abliterated версии Gemma 3 12B.

Закрыть

X

### SAINEMO-reMIX (микс русскоязычных моделей)

Модель представляет микс из Сайги, Вихрь, и ряда англоязычных моделей с целью получить хорошую модель для русскоязычного ролеплея.  
  
Модель показала высокие результаты в ролеплей рейтинге.

Закрыть

X

### Сайга MistralNemo 12B v1 (российский разработчик)

Версия Сайги на базе MistralNemo 12B. Автор: Илья Гусев  
  
Уникальная фича модели — расцензурированность и ориентация на role-play. Обучена abliterated версии Немо, и из и SFT, и SimPO датасетов вычищены отказы.  
  
К сожалению, ввиду особенностей инференса, не даем гарантий, что роль system упоминается в темплейте корректно. В случае проблем исключите роль system из чата.

Закрыть

X

### Vikhr-Nemo-12B-Instruct-R-21-09-24 (российский разработчик)

Описание от команды VikhrModels  
  
Vikhr-Nemo - это наша флагманская унимодальная LLM (Large Language Model) представляющая из себя улучшенную версию mistralai/Mistral-Nemo-Instruct-2407 командой VikhrModels, адаптированную преимущественно для русского и английского языков. Для ее обучения мы использовали несколько этапов включающих в себя SFT и SMPO - нашу собственную вариацию DPO, подробнее читайте в секции "Как эта модель создавалась".  
  
Модель оптимизированна для различных вариантов использования, включая ризонинг, суммаризацию, код, roleplay, поддержание диалога. Vikhr-Nemo обладает возможностью многоязычной генерации, и высокопроизводительными возможностями RAG. Модель иммет лучшие оценки среди прочих на наших инструктивных и RAG бенчарках и, поэтому, мы верим, что в некоторых задачах (например, RAG) может быть не хуже gpt-4o-mini от OpenAI.

Закрыть

X

### Vikhr-Llama3.1-8B-Instruct-R-21-09-24 (российский разработчик)

Vikhr-Llama3.1 - это унимодальная LLM (Large Language Model) на 8B параметров представляющая из себя улучшенную версию meta-llama/Meta-Llama-3.1-8B-Instruct командой VikhrModels, адаптированную преимущественно для русского и английского языков. Для обучения использовались несколько этапов включающих в себя SFT и SMPO.  
  
Модель оптимизирована для различных вариантов использования, включая ризонинг, суммаризацию, код, roleplay, поддержание диалога. Vikhr-Llama обладает возможностью многоязычной генерации, и высокопроизводительными возможностями RAG. Модель иммет лучшие оценки среди прочих на наших инструктивных и RAG бенчарках и, поэтому, мы верим, что во многих задачах может быть лучше чем gpt-3.5-turbo от OpenAI.

Закрыть

X

### Saiga/Llama3 8B (российский разработчик)

Версия Сайги для LLama3 8B

Закрыть

  

## Опенсорс

### Обычные опенсорс модели

  

**Различные опенсорс модели**. Эти модели в первую очередь тренировались на английском языке (учтите это), но и на русском могут показывать неплохое качество. В отличие от коммерческих моделей они, как правило, не используют автомодерацию запросов по этическому признаку. Читайте описания к модели по знаку “?". Как правило, модели с большим числом параметров (70B против 7B) более точны и лучше рассуждают, но и более дороги в обработке.  
   
В тегах указано, на чем специализируется модель. Если тег не указан – модель многоцелевая, т.е. чаще всего обычное следование инструкциям, но лучше прочитать описание.  
   
Если на русский запрос они выдают не очень хороший результат, попробуйте обращаться к ним на английском, или попробуйте наши translate-версии (ниже). **Особенно рекомендуется translate-версии для ролеплейных моделей (если вы не пишете на английском)**

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Xiaomi: MiMo-V2.5 Pro (Thinking) [?](#mar692taskfull) xiaomi/mimo-v2.5-pro-thinking  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.13 | 0.26 | 1000000 | 16 июн | нет |
| Xiaomi: MiMo-V2.5 Pro [?](#mar691taskfull) xiaomi/mimo-v2.5-pro  Профессиональный (не Тестовый) tools structured-outputs   vision  audioinput | 0.13 | 0.26 | 1000000 | 16 июн | нет |
| Xiaomi: MiMo-V2.5 (Thinking) [?](#mar690taskfull) xiaomi/mimo-v2.5-thinking  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.05 | 0.09 | 1000000 | 16 июн | нет |
| Xiaomi: MiMo-V2.5 [?](#mar689taskfull) xiaomi/mimo-v2.5  Базовый и выше (не Тестовый) tools structured-outputs   vision  audioinput | 0.05 | 0.09 | 1000000 | 16 июн | нет |
| AionLabs: Aion-2.0 (ролеплей модель на базе Deepseek 3.2, размышляющая) [?](#mar608taskfull) aion/aion-2.0  ролеплей | 0.12 | 0.24 | 128000 | 25 фев | нет |
| Nous: Hermes 4 405B [?](#mar468taskfull) nousresearch/hermes-4-405b | 0.15 | 0.45 | 128000 | 2 сен 25 | нет |
| Nous: Hermes 4 70B [?](#mar467taskfull) nousresearch/hermes-4-70b | 0.02 | 0.07 | 128000 | 2 сен 25 | нет |
| Llama 3.3 70B Instruct (SuperFast, порядка 1000-2000 токенов в секунду) [?](#mar354taskfull) meta-llama/llama-3.3-70b-instruct-superfast  Базовый и выше (не Тестовый) superfast tools structured-outputs | 0.14 | 0.18 | 32000 | 8 мая 25 | нет |
| Llama 4 Scout (SuperFast, порядка 1000-2000 токенов в секунду!) [?](#mar353taskfull) meta-llama/llama-4-scout-superfast  superfast structured-outputs | 0.10 | 0.14 | 32000 | 8 мая 25 | нет |
| Llama 4 Maverick (быстрая, до 400 токенов в секунду) [?](#mar342taskfull) meta-llama/llama-4-maverick-fast  Профессиональный | 0.09 | 0.22 | 1000000 | 6 апр 25 | нет |
| Llama 4 Maverick Online HQ [?](#mar322taskfull) meta-llama/llama-4-maverick-online-hq  Профессиональный За вызов: 2.0 р. онлайн tools structured-outputs | 0.03 | 0.12 | 1000000 | 7 апр 25 | нет |
| Llama 4 Maverick [?](#mar319taskfull) meta-llama/llama-4-maverick  Профессиональный tools structured-outputs | 0.03 | 0.12 | 1000000 | 6 апр 25 | нет |
| Llama 4 Scout (быстрая) [?](#mar318taskfull) meta-llama/llama-4-scout  fast tools | 0.022 | 0.08 | 328000 | 6 апр 25 | нет |
| Llama 3.3 70B Instruct (быстрая, более 200 токенов в секунду) [?](#mar276taskfull) meta-llama/llama-3.3-70b-instruct-fast | 0.10 | 0.15 | 128000 | 14 фев 25 | нет |
| Sao10K: Llama 3.3 Euryale 70B [?](#mar242taskfull) sao10k/l3.3-euryale-70b  ролеплей | 0.25 | 0.25 | 8000 | 19 дек 24 | нет |
| Llama 3.3 70B Instruct (с поддержкой structured outputs) [?](#mar239taskfull) meta-llama/llama-3.3-70b-structured  Профессиональный structured-outputs | 0.22 | 0.22 | 128000 | 19 дек 24 | нет |
| Llama 3.3 70B Instruct [?](#mar227taskfull) meta-llama/llama-3.3-70b-instruct | 0.08 | 0.08 | 128000 | 8 дек 24 | нет |
| Rocinante 12B [?](#mar210taskfull) thedrummer/rocinante-12b  ролеплей | 0.04 | 0.075 | 32768 | 16 окт 24 | нет |
| Llama 3.2 3B Instruct [?](#mar202taskfull) meta-llama/llama-3.2-3b-instruct | 0.015 | 0.05 | 128000 | 26 сен 24 | нет |
| Llama 3.1 Euryale 70B v2.2 [?](#mar183taskfull) sao10k/l3.1-euryale-70b  квантизация fp8 ролеплей [Hugging Face](https://huggingface.co/Sao10K/L3.1-70B-Euryale-v2.2) | 0.25 | 0.25 | 8192 | 28 авг 24 | нет |
| Hermes 3 405B Instruct [?](#mar182taskfull) nousresearch/hermes-3-llama-3.1-405b  ролеплей и общие вопросы | 0.70 | 0.70 | 128000 | 17 авг 24 | нет |
| Llama 3.1 70B Instruct meta-llama/llama-3.1-70b-instruct  tools | 0.12 | 0.12 | 128000 | 24 июл 24 | нет |
| Llama 3.1 8B Instruct meta-llama/llama-3.1-8b-instruct | 0.027 | 0.06 | 128000 | 24 июл 24 | нет |
| NVIDIA Nemotron 4 340B Instruct [?](#mar137taskfull) nvidia/nemotron-4-340b-instruct  выключена провайдером топ опенсорс переводчик от 25 июня общие вопросы | 0.63 | 0.63 | 4096 | 25 июн 24 | нет |
| WizardLM-2 8x22B [?](#mar99taskfull) microsoft/wizardlm-2-8x22b  топ ролеплей от 17 апреля ролеплей и общие вопросы | 0.15 | 0.15 | 65536 | 18 апр 24 | нет |
| Gryphe: MythoMax L2 13B [?](#mar6taskfull) gryphe/mythomax-L2-13b  дешевая 13B | 0.04 | 0.04 | 4096 | 8 мар 24 | нет |

X

### Xiaomi: MiMo-V2.5 Pro (Thinking)

MiMo-V2.5-Pro — это флагманская модель Xiaomi, демонстрирующая высокие результаты в области универсальных агентных возможностей, сложной разработки программного обеспечения и задач с долгосрочным горизонтом планирования. Модель занимает лидирующие позиции в таких бенчмарках, как ClawEval, GDPVal и SWE-bench Pro. Она способна самостоятельно и автономно выполнять профессиональные задачи, на которые у специалистов-людей уходят дни или недели, задействуя при этом более тысячи обращений к инструментам. Поддержка контекстного окна объёмом до 1 миллиона токенов делает её удобной для интеграции с широким спектром агентных фреймворков.  
  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Xiaomi: MiMo-V2.5 Pro

MiMo-V2.5-Pro — это флагманская модель Xiaomi, демонстрирующая высокие результаты в области универсальных агентных возможностей, сложной разработки программного обеспечения и задач с долгосрочным горизонтом планирования. Модель занимает лидирующие позиции в таких бенчмарках, как ClawEval, GDPVal и SWE-bench Pro. Она способна самостоятельно и автономно выполнять профессиональные задачи, на которые у специалистов-людей уходят дни или недели, задействуя при этом более тысячи обращений к инструментам. Поддержка контекстного окна объёмом до 1 миллиона токенов делает её удобной для интеграции с широким спектром агентных фреймворков.  
  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Xiaomi: MiMo-V2.5 (Thinking)

MiMo-V2.5 — это нативная омнимодальная модель от Xiaomi. Она обеспечивает производительность уровня Pro в агентных задачах примерно при вдвое меньших затратах на инференс, превосходя MiMo-V2-Omni в мультимодальном восприятии при работе с изображениями. Контекстное окно в 1 миллион токенов позволяет обрабатывать целые документы, длинные диалоги и сложные задачи за один проход, что делает модель идеальным выбором для интеграции с агентными фреймворками, где важны развитые способности к рассуждению, богатое восприятие и экономичность.  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Xiaomi: MiMo-V2.5

MiMo-V2.5 — это нативная омнимодальная модель от Xiaomi. Она обеспечивает производительность уровня Pro в агентных задачах примерно при вдвое меньших затратах на инференс, превосходя MiMo-V2-Omni в мультимодальном восприятии при работе с изображениями. Контекстное окно в 1 миллион токенов позволяет обрабатывать целые документы, длинные диалоги и сложные задачи за один проход, что делает модель идеальным выбором для интеграции с агентными фреймворками, где важны развитые способности к рассуждению, богатое восприятие и экономичность.  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### AionLabs: Aion-2.0 (ролеплей модель на базе Deepseek 3.2, размышляющая)

Aion-2.0 — это вариант Deepseek V3.2, оптимизированный для иммерсивных ролевых игр и сторителлинга. Он особенно хорошо справляется с созданием напряжённости, кризисов и конфликтов в истории, делая повествование более захватывающим. Также он работает со взрослыми и мрачными темами с большей тонкостью и глубиной.

Закрыть

X

### Nous: Hermes 4 405B

Hermes 4 — это крупномасштабная модель для рассуждений, созданная на основе Meta-Llama-3.1-405B и выпущенная компанией Nous Research.  
  
Для генерации русского текста рекомендуется использовать пониженную температуру около 0.7, и top\_p=0.95

Закрыть

X

### Nous: Hermes 4 70B

Hermes 4 70B — это гибридная модель рассуждений от Nous Research, созданная на основе Meta-Llama-3.1-70B.  
  
Для генерации русского текста рекомендуется использовать пониженную температуру около 0.7, и top\_p=0.95

Закрыть

X

### Llama 3.3 70B Instruct (SuperFast, порядка 1000-2000 токенов в секунду)

Meta Llama 3.3 - это многоязычная языковая модель большого масштаба (LLM), предварительно обученная и настроенная на выполнение инструкций, размером 70B (текст на входе/текст на выходе). Текстовая модель Llama 3.3, настроенная на выполнение инструкций, оптимизирована для многоязычных диалоговых сценариев использования и превосходит многие доступные модели с открытым и закрытым исходным кодом по общепринятым отраслевым показателям.  
  
По бенчмаркам сопоставима с Llama 3.1 405B  
  
Используется экстрабыстрый провайдер - до 32К контекста.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Scout (SuperFast, порядка 1000-2000 токенов в секунду!)

Llama 4 Scout 17B Instruct (16E) - это языковая модель на основе смеси экспертов (MoE), разработанная компанией Meta, активирующая 17 миллиардов параметров из общего числа 109 миллиардов.   
  
Модель последний раз обучалась на данных до августа 2024 года и была публично запущена 5 апреля 2025 года.  
  
Для запуска используется экстрабыстрый провайдер, но контекст ограничен 32К.  
  
Поддержка tools не декларировалась официально, но присутствует.  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Maverick (быстрая, до 400 токенов в секунду)

Llama 4 Maverick 17B Instruct (128E) — это мультимодальная языковая модель высокой ёмкости от Meta, построенная на архитектуре смеси экспертов (MoE) со 128 экспертами и 17 миллиардами активных параметров за один прямой проход (400 миллиардов всего).   
  
Модель последний раз обучалась на данных до августа 2024 года и была публично запущена 5 апреля 2025 года.  
  
Поддержка tools не декларировалась официально, но присутствует.  
  
Быстрые провайдеры: отвечают быстро, но могут быть нестабильны.

Закрыть

X

### Llama 4 Maverick Online HQ

Версия Llama 4 Maverick с расширенным поиском по интернету - при ответе берется 20 источников.  
Рекомендуется задавать запрос максимально просто, одним предложением, например: Сравни Nvidia 5070 и 4090.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Maverick

Llama 4 Maverick 17B Instruct (128E) — это мультимодальная языковая модель высокой ёмкости от Meta, построенная на архитектуре смеси экспертов (MoE) со 128 экспертами и 17 миллиардами активных параметров за один прямой проход (400 миллиардов всего).   
  
Модель последний раз обучалась на данных до августа 2024 года и была публично запущена 5 апреля 2025 года.  
  
Поддержка tools не декларировалась официально, но присутствует.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Scout (быстрая)

Llama 4 Scout 17B Instruct (16E) - это языковая модель на основе смеси экспертов (MoE), разработанная компанией Meta, активирующая 17 миллиардов параметров из общего числа 109 миллиардов.   
  
Модель последний раз обучалась на данных до августа 2024 года и была публично запущена 5 апреля 2025 года.  
  
Для запуска используется сет провайдеров:  
- Быстрый инференс (до 400 токенов в секунду) предоставляется, если вход не превышает 128К токенов, а требуемый выход - 8К токенов  
- В противном случае используются дополнительные провайдеры, которые могут обрабатывать вход и выход вплоть до 328К токенов  
  
Поддержка tools не декларировалась официально, но присутствует.  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 3.3 70B Instruct (быстрая, более 200 токенов в секунду)

Meta Llama 3.3 - это многоязычная языковая модель большого масштаба (LLM), предварительно обученная и настроенная на выполнение инструкций, размером 70B (текст на входе/текст на выходе). Текстовая модель Llama 3.3, настроенная на выполнение инструкций, оптимизирована для многоязычных диалоговых сценариев использования и превосходит многие доступные модели с открытым и закрытым исходным кодом по общепринятым отраслевым показателям.  
  
По бенчмаркам сопоставима с Llama 3.1 405B  
  
Модель использует квантизацию bf16

Закрыть

X

### Sao10K: Llama 3.3 Euryale 70B

Euryale L3.3 70B - это модель от Sao10k, ориентированная на креативную ролевую игру. Она является преемником Euryale L3 70B v2.2.

Закрыть

X

### Llama 3.3 70B Instruct (с поддержкой structured outputs)

Версия Llama 3.3 70B с поддержкой structured outputs  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 3.3 70B Instruct

Meta Llama 3.3 - это многоязычная языковая модель большого масштаба (LLM), предварительно обученная и настроенная на выполнение инструкций, размером 70B (текст на входе/текст на выходе). Текстовая модель Llama 3.3, настроенная на выполнение инструкций, оптимизирована для многоязычных диалоговых сценариев использования и превосходит многие доступные модели с открытым и закрытым исходным кодом по общепринятым отраслевым показателям.  
  
По бенчмаркам сопоставима с Llama 3.1 405B  
  
Модель использует квантизацию bf16

Закрыть

X

### Rocinante 12B

Rocinante 12B разработан для увлекательного повествования и богатой прозы.  
  
Ранние тестировщики сообщали о:  
  
Расширенном словарном запасе с уникальным и выразительным выбором слов  
Улучшенной креативности для создания ярких повествований  
Наполненных приключениями и захватывающих историях

Закрыть

X

### Llama 3.2 3B Instruct

Llama 3.2 3B - это многоязычная модель большого языка с 3 миллиардами параметров, оптимизированная для продвинутых задач обработки естественного языка, таких как генерация диалогов, рассуждения и обобщение. Разработанная с использованием новейшей архитектуры трансформеров, она поддерживает восемь языков, включая английский, испанский и хинди, и адаптируема для дополнительных языков.  
  
Обученная на 9 триллионах токенов, модель Llama 3.2B отлично справляется с выполнением инструкций, сложными рассуждениями и использованием инструментов. Её сбалансированная производительность делает её идеальной для приложений, требующих точности и эффективности в генерации текста в многоязычных средах.

Закрыть

X

### Llama 3.1 Euryale 70B v2.2

Euryale L3.1 70B v2.2 - это модель, ориентированная на креативную ролевую игру, созданная Sao10k. Она является преемником Euryale L3 70B v2.1, но уже на базе модели Llama 3.1, которая значительно лучше работает с русским языком.

Закрыть

X

### Hermes 3 405B Instruct

Гермес 3 - это универсальная языковая модель со многими улучшениями по сравнению с Гермесом 2, включая продвинутые агентные возможности, гораздо лучшее ролевое взаимодействие, рассуждение, многоходовую беседу, согласованность длинного контекста и улучшения по всем направлениям.  
  
Гермес 3 405B - это полнопараметрическая доводка базовой модели Llama-3.1 405B уровня передовых технологий, ориентированная на согласование языковых моделей с пользователем, с мощными возможностями управления и контроля, предоставляемыми конечному пользователю.

Закрыть

X

### NVIDIA Nemotron 4 340B Instruct

Nemotron-4-340B-Instruct - это англоязычная модель чата, оптимизированная для генерации синтетических данных. Эта крупная языковая модель (LLM) является доработанной версией Nemotron-4-340B-Base, разработанной для одно- и многоходовых сценариев чата с контекстной длиной 4096 токенов.  
  
Базовая модель была предварительно обучена на 9 триллионах токенов из разнообразных английских текстов, более 50 естественных языков и более 40 языков программирования. Инструктивная модель прошла дополнительные этапы настройки:  
  
- Супервизированное дообучение (SFT)  
- Прямая оптимизация предпочтений (DPO)  
- Оптимизация предпочтений с учетом вознаграждения (RPO)  
  
В процессе выравнивания использовалось примерно 20 тыс. образцов, аннотированных человеком, в то время как 98% данных для дообучения были синтетически сгенерированы.  
  
Модель умеет работать с русским языком

Закрыть

X

### WizardLM-2 8x22B

WizardLM-2 8x22B — самая совершенная модель Wizard от Microsoft AI. Она демонстрирует высокую конкурентоспособность по сравнению с ведущими проприетарными моделями и неизменно превосходит все существующие современные модели с открытым исходным кодом.

Закрыть

X

### Gryphe: MythoMax L2 13B

Из серии Mytho моделей, сделана поверх Llama2 13b   
  
Очень популярна на Западе для самых разных запросов, включая ролеплей.  
  
Очень низкая цена - 13B модель по цене 7B.

Закрыть

  

### Самые свежие опенсорс модели Open Models Fan (OMF) (бета-тест)

  

**Самые свежие опенсорс модели серии Open Models Fan (могут быть недоступны на Тестовом тарифе)**.   
   
Особенности:  
– Модели доступны для **экспериментирования**, а не для реальной автоматизации (но они также доступны через API). Поэтому, пожалуйста, используйте их вручную или на малом объеме автоматических запросов (до 500). Если вам нужно интенсивно работать с ними, рекомендуем развернуть их на собственном сервере. Если мы увидим большое число автоматических запросов от вас к этим моделям, мы оставляем за собой право временно заблокировать ваш аккаунт  
– Следствие – **мы берем плату за вызов и небольшую плату за входные и выходные символы**. Таким образом, эти модели более выгодно использовать для долгого ролеплея с большим контекстом (если они это поддерживают)  
– Скорость вывода – 10–40 токенов в секунду, в зависимости от размера модели.   
– Модели 70B и выше поставляются в **квантизации FP8** – создавая баланс между загрузкой серверов и качеством. В целом, падение качества по сравнению с FP16 и FP32 (оригинал) довольно небольшое.  
– Размер контекста не гарантирован (в процессе выяснения у провайдера)  
– Обычно опенсорсные файнтюны моделей в первую очередь предназначены для ролеплея и написания историй (часто – на английском, если не указано обратное). Для общих кейсов мы рекомендуем обычные модели.  
– *Серия моделей OMF включает в себя «холодный старт» – т.е. загрузку по мере запроса. Если на первый запрос вы не получили ответ по таймауту, просто подождите 1–2 минуты и попробуйте снова – весьма вероятно, что модель загрузится.*  
   
 Пожалуйста, поддержите опенсорсную альтернативу проприетарным моделям!

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Gemma 3 27B (abliterated alt) [?](#mar545taskfull) OMF-gemma3-27b-abliterated-dpo  Open Models Fan За вызов: 0.20 р. ролеплей [Hugging Face](https://huggingface.co/summykai/gemma3-27b-abliterated-dpo) | 0.15 | 0.15 | 32000 | 19 ноя 25 | нет |
| Saiga Gemma 3 12B (российский разработчик) [?](#mar350taskfull) OMF-R-IlyaGusev/saiga\_gemma3\_12b  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/IlyaGusev/saiga_gemma3_12b) | 0.10 | 0.10 | 16000 | 30 апр 25 | нет |
| Gemma 3 27B (abliterated) [?](#mar332taskfull) OMF-Gemma3-27B-abliterated  Open Models Fan За вызов: 0.20 р. ролеплей [Hugging Face](https://huggingface.co/mlabonne/gemma-3-27b-it-abliterated) | 0.15 | 0.15 | 16384 | 12 апр 25 | нет |
| Pantheon RP 1.8 24b [?](#mar315taskfull) OMF-Pantheon-RP-1.8-24b-Small-3.1  Open Models Fan За вызов: 0.20 р. ролеплей [Hugging Face](https://huggingface.co/Gryphe/Pantheon-RP-1.8-24b-Small-3.1) | 0.15 | 0.15 | 16384 | 31 мар 25 | нет |
| Forgotten Abomination 24B V2.2 [?](#mar306taskfull) OMF-Forgotten-Abomination-24B-V2.2  Open Models Fan За вызов: 0.20 р. ролеплей [Hugging Face](https://huggingface.co/ReadyArt/Forgotten-Abomination-24B-V2.2) | 0.15 | 0.15 | 16384 | 19 мар 25 | нет |
| Hamanasu QwQ 32B V2 RP [?](#mar305taskfull) OMF-Hamanasu-QwQ-32B-V2-RP  Open Models Fan За вызов: 0.25 р. ролеплей [Hugging Face](https://huggingface.co/Delta-Vector/Hamanasu-QwQ-V2-RP) | 0.18 | 0.18 | 16384 | 19 мар 25 | нет |
| QwQ 32B (abliterated) [?](#mar304taskfull) OMF-QwQ-32B-abliterated  Open Models Fan За вызов: 0.25 р. ролеплей | 0.18 | 0.18 | 16384 | 19 мар 25 | нет |
| SAINEMO-reMIX (микс русскоязычных моделей) [?](#mar237taskfull) OMF-R-Moraliane/SAINEMO-reMIX  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/Moraliane/SAINEMO-reMIX) | 0.10 | 0.10 | 16000 | 16 дек 24 | нет |
| EVA Qwen2.5-72B v0.1 [?](#mar218taskfull) OMF-EVA-Qwen2.5-72B-v0.1  Open Models Fan За вызов: 0.50 р. ролеплей | 0.25 | 0.25 | 8192 | 8 ноя 24 | нет |
| Сайга MistralNemo 12B v1 (российский разработчик) [?](#mar216taskfull) OMF-R-IlyaGusev/saiga\_nemo\_12b  Open Models Fan За вызов: 0.15 р. ролеплей [Hugging Face](https://huggingface.co/IlyaGusev/saiga_nemo_12b) | 0.10 | 0.10 | 8192 | 3 ноя 24 | нет |
| EVA Qwen2.5-72B v0.0 [?](#mar215taskfull) OMF-EVA-Qwen2.5-72B-v0.0  Open Models Fan За вызов: 0.50 р. ролеплей | 0.25 | 0.25 | 8192 | 3 ноя 24 | нет |
| Qwen2.5-72B-Instruct-abliterated [?](#mar212taskfull) OMF-Qwen2.5-72B-Instruct-abliterated  Open Models Fan За вызов: 0.50 р. ролеплей и общие вопросы [Hugging Face](https://huggingface.co/zetasepic/Qwen2.5-72B-Instruct-abliterated) | 0.25 | 0.25 | 16000 | 16 окт 24 | нет |
| Vikhr-Nemo-12B-Instruct-R-21-09-24 (российский разработчик) [?](#mar198taskfull) OMF-R-Vikhr-Nemo-12B-Instruct-R-21-09-24  Open Models Fan За вызов: 0.15 р. [Hugging Face](https://huggingface.co/Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24) | 0.10 | 0.10 | 16000 | 22 сен 24 | нет |
| Vikhr-Llama3.1-8B-Instruct-R-21-09-24 (российский разработчик) [?](#mar197taskfull) OMF-R-Vikhr-Llama3.1-8B-Instruct-R-21-09-24  Open Models Fan За вызов: 0.10 р. [Hugging Face](https://huggingface.co/Vikhrmodels/Vikhr-Llama3.1-8B-Instruct-R-21-09-24) | 0.10 | 0.10 | 16000 | 22 сен 24 | нет |
| Smaug Qwen2 72B Instruct [?](#mar161taskfull) OMF-abacusai/Smaug-Qwen2-72B-Instruct  Open Models Fan За вызов: 0.50 р. ролеплей и общие вопросы [Hugging Face](https://huggingface.co/abacusai/Smaug-Qwen2-72B-Instruct) | 0.25 | 0.25 | 16000 | 22 июл 24 | нет |
| Tess v2.5.2 Qwen2 72B [?](#mar158taskfull) OMF-Tess-v2.5.2-Qwen2-72B  Open Models Fan За вызов: 0.50 р. [Hugging Face](https://huggingface.co/migtissera/Tess-v2.5.2-Qwen2-72B) | 0.25 | 0.25 | 16000 | 19 июл 24 | нет |
| MG-FinalMix-72B (Magnum-72B based) [?](#mar157taskfull) OMF-Undi95/MG-FinalMix-72B  Open Models Fan За вызов: 0.50 р. ролеплей [Hugging Face](https://huggingface.co/Undi95/MG-FinalMix-72B) | 0.25 | 0.25 | 16000 | 19 июл 24 | нет |
| Saiga/Llama3 8B (российский разработчик) [?](#mar150taskfull) OMF-R-IlyaGusev/saiga\_llama3\_8b  Open Models Fan За вызов: 0.10 р. [Hugging Face](https://huggingface.co/IlyaGusev/saiga_llama3_8b) | 0.10 | 0.10 | 8192 | 19 июл 24 | нет |

X

### Gemma 3 27B (abliterated alt)

Версия Gemma 3 27B без этических фильтров, альтернативная.

Закрыть

X

### Saiga Gemma 3 12B (российский разработчик)

Версия Сайги на базе MistralNemo 12B. Автор: Илья Гусев  
  
Уникальная фича модели — расцензурированность и ориентация на role-play.  
Обучена на abliterated версии Gemma 3 12B.

Закрыть

X

### Gemma 3 27B (abliterated)

Модель Gemma 3 27B, дотюненая на выключение этических фильтров.

Закрыть

X

### Pantheon RP 1.8 24b

Модель Mistral 3.1 24B, дотюненая на ролеплей.

Закрыть

X

### Forgotten Abomination 24B V2.2

Модель Mistral 3 24B, дотюненая на ролеплей.

Закрыть

X

### Hamanasu QwQ 32B V2 RP

Размышляющая модель QwQ-32B, дотюненая на ролеплей.

Закрыть

X

### QwQ 32B (abliterated)

Размышляющая модель QwQ-32B, дотюненая на выключение этических фильтров

Закрыть

X

### SAINEMO-reMIX (микс русскоязычных моделей)

Модель представляет микс из Сайги, Вихрь, и ряда англоязычных моделей с целью получить хорошую модель для русскоязычного ролеплея.  
  
Модель показала высокие результаты в ролеплей рейтинге.

Закрыть

X

### EVA Qwen2.5-72B v0.1

Обновленная специализированная модель для ролевых игр и написания историй, файнтюн Qwen2.5-72B на смеси синтетических и естественных данных.  
Использует набор данных Celeste 70B 0.1, значительно расширенный для улучшения универсальности, креативности и "характера" результирующей модели.  
  
Примечания к версии 0.1: Обработанный заново набор данных (через Cahvay для 32B 0.2, использован также здесь), скорректированная конфигурация обучения для 8xH100 SXM. Значительные улучшения в следовании инструкциям, понимании длинного контекста и общей согласованности по сравнению с v0.0.

Закрыть

X

### Сайга MistralNemo 12B v1 (российский разработчик)

Версия Сайги на базе MistralNemo 12B. Автор: Илья Гусев  
  
Уникальная фича модели — расцензурированность и ориентация на role-play. Обучена abliterated версии Немо, и из и SFT, и SimPO датасетов вычищены отказы.  
  
К сожалению, ввиду особенностей инференса, не даем гарантий, что роль system упоминается в темплейте корректно. В случае проблем исключите роль system из чата.

Закрыть

X

### EVA Qwen2.5-72B v0.0

Специализированная модель для ролевых игр и написания историй, файнтюн Qwen2.5-72B на смеси синтетических и естественных данных.  
Использует набор данных Celeste 70B 0.1, значительно расширенный для улучшения универсальности, креативности и "характера" результирующей модели.

Закрыть

X

### Qwen2.5-72B-Instruct-abliterated

Файнтюн версии Qwen2.5-72B, который значительно реже отказывается отвечать.

Закрыть

X

### Vikhr-Nemo-12B-Instruct-R-21-09-24 (российский разработчик)

Описание от команды VikhrModels  
  
Vikhr-Nemo - это наша флагманская унимодальная LLM (Large Language Model) представляющая из себя улучшенную версию mistralai/Mistral-Nemo-Instruct-2407 командой VikhrModels, адаптированную преимущественно для русского и английского языков. Для ее обучения мы использовали несколько этапов включающих в себя SFT и SMPO - нашу собственную вариацию DPO, подробнее читайте в секции "Как эта модель создавалась".  
  
Модель оптимизированна для различных вариантов использования, включая ризонинг, суммаризацию, код, roleplay, поддержание диалога. Vikhr-Nemo обладает возможностью многоязычной генерации, и высокопроизводительными возможностями RAG. Модель иммет лучшие оценки среди прочих на наших инструктивных и RAG бенчарках и, поэтому, мы верим, что в некоторых задачах (например, RAG) может быть не хуже gpt-4o-mini от OpenAI.

Закрыть

X

### Vikhr-Llama3.1-8B-Instruct-R-21-09-24 (российский разработчик)

Vikhr-Llama3.1 - это унимодальная LLM (Large Language Model) на 8B параметров представляющая из себя улучшенную версию meta-llama/Meta-Llama-3.1-8B-Instruct командой VikhrModels, адаптированную преимущественно для русского и английского языков. Для обучения использовались несколько этапов включающих в себя SFT и SMPO.  
  
Модель оптимизирована для различных вариантов использования, включая ризонинг, суммаризацию, код, roleplay, поддержание диалога. Vikhr-Llama обладает возможностью многоязычной генерации, и высокопроизводительными возможностями RAG. Модель иммет лучшие оценки среди прочих на наших инструктивных и RAG бенчарках и, поэтому, мы верим, что во многих задачах может быть лучше чем gpt-3.5-turbo от OpenAI.

Закрыть

X

### Smaug Qwen2 72B Instruct

Довольно сильный файюнтюн Smaug теперь и на базе Qwen 72B, с расширенным контекстом 16 000 токенов.

Закрыть

X

### Tess v2.5.2 Qwen2 72B

Мы создали Tess-v2.5.2, новейшую передовую модель в серии больших языковых моделей (LLM) Tess. Tess, сокращение от Tesoro (Сокровище на итальянском), - это флагманская серия LLM, созданная Мигелем Тиссерой. Tess-v2.5.2 приносит значительные улучшения в способностях рассуждения, кодирования и математики. В настоящее время это модель №1 с открытым весом при оценке по MMLU (Massive Multitask Language Understanding). Она набирает больше баллов, чем все другие модели с открытым весом, включая Qwen2-72B-Instruct, Llama3-70B-Instruct, Mixtral-8x22B-Instruct и DBRX-Instruct. Более того, при оценке по MMLU, модель Tess-v2.5.2 (Qwen2-72B) превосходит даже передовые закрытые модели Gemini-1.0-Ultra, Gemini-1.5-Pro, Mistral-Large и Claude-3-Sonnet.

Закрыть

X

### MG-FinalMix-72B (Magnum-72B based)

Доработка Magnum-72B от Undi95

Закрыть

X

### Saiga/Llama3 8B (российский разработчик)

Версия Сайги для LLama3 8B

Закрыть

  

## Примечания

  
**Автомодерация** – означает, что, в соответствии с требованиями поставщика модели автоматически проверяется вход на несоответствие этическим нормам (Terms Of Service конкретной модели). В случае, если запрос не проходит модерацию, возвращается ошибка и деньги не списываются.  
  
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/file.gif)Ответ на вопрос «Настоящая ли GPT-4 на сайте, если она не отвечает, что она GPT-4 в чате»](https://vsegpt.ru/pdfs/is_gpt4_on_vsegpt.pdf)

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Модели генерации эмбеддингов для RAG - OpenAI text-embedding-ada-002, text-embedding-3-large

Источник: https://vsegpt.ru/Docs/Models/Embeddings

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Embeddings

  

**Embeddings-модели для вычисления семантической схожести текстов**. Для эндпойнта v1/embeddings. (Если вы не знаете, что это такое, оно вам не нужно).  
   
Пример реализации RAG с использованием наших эмбеддингов доступен [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)у нас на Github](https://github.com/janvarev/demo_rag_vsegpt "Внешняя ссылка (откроется в новом окне)")

  

### Старые (v2)

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Text Embedding Ada v2 [?](#mar36taskfull) text-embedding-ada-002 | 0.03 | 0.00 | 1024 | 13 мар 24 | нет |

X

### Text Embedding Ada v2

Модель для текстовых эмбеддингов от OpenAI

Закрыть

  

### Новые (v3)

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Qwen: Qwen3 Embedding 8b (тест) [?](#mar511taskfull) emb-qwen/qwen3-embedding-8b | 0.009 | 0.0 | 32000 | 31 окт 25 | нет |
| OpenAI: text-embedding-3-large (тест) emb-openai/text-embedding-3-large | 0.035 | 0.0 | 32000 | 13 мар 24 | нет |
| OpenAI: text-embedding-3-small (тест) emb-openai/text-embedding-3-small | 0.006 | 0.0 | 32000 | 13 мар 24 | нет |

X

### Qwen: Qwen3 Embedding 8b (тест)

Серия моделей Qwen3 Embedding является новейшей проприетарной моделью семейства Qwen, специально разработанной для задач встраивания и ранжирования текста. Эта серия наследует исключительные возможности многоязычности, понимания длинных текстов и навыки рассуждения своей базовой модели. Серия Qwen3 Embedding представляет собой значительный прогресс в решении множества задач встраивания и ранжирования текста, включая поиск текста, поиск кода, классификацию текста, кластеризацию текста и извлечение параллельных текстов.

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Модели генерации изображений по изображениям - FLUX 2, Google Nano Banana Pro...

Источник: https://vsegpt.ru/Docs/Models/Img2Img

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

[Image-to-image (редактирование изображений)](#h210-1)

[Общие модели (Google Nano Banana (Pro) Edit, FLUX Edit...)](#h210-2)

[AI Transform – трансформация изображений](#h210-3)

  

## Image-to-image (редактирование изображений)

### Общие модели (Google Nano Banana (Pro) Edit, FLUX Edit...)

  

**Модели для редактирования изображений с самыми разными запросами**  
Можно использовать через меню Сервисы > Текстовый фоторедактор (для зарегистрированных пользователей) или по API.

  

![](https://vsegpt.ru/pdfs/google_flash_edit2.png)

![](https://vsegpt.ru/pdfs/google_flash_edit_multi1.png)

  
  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| OpenAI: GPT-5.4 Image 2 (ChatGPT Images 2.0) (Multi Edit, редактирование изображений) [?](#mar660taskfull) img2img-openai/gpt-image-2-edit-multi  Профессиональный (не Тестовый) топ от 22 апреля отличная типографика 6 / 21 / 63 р. за изображение | 10.0 | 0.0 | 2000 | 22 апр | нет |
| Google Nano Banana 2 Edit Multi References (Flash Image 3.1) [?](#mar612taskfull) img2img-google/nano-banana-2-edit-multi  Профессиональный (не Тестовый) с поддержкой русского текста редактирование изображений 19.9 р за изображение | 19.9 | 0.0 | 2000 | 27 фев | нет |
| Flux 2 [klein] 4B Multi Edit [?](#mar578taskfull) img2img-flux/flux-2-klein-4b  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 3.9 р. за 1 изображение | 3.9 | 0.0 | 2000 | 15 янв | нет |
| ByteDance Seedream 4.5, Multi Image-to-Image [?](#mar559taskfull) img2img-bytedance/seedream-v4.5-edit-multi  Профессиональный (не Тестовый) конкурент Nano Banana Pro с поддержкой русского текста 13.9 р. за изображение | 13.9 | 0.0 | 2000 | 8 дек 25 | да |
| FLUX 2 (flex) Multi Edit (временно отключена из-за проблем) [?](#mar551taskfull) img2img-flux/flux-2-flex-multi-edit  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 18/36 р. за 1 изображение | 10.0 | 0.0 | 2000 | 26 ноя 25 | нет |
| Google Nano Banana Pro (Gemini Image Pro 3 Preview) Edit Image Multi References [?](#mar547taskfull) img2img-google/nano-banana-pro-edit-multi  Профессиональный (не Тестовый) топ с поддержкой русского текста редактирование изображений 29.9 р за изображение | 29.9 | 0.0 | 2000 | 20 ноя 25 | да |
| Reve Fast (Edit Multi) [?](#mar522taskfull) img2img-reve-fast-edit-multi  Базовый и выше (не Тестовый) генерация изображений 3.0 р. за изображение | 3.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Reve Fast (Edit) [?](#mar521taskfull) img2img-reve-fast-edit  Базовый и выше (не Тестовый) генерация изображений 3.0 р. за изображение | 3.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Nvidia: Chrono (Edit, Thinking) [?](#mar513taskfull) img2img-nvidia/chrono-edit-thinking  Профессиональный (не Тестовый) генерация изображений 3.0 р. за изображение | 3.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Nvidia: Chrono (Edit) [?](#mar512taskfull) img2img-nvidia/chrono-edit  Профессиональный (не Тестовый) генерация изображений 3.0 р. за изображение | 3.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Reve (Edit Multi) [?](#mar508taskfull) img2img-reve-edit-multi  Профессиональный (не Тестовый) генерация изображений 8.9 р. за изображение | 8.9 | 0.0 | 2000 | 24 окт 25 | нет |
| Reve (Edit) [?](#mar507taskfull) img2img-reve-edit  Профессиональный (не Тестовый) генерация изображений 8.9 р. за изображение | 8.9 | 0.0 | 2000 | 24 окт 25 | нет |
| GPT Image 1 mini (Edit Multi) [?](#mar505taskfull) img2img-openai/gpt-image-1-mini-edit-multi  Профессиональный (не Тестовый) генерация изображений 5.0 р. за изображение | 5.0 | 0.0 | 2000 | 24 окт 25 | нет |
| ByteDance Seedream 4.0 Edit Multi References [?](#mar472taskfull) img2img-bytedance/seedream-v4-edit-multi  Профессиональный (не Тестовый) редактирование изображений 6.9 р за изображение | 6.9 | 0.0 | 2000 | 11 сен 25 | нет |
| Google Flash Image 2.5 Edit Multi References (Nano Banana) [?](#mar457taskfull) img2img-google/flash-25-edit-multi  Профессиональный (не Тестовый) редактирование изображений 9.9 р за изображение | 9.9 | 0.0 | 2000 | 26 авг 25 | нет |
| FLUX.1 Kontext [max] Image Edit Multi [?](#mar391taskfull) img2img-flux/kontext-max-edit-multi  Профессиональный (не Тестовый) редактирование изображений 15 р. за изображение | 15.0 | 0.0 | 2000 | 2 июн 25 | нет |
| FLUX.1 Kontext [pro] Image Edit Multi [?](#mar390taskfull) img2img-flux/kontext-pro-edit-multi  Профессиональный (не Тестовый) редактирование изображений 7.5 р. за изображение | 7.5 | 0.0 | 2000 | 2 июн 25 | нет |
| FLUX.1 Kontext [max] Image Edit [?](#mar389taskfull) img2img-flux/kontext-max-edit  Профессиональный (не Тестовый) редактирование изображений 15.0 р. за изображение | 15.0 | 0.0 | 2000 | 2 июн 25 | нет |
| FLUX.1 Kontext [pro] Image Edit [?](#mar388taskfull) img2img-flux/kontext-pro-edit  Профессиональный (не Тестовый) редактирование изображений 7.5 р. за изображение | 7.5 | 0.0 | 2000 | 2 июн 25 | нет |
| Ideogram V3 (замена фона) [?](#mar362taskfull) img2img-ideogram/v3-multi-replace-background  Профессиональный (не Тестовый) генерация изображений 7.9 р. за изображение | 10.0 | 0.0 | 2000 | 16 мая 25 | нет |
| DD Colorization (раскрашивание черно-белых изображений) [?](#mar361taskfull) img2img-dd/colorization  генерация изображений 0.8 р. за изображение | 0.8 | 0.0 | 2000 | 16 мая 25 | нет |
| Recraft V3 Image Edit [?](#mar360taskfull) img2img-recraft/v3-edit  Профессиональный (не Тестовый) генерация изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 16 мая 25 | нет |
| Recraft V3 Upscaler (улучшение разрешения изображения) [?](#mar359taskfull) img2img-recraft/v3-upscale-crisp  генерация изображений 0.8 р. за изображение | 0.8 | 0.0 | 2000 | 16 мая 25 | нет |
| Google Flash Edit Multi References [?](#mar356taskfull) img2img-google/flash-edit-multi  Профессиональный За вызов: 9.9 р. редактирование изображений 9.9 р за изображение | 0.0 | 0.0 | 2000 | 8 мая 25 | нет |
| Google Flash Edit [?](#mar321taskfull) img2img-google/flash-edit  Профессиональный За вызов: 9.9 р. редактирование изображений 9.9 р за изображение | 0.0 | 0.0 | 2000 | 7 апр 25 | нет |

X

### OpenAI: GPT-5.4 Image 2 (ChatGPT Images 2.0) (Multi Edit, редактирование изображений)

Стоимость за генерацию зависит от качества:  
- low: 6 р.  
- medium: 21 р. (по умолчанию)  
- high: 63 р.  
  
Модель поддерживает разрешения (выбирайте их вручную в выпадающем списке!):  
- 1024x1024  
- 1024x768, 768x1024  
- 1280x720, 720x1280  
  
(Если вам ОЧЕНЬ нужны дополнительные разрешения для данной модели, пожалуйста, обратитесь в техподдержку)  
  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Google Nano Banana 2 Edit Multi References (Flash Image 3.1)

Google Nano Banana 2 Edit Multi References — это модель, которая может редактировать отдельное изображение с помощью текстовой подсказки и (опционально) нескольких референсных изображений.  
  
Поддерживается всего до 4 изображений на вход.  
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
(Точно работает с JPEG-картинками; были проблемы с PNG)  
  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Flux 2 [klein] 4B Multi Edit

Композиция изображений из других изображений с помощью FLUX.2 klein 4B от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает любые разрешения

Закрыть

X

### ByteDance Seedream 4.5, Multi Image-to-Image

Топовая модель для редактирования изображений с поддержкой русского текста на картинках.   
Поддерживается всего до 10 изображений на вход.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json".  
  
Соотношение сторон задается автоматически, но вы можете задать его в текстовом промте добавив фразу типа следующей: "The image has a 4:3 aspect ratio"

Закрыть

X

### FLUX 2 (flex) Multi Edit (временно отключена из-за проблем)

Композиция изображений из других изображений с помощью FLUX.2 [flex] от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения по цене в 18 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 36 р / генерация  
  
Подробное описание возможностей:  
  
- Управление цветовым кодом HEX  
Указывайте точные цвета с помощью HEX-кодов для точного подбора цвета и соблюдения фирменного стиля. Для достижения наилучших результатов используйте ключевое слово "color" или "hex" перед кодом.  
  
Например:   
  
"a wall painted in color #2ECC71"  
"gradient from hex #FF6B6B to hex #4ECDC4"  
"the car in color #1A1A1A with accents in #FFD700"  
  
- Ссылки на изображения с помощью @  
  
Ссылайтесь на загруженные изображения непосредственно в промптах, используя символ @ для интуитивной работы с несколькими изображениями.  
  
Например:   
"@image1 wearing the outfit from @image2"  
"combine the style of @image1 with the composition of @image2"  
"the person from @image1 in the setting from @image3"  
  
- JSON-промт  
  
Для точного контроля над сложной генерацией используйте структурированные JSON промпты вместо естественного языка. JSON промптинг обеспечивает детальную спецификацию элементов сцены, объектов, настроек камеры и композиции.  
  
Basic JSON structure:  
{  
"scene": "Overall setting description",  
"subjects": [  
{  
"type": "Subject category",  
"description": "Physical attributes and details",  
"pose": "Action or stance",  
"position": "foreground/midground/background"  
}  
],  
"style": "Artistic rendering approach",  
"color\_palette": ["color1", "color2", "color3"],  
"lighting": "Lighting conditions and direction",  
"mood": "Emotional atmosphere",  
"composition": "rule of thirds/centered/dynamic diagonal",  
"camera": {  
"angle": "eye level/low angle/high angle",  
"distance": "close-up/medium shot/wide shot",  
"lens": "35mm/50mm/85mm"  
}  
}

Закрыть

X

### Google Nano Banana Pro (Gemini Image Pro 3 Preview) Edit Image Multi References

Google Nano Banana Pro — это топовая модель с поддержкой русского текста на картинках, которая может редактировать отдельное изображение с помощью текстовой подсказки и (опционально) нескольких референсных изображений.  
  
Поддерживается всего до 10 изображений на вход.  
Поддерживает установку соотношения сторон финальной картинки - не забывайте настроить это в интерфейсе.   
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
(Точно работает с JPEG-картинками; были проблемы с PNG)  
  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Reve Fast (Edit Multi)

Модель Reve Fast для ремикса изображений (поддерживает до 4 изображений)  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Reve Fast (Edit)

Модель Reve Fast для редактирования 1 изображения.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### Nvidia: Chrono (Edit, Thinking)

Логически последовательная и физически корректная модель редактирования изображений от NVIDIA  
Данный вариант включает в себя "шаги размышления" для редактирования картинки - лучше, но дольше.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### Nvidia: Chrono (Edit)

Логически последовательная и физически корректная модель редактирования изображений от NVIDIA  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### Reve (Edit Multi)

Модель Reve для ремикса изображений (поддерживает до 4 изображений)  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Reve (Edit)

Модель Reve для редактирования 1 изображения.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### GPT Image 1 mini (Edit Multi)

Модель поддерживает редактирование и компоновку до 4 изображений.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### ByteDance Seedream 4.0 Edit Multi References

ByteDance Seedream 4.0 Edit Multi References — это модель, которая может редактировать отдельное изображение с помощью текстовой подсказки и (опционально) нескольких референсных изображений.  
  
Поддерживается всего до 4 изображений.  
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"

Закрыть

X

### Google Flash Image 2.5 Edit Multi References (Nano Banana)

Google Flash Image 2.5 Edit Multi References (Nano Banana) — это модель, которая может редактировать отдельное изображение с помощью текстовой подсказки и (опционально) нескольких референсных изображений.  
  
Поддерживается всего до 4 изображений на вход.  
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
(Точно работает с JPEG-картинками; были проблемы с PNG)  
  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### FLUX.1 Kontext [max] Image Edit Multi

Экспериментальная версия FLUX.1 Kontext [max] с возможностями обработки нескольких изображений.  
MAX-модель лучше следует промту, но при его отсутствии менее креативная.  
  
Поддерживает установку aspect\_ratio для целевого изображения.  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 Kontext [pro] Image Edit Multi

Экспериментальная версия FLUX.1 Kontext [pro] с возможностями обработки нескольких изображений  
  
Поддерживает установку aspect\_ratio для целевого изображения.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 Kontext [max] Image Edit

FLUX.1 Kontext [max] обрабатывает как текст, так и эталонные изображения в качестве входных данных, безупречно обеспечивая целенаправленное локальное редактирование и сложные трансформации целых сцен.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 Kontext [pro] Image Edit

FLUX.1 Kontext [pro] обрабатывает как текст, так и эталонные изображения в качестве входных данных, безупречно обеспечивая целенаправленное локальное редактирование и сложные трансформации целых сцен.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Ideogram V3 (замена фона)

Стоимость за генерацию зависит от качества:  
- TURBO: 7.90 р.  
- BALANCED: 14.90 р.  
- QUALITY: 19.90 р.  
  
Модель поддерживает кроме промта дополнительные изображения в качестве референса.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### DD Colorization (раскрашивание черно-белых изображений)

Позволяет превратить черно-белое изображение в цветное.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Recraft V3 Image Edit

Позволяет отредактировать текущее изображение.  
  
Поддерживает дополнительные аргументы в JSON:  
- style (строка)  
- strength (float)  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Recraft V3 Upscaler (улучшение разрешения изображения)

Улучшает заданное растровое изображение с помощью инструмента "четкое масштабирование", повышая разрешение с акцентом на улучшение мелких деталей и лиц.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Google Flash Edit Multi References

Google Flash Edit Multi References — это модель, которая может редактировать отдельное изображение с помощью текстовой подсказки и нескольких референсных изображений.  
  
Поддерживается всего до 4 изображений.  
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"

Закрыть

X

### Google Flash Edit

Google Flash Edit — это модель, которая может редактировать отдельное изображение с помощью текстовой подсказки и референсного изображения.  
  
Вызывать можно как через API, так и через Сервисы > Редактор изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"

Закрыть

  

### AI Transform – трансформация изображений

  

**Модели для частных задач трансформации изображений**.   
Можно использовать через меню Сервисы > Текстовый фоторедактор (для зарегистрированных пользователей) или по API.

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| AI Transform - удаление текста [?](#mar420taskfull) img2img-aitransform/text-removal  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена стиля изображения [?](#mar419taskfull) img2img-aitransform/style-transfer  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - профессиональное фото [?](#mar418taskfull) img2img-aitransform/professional-photo  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена соотношения сторон [?](#mar417taskfull) img2img-aitransform/reframe  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - плюшевый стиль [?](#mar416taskfull) img2img-aitransform/plushie-style  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - восстановление фото [?](#mar415taskfull) img2img-aitransform/photo-restoration  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - удаление объектов [?](#mar414taskfull) img2img-aitransform/object-removal  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена прически [?](#mar413taskfull) img2img-aitransform/hair-change  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - ретушь лица [?](#mar412taskfull) img2img-aitransform/face-enhancement  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена выражения лица [?](#mar411taskfull) img2img-aitransform/expression-change  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - автоматическая цветокоррекция [?](#mar410taskfull) img2img-aitransform/auto-color  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - трансформация в мультфильм [?](#mar409taskfull) img2img-aitransform/cartoonify  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена фона [?](#mar408taskfull) img2img-aitransform/background-change  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |
| AI Transform - смена сцены [?](#mar407taskfull) img2img-aitransform/scene-composition  Профессиональный (не Тестовый) редактирование изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 10 июл 25 | нет |

X

### AI Transform - удаление текста

Удалите весь текст и надписи с изображений, сохраняя при этом фон и естественный вид.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена стиля изображения

Превратите ваши фотографии в художественные шедевры, вдохновленные знаменитыми стилями  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - профессиональное фото

Превратите свои обычные фотографии в потрясающие профессиональные студийные портреты с идеальным освещением и стилем.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена соотношения сторон

Трансформирует с помощью ИИ исходное изображение в новое, с нужным соотношением сторон (например: квадратное в прямоугольное горизонтальное, или вертикальное)  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - плюшевый стиль

Превратите свои фотографии в крутые плюшевые игрушки, сохранив при этом сходство с оригинальными персонажами  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - восстановление фото

Восстанавливайте и улучшайте старые или поврежденные фотографии, устраняя дефекты и добавляя цвет, сохраняя при этом оригинальный характер и детали изображения.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - удаление объектов

Удаляйте нежелательные объекты или людей с ваших фотографий.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена прически

Экспериментируйте с различными прическами, от лысой головы до любого стиля, который вы можете представить, сохраняя при этом естественное освещение и реалистичные результаты.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - ретушь лица

Улучшайте черты лица с помощью профессиональной ретуши, сохраняя при этом естественный, реалистичный вид  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена выражения лица

Изменяйте выражения лица на фотографиях на любые желаемые эмоции — от улыбок до серьёзных взглядов.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - автоматическая цветокоррекция

Улучшите свои фотографии с помощью профессиональной цветокоррекции, сбалансированных тонов и ярких, но естественных цветов  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - трансформация в мультфильм

Превратите свои фотографии в яркий стиль мультфильма.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена фона

Замените фон вашей фотографии на любую желаемую сцену — от закатов на пляже до городских пейзажей — с идеальным освещением и тенями  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### AI Transform - смена сцены

Поместите ваш объект в любую воображаемую сцену, от зачарованных лесов до городских пейзажей, с профессиональной композицией и освещением  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Старые новости по подключенным моделям

Источник: https://vsegpt.ru/Docs/Models/OldNews

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Старые новости по подключенным моделям

  

[2025 г](#h120-2)

[2024 г](#h120-3)

[2023 г](#h120-4)

  

## 2025 г

  

- **18 ноября, Gemini 3.0 Pro Preview** от Google, в течение 3 часов после публикации.
- **14 ноября, GPT-5.1** от OpenAI.
- **6 ноября, Kimi K2 Thinking** – в течение 2 часов после публикации. Опенсорс модель уровня GPT-5, согласно метрикам.
- **4 ноября, Kling 2.5**. Топовая модель генерации видео.
- **4 ноября, Sora 2** от OpenAI. Топовая модель генерации видео.
- **31 октября, Veo 3.1 Fast** от Google. Топовая модель генерации видео.
- **31 октября, Minimax M2** от Minimax. Топовая опенсорс модель.
- **22 октября, Grok 4 Fast** от xAI. Модель уровня GPT-5, но значительно быстрее и дешевле.
- **22 октября, GPT 5 Pro** от OpenAI. Самая дорогая и топовая модель.
- **16 октября, Haiku 4.5** – обновленная модель от Anthropic. По метрикам сопоставима с более старой Sonnet 4, но дешевле её практически в 5 раз!
- **29 сентября, Sonnet 4.5** – обновленная модель от Anthropic
- **29 сентября, DeepSeek Chat 3.2 Exp** – обновленная модель от DeepSeek со значительным понижением стоимости генерации
- **22 сентября, DeepSeek Chat 3.1 Terminus** – обновленная модель от DeepSeek
- **11 сентября, Seedream 4.0 + Seedream 4.0 Edit Multi References** – топовые модели генерации и редактирования изображений от Bytedance. Seedream 4.0 Edit Multi References хорошо справляется с примеркой одежды на модель.
- **28 августа, Grok Code Fast 1 от xAI** – топовая дешевая модель работы с кодом
- **26 августа, Flash Image 2.5 + Flash Image 2.5 Edit** – топовые модели генерации и редактирования изображений от Google.
- **22 августа, DeepSeek Chat 3.1 и DeepSeek Chat 3.1 Thinking** – обновленные модели от DeepSeek
- **13 августа, Claude Sonnet 4 на 1 миллион контекста** – подключили специальную точку, на которой доступен расширенный контекст до 1 миллиона токенов.
- **7 августа, OpenAI GPT-5 Nano, Mini и Chat** – новые модели стали доступны в течение 3 часов после запуска!
- **7 августа, OpenAI GPT OSS 120B и 20B** – модели доступны, в том числе в быстром варианте (скорость генерации 500–600 токенов в секунду!)
- **7 августа, Claude Opus 4.1** – улучшенный вариант Opus 4.1. Доступен в режиме «с размышлениями» и «без размышлений».
- **16 июля, Google отключила preview-версии Gemini 2.5 Flash**. Мы сделали перенаправление в релизную версию 2.5 Fllash, но а) не везде, б) она дороже. Если вы пользовались этими моделями – поправьте свои настройки!
- **15 июля, Llama 4 Scout на 10М контекста** – уже вышедшая Scout, но с поставщиком, поддерживающим крупнейший в мире контекст этой модели – 10М токенов! Обычно книгу можно уложить в 1М токенов, так что тут модель может обработать целых 10 книг!
- **12 июля, Kimi K2** – топовая китайская опенсорс модель размером в 1Т, которая соперничает с лучшими сетями типа Sonnet 4, OpenAI o3 по значительно более низкой цене
- **10 июля, AI Transform** – 14(!) нейросетей для разнообразных операций с изображениями: восстановление, смена стиля, смена фона, трансформация в профессиональное фото...
- **10 июля, Grok 4** – самая свежая модель от xAI Илона Маска. Согласно бенчмаркам, обгоняет o3, Opus 4, Gemini 2.5 Pro.
- **2 июля, Imagen 4 Fast, Imagen 4 Ultra** – топовые модели генерации изображений от Google
- **17 июня, Gemini Pro 2.5, Flash 2.5** – официальный выход 2.5 моделей от Google
- **10 июня, OpenAI o3** – цены **снижены на 80%** вслед за OpenAI!
- **5 июня, Gemini Pro 2.5 Preview** – обновление топовой модели от Google
- **2 июня, FLUX.1 Kontext Pro/Max** – топовая нейросеть для генерации и редактирования изображений. Поддерживает: генерацию по тексту, редактирование изображения, генерацию по нескольким изображениям/референсам
- **22 мая, Claude Sonnet 4 и Opus 4 от Anthropic** – модели стали доступны в течение 2 часов после запуска!
- **20 мая, Gemini Flash 2.5 Preview 05 20**. Вышла на презентации Google IO, мы подключили в течение пары часов :)
- **17 мая, LTX 0.9.7, генерация Image-To-Video и Text-to-Video**, быстрая и дешевая
- **16 мая, ряд нейросетей для редактирования изображений** – Recraft Edit, Recraft Upscale, Colorization, Ideogram V3 Replace Background, Ideogram V3 Edit
- **8 мая, Mistral Medium 3**
- **2 мая, модели генерации изображений Ideogram V3 и Recraft V3** (У Recraft V3 более 30 стилей генерации!)
- **29 апреля, модели Qwen 3 от Alibaba**
- **18 апреля, Gemini Flash 2.5 от Google**
- **16 апреля, o4-mini от OpenAI** – модели стали доступны в течение 1.5 часов после запуска!
- **14 апреля, GPT 4.1 от OpenAI** – модели стали доступны в течение 1.5 часов после запуска!
- **7 апреля, Google Flash Edit** – модель, позволяющая редактировать изображения по простому текстовому запросу.
- **6 апреля, Gemini Pro 2.5 Preview** – топ 1 модель по оценкам пользователей! Поддержка 1 млн токенов контекста!
- **6 апреля, LLama 4 Scout и Maverick**
- **30 марта, PDF OCR 1.0** – модель для распознавания PDF в текст, включая графические PDF. Поддерживает PDF до 1000 страниц.
- **26 марта, gpt-4o-mini-transcribe и gpt-4o-transcribe от OpenAI** – новые модели распознавания речи-в-текст.
- **22 марта, gpt-4o-mini-tts от OpenAI** – новая качественная модель озвучки с возможностью задавать характер.
- **19 марта, 7 новых vision-моделей** – т.е. моделей для запросов по изображениям. Flash 2.0, Sonnet 3.7 в vision-вариантах, Mistral 24B, Gemma 27B, Qwen 2.5 72B, Qwen VL Plus, Qwen VL Max.
- **10 марта – 4 research модели поверх Sonnet 3.7** – Online High Quality, Deep Online, Research, Deep Research для формирования полноценных исследований на 8–9 страниц A4! [Подробнее о Research-моделях + примеры](https://vsegpt.ru/ExtTools/Research "Ext Tools / Research")
- **28 февраля, GPT-4.5 Preview от OpenAI** уже доступна!
- **26 февраля, Sonnet 3.7 c размышлениями** доступна! Поддерживается 3 варианта модели, предлагающие разный бюджет на размышления: low, medium (по умолчанию), high. Модели полностью совместимы с обычным OpenAI API, доработок не требуется.
- **25 февраля, новая Sonnet 3.7** – новая Sonnet 3.7 уже доступна на сервисе!
- **14 февраля, версии модели OpenAI: o3-mini** – o3-mini-high с предустановленным пресетом глубоких размышлений, и o3-mini-online с возможностью поиска в Интернете.
- **5 февраля, Google Gemini Flash 2.0** – новая модель от Google!
- **1 февраля, o3-mini от OpenAI** уже доступна! (Также модель **o1** возвращена на сервис после долгого отключения)
- **1 февраля, Qwen Turbo, Plus, Max** – доступны свежие модели от Alibaba group! Max по метрикам превосходят другие модели, включая западные (кроме рассуждающих)
- **29 января, Deepseek R1 от Perplexity** – R1 с онлайн-поиском информации!
- **28 января, альтернативные провайдеры для Deepseek R1 и V3** – поскольку оригинальный DeepSeek сейчас находится под нагрузкой.
- **25 января, серия online-моделей** – теперь целый ряд моделей могут отвечать с учетом интернет-поиска, т.е. текущих данных. Доступны в онлайн-варианте: GPT-4o-mini, GPT-4o, Sonnet/Haiku 3.5, Google Pro 1.5, Llama 3.3, EVA Qwen 72B.
- **20 января, подключена Deepseek R1** – топовая рассуждающая модель от Deepseek, по метрикам сравнимая с o1, но по цене дешевле, чем o1-mini; она также быстрее o1 и o1-mini.
- **8 января, Kling Standart 1.6, Kling Pro V1.6** – топовые модели для генерации видео от Kling.

  

## 2024 г

  

- **29 декабря, подключена Minimax Music** – модель генерации песен по тексту и аудио референсу
- **26 декабря, подключена Deepseek V3** – топовая модель от Deepseek, около 600B параметров, сравнима по метрикам с GPT-4o и Sonnet 3.5... и еще у неё крайне низкая цена!
- **18 декабря, модель o1 от OpenAI** подключена в течение суток после выхода!
- **9 декабря, Kling Standart, Kling Pro V1.5, Haiper 2.0** – подключили модели для генерации видео по тексту и изображению, включая одного из мировых лидеров Kling Pro 1.5
- **8 декабря, LLama 3.3 70B** подключена в течение двух суток после выхода!
- **6 декабря, серия новых моделей от Amazon с большим контекстным окном до 300 000**
- **26 ноября, новая модель OpenAI: GPT-4o (2024–11–20)**
- **19 ноября, Mistral Large 2411** – подключили обновление модели Mistral Large.
- **5 ноября, новая Haiku 3.5** – самая последняя модель от Anthropic, сравнима с версией Sonnet 3.5 от июня 2024.
- **22 октября, новая Sonnet 3.5** – новая Sonnet 3.5 уже доступна на сервисе!
- **13 октября, Grok Beta от xAI** – модель от xAI, компании Илона Маска, который пытается конкурировать с OpenAI
- **7 октября, Google Gemini Flash-8B** – новые модели от Google.
- **4 октября, FLUX pro 1.1** – лучшая мировая модель на текущий момент для генерации изображений уже у нас!
- **26 сентября, серия LLama 3.2** подключена в течение суток после выхода!
- **25 сентября, Google Gemini Pro 002 и Gemini Flash 002** – новые модели от Google.
- **13 сентября, OpenAI o1-mini и o1-preview** – новая модель от OpenAI подключена в течение суток!
- **28 августа, FLUX schnell, dev и pro** – топовые модели генерации изображений серии FLUX доступны у нас. FLUX pro даже обходит Midjourney на Арене генерирующих картинки моделей.
- **28 августа, новые опенсорс модели** – Hermes 405B (один из немногих файнтюнов Llama 3.1 405B), Mistral Nemo 12B Starcannon, Llama 3.1 Euryale 70B v2.2
- **22 августа, Webapp AI Generator** – выкатили ИИ-генератор веб-приложений по текстовому описанию с возможностью просмотра результата (аналог Artifacts). Доступно в «Интеграциях».
- **14 августа, OpenAI: GPT-4o-latest** – последняя сеть от OpenAI. Под ней OpenAI будет постоянно публиковать все новые и более совершенные релизы GPT-4o
- **14 августа, OpenAI: GPT-4o-64k-output** – версия GPT-4o, позволяющая генерировать расширенные результаты, вплоть до 64 000 токенов. Временно недоступна обычным подписчикам OpenAI, только специальным тестерам – а у нас доступна :)
- **14 августа, Google Flash** – значительно снижены цены вслед за Google
- **7 августа, OpenAI: GPT-4o 2024–08–06** – последняя модель GPT-4o, с пониженной ценой и поддержкой структурированного выхода JSON (мы уже поддерживаем структурный выход по схеме)
- **25 июля, Mistral Large 2** – последняя модель от Mistral (вышла 24 июля)
- **23 июля, Llama 3.1 405B Instruct** – доступна у нас, в течение 1.5 часов после официального релиза. (также доступны LLama 3.1 8B и 70B)
- **19 июля, 10 новых опенсорс моделей** – в серии Open Models Fan, предназначенной для поддержки доступа к опенсорс моделям (теперь на всех платных тарифных планах).
- **18 июля, OpenAI: GPT-4o mini** – в 22:00, спустя 2 часа после официального запуска, модель уже доступна!
- **17 июля, Google Gemma 2 27B** – новая опенсорс модель от Google. Очень неплохо общается на русском.
- **12 июля, Playground 2.5** – опенсорс модель для генерации изображений уровня DALLE-3 (согласно рейтингу ЭЛО text-to-image моделей), но в пять раз дешевле DALLE-3.
- **12 июля, Magnum 72B** – топовая опенсорсная модель для ролевого взаимодействия
- **30 июня, Stable Diffusion XL** – подключили классическую опенсорс модель генерации изображений.
- **28 июня, Google Gemma 2 9B** – новая опенсорс модель от Google. Очень неплохо общается на русском.
- **25 июня, NVIDIA Nemotron 4 340B Instruct** – крупнейшая опенсорс модель на настоящий момент. Первая опенсорс модель, которая переводит по метрикам лучше Google Translate и DeepL.
- **20 июня, Anthropic: Claude 3.5 Sonnet** – новая топовая модель; по метрикам превосходит GPT-4o и предыдущий топовый Claude 3 Opus
- **14 июня, OpenAI: TTS** – добавили модели для генерации речи по тексту от OpenAI
- **7 июня, Qwen2 72B Instruct** – новая опенсорс модель из серии Qwen от Tongyi Qianwen (Alibaba group, Китай), сравнимая с LLama3 70B
- **25 мая, Microsoft: Phi 3 Medium** – самая старшая из серии Phi 3 моделей. Хорошая тренировка, 128 000 контекст.
- **15 мая, Google: Gemini Flash 1.5** – с презентации Google IO от 14 мая. 1 миллион контекста и очень дешевая обработка.
- **13 мая, OpenAI: GPT-4o** – самая свежая и сильная модель от OpenAI уже на сервисе! (подключили в течение часа после выхода)
- **11 мая, Qwen 1.5 14B/32B/72B/110B** – опенсорс модели от Tongyi Qianwen (Alibaba group, Китай)
- **6 мая, Lumimaid 8B** – опенсорс модель для ролевого взаимодействия (файнтюн Llama3 8B)
- **26 апреля, FireLLaVA 13B** – опенсорс модель для вопросов по изображениям
- **19 апреля, Llama3 8B/70B** – новейшие опенсорс модели серии Llama.
- **18 апреля, MicrosoftAI: WizardLM-2 7B** – файнтюн 7B-модели от MicrosoftAI.
- **18 апреля, Mistral: Mixtral 8x22B Instruct** – официальная дотренировка от Mistral их модели на выполнение инструкций.
- **16 апреля, MicrosoftAI: WizardLM-2 8x22B** – мощный опенсорсный файнтюн для Mixtral 8x22B, по метрикам сопоставим с GPT-4.
- **11 апреля, Mistral: Mixtral 8x22B** – запустили самую последнюю опенсорс модель от Mistral.
- **10 апреля, OpenAI: GPT-4-Turbo** – последний вариант GPT-4-Turbo от 9 апреля
- **10 апреля, Google: Gemini Pro 1.5** на 1 миллион контекста
- **5 апреля, Cohere** – Command R и Command R+ – общие сети с контекстом 128 000, фокусирующиеся на RAG и обработке вызова функций (function calling) и tools
- **20 марта, OpenAI** – подключили Whisper – сеть для распознавания аудио (Speech-To-Text)
- **14 марта, Anthropic** – добавили Claude 3 Haiku. Очень дешевая модель с возможностью общаться на русском и гигантским контекстом в 200К токенов!
- **13 марта, OpenAI** – подключили новые embeddings: text-embedding-3-small, text-embedding-3-large
- **8 марта, Mistral** – перенесли запуск Mixtral 8x7B Instruct на API от Groq с их уникальными ускоряющими процессорами. Скорость выросла где-то в 5 раз.
- **4 марта, Anthropic** – выпустила Claude 3. По оценкам разработчиков модель Sonnet быстрее, дешевле и лучше Claude 2, а Opus даже превосходит GPT-4.
- **27 февраля, Mistral, закрытые модели** – добавили Mistral Large. По оценкам разработчиков она находится на уровне между Claude 2 и GPT-4. Модель в первую очередь предназначена для европейских языков, на русском работает, но похуже.
- **27 февраля, Perplexity** – Sonar Online Models, модели с доступом в интернет, которые умеют отвечать по актуальным фактам
- **26 февраля, Translate-модели** – значительно улучшили скорость и качество при долгих диалогах за счет внутреннего сервиса кэша и обратного кэша.
- **25 февраля, Google** – Gemini Pro и Gemini Pro Vision подешевели на 30%. У Gemini Pro Vision самая низкая цена на обработку изображений – около 4 копеек за 1 изображение!
- **23 февраля, Google Gemma 7B** – добавлена новая опенсорс модель от Google.
- **21 февраля, Dall-E 2 и 3** – добавили text-to-image модели на сервис.
- **17 февраля, Anthropic** – Claude Instant подешевел на 50%.
- **2 февраля, OpenAI** – новая, более дешевая ChatGPT (цена на входные токены уменьшена на 50%, на выходные – на 25%)
- **1 февраля, CodeLlama70B** – новая опенсорс 70B модель для генерации кода
- **26 января, OpenAI** – новая GPT-4-Turbo
- **19 января, Google: Gemini Pro Vision** – мощная модель от Google, позволяющая обрабатывать изображения.
- **15 января, Mistral, закрытые модели** – подключили модели, доступные по API. Флагманская Mistral Medium конкурирует с Claude 2.

## 2023 г

  

- **13 декабря, Google: Gemini Pro** – новая мощная модель от Google.
- **11 декабря, Mistral** – Mixtral 8x7B Instruct, Mixtral 8x7B Chat, опенсорс модели на новой архитектуре. Дешевые и сравнимые по качеству с ChatGPT (по оценкам авторов)
- **29 ноября, Perplexity** – Perplexity Online Models с доступом к интернету для более точного следования фактам
- **21 ноября, Anthropic** – Claude 2.1 с 200к контекста!
- **6 ноября, OpenAI** – GPT-3.5 Turbo 16k (11–06), GPT-4 Turbo на 128к контекста.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Speech-To-Text-модели (распознавание речи) - Whisper, gpt-4o-transcribe

Источник: https://vsegpt.ru/Docs/Models/STT

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Speech-To-Text-модели (распознавание речи)

  

**Предназначены для распознавания речи**.   
   
**Временные особенности:**

- Токен = 1 секунде; приведена цена за 1000 токенов. Округление секунд идет в большую сторону.
- Пример вызова по API есть в [Документации API](https://vsegpt.ru/Docs/API "Docs / API").
- Также есть клиент для тестирования распознавания – доступен на странице Инструменты либо через меню.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Deepgram: Nova 3 (с диаризацией, бета-тест) [?](#mar697taskfull) stt-deepgram/nova-3-diarize  1.80 р за минуту | 30.00 | 0.00 | 2000 | 8 мая | нет |
| OpenAI: Whisper (новый провайдер с 8 мая 2026) (с диаризацией, бета-тест) [?](#mar696taskfull) stt-openai/whisper-1-diarize  1.80 р за минуту | 30.00 | 0.00 | 2000 | 28 июн 24 | нет |
| Deepgram: Nova 3 [?](#mar669taskfull) stt-deepgram/nova-3  1.20 р за минуту | 20.00 | 0.00 | 2000 | 8 мая | нет |
| OpenAI: gpt-4o-transcribe [?](#mar310taskfull) stt-openai/gpt-4o-transcribe  Профессиональный 1.92 р за минуту | 32.00 | 0.00 | 2000 | 26 мар 25 | нет |
| OpenAI: gpt-4o-mini-transcribe [?](#mar308taskfull) stt-openai/gpt-4o-mini-transcribe  0.96 р за минуту | 16.00 | 0.00 | 2000 | 22 мар 25 | нет |
| OpenAI: Whisper (новый сторонний провайдер с 8 мая 2026) [?](#mar86taskfull) stt-openai/whisper-1  1.20 р за минуту | 20.00 | 0.00 | 2000 | 28 июн 24 | нет |

X

### Deepgram: Nova 3 (с диаризацией, бета-тест)

Одна из новейших моделей распознавания аудио от DeepGram, которая значительно лучше Whisper.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Поддерживает:  
- response\_format = text, json (обычный текст)  
- response\_format = verbose\_json (расширенный формат ответа с деталями, но, возможно, несовместимый с OpenAI)  
  
Поддерживает диаризацию - т.е. распознавание спикеров (кому какая распознанная часть речи принадлежит). Полезно для анализа записей разговоров и пр.  
  
ВАЖНО: требует корректного указания language="ru" при запросе; иначе выдает многоязычный текст.  
  
ВАЖНО: детали диаризации поддерживаются только в verbose\_json, вам придется собирать их в коде самостоятельно.

Закрыть

X

### OpenAI: Whisper (новый провайдер с 8 мая 2026) (с диаризацией, бета-тест)

Распознавание речи с помощью Whisper.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Важно: обращение идет не к OpenAI, а к стороннему хостеру модели.   
Хостер обновлен 8 мая 2026, и поддерживает  
- response\_format = text, json (обычный текст)  
- response\_format = verbose\_json (расширенный формат ответа с деталями, но, возможно, несовместимый с OpenAI)  
  
Поддерживает диаризацию - т.е. распознавание спикеров (кому какая распознанная часть речи принадлежит). Полезно для анализа записей разговоров и пр.  
  
ВАЖНО: детали диаризации поддерживаются только в verbose\_json, вам придется собирать их в коде самостоятельно.

Закрыть

X

### Deepgram: Nova 3

Одна из новейших моделей распознавания аудио от DeepGram, которая значительно лучше Whisper.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Поддерживает:  
- response\_format = text, json (обычный текст)  
- response\_format = verbose\_json (расширенный формат ответа с деталями, но, возможно, несовместимый с OpenAI)  
  
ВАЖНО:  
Требует корректного указания language="ru" при запросе; иначе выдает многоязычный текст.

Закрыть

X

### OpenAI: gpt-4o-transcribe

Распознавание речи с помощью gpt-4o-transcribe.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Важно: нужно корректно передавать имя файла (например, userfile.mp3) в запросе, иначе возможны ошибки.

Закрыть

X

### OpenAI: gpt-4o-mini-transcribe

Распознавание речи с помощью gpt-4o-mini-transcribe.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Важно: нужно корректно передавать имя файла (например, userfile.mp3) в запросе, иначе возможны ошибки.

Закрыть

X

### OpenAI: Whisper (новый сторонний провайдер с 8 мая 2026)

Распознавание речи с помощью Whisper.  
Тарификация идет посекундно; цена указана за 1000 секунд и измеряется при входе.  
  
Важно: обращение идет не к OpenAI, а к стороннему хостеру модели.   
Хостер обновлен 8 мая 2026, и поддерживает  
- response\_format = text, json (обычный текст)  
- response\_format = verbose\_json (расширенный формат ответа с деталями, но, возможно, несовместимый с OpenAI)

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Text-to-Audio-модели (генерация музыки) - Google Lyria 2, Stable Audio

Источник: https://vsegpt.ru/Docs/Models/TTA

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Text-to-Audio-модели (генерация музыки)

  

**Предназначены для генерации музыки по текстовому запросу**.   
   
Пример генерации для [Cassete Music Generator](https://vsegpt.ru/videos/mp3/cassete_music_generator.mp3)  
Пример генерации для [Google Lyria 2](https://vsegpt.ru/videos/mp3/Lyria_2_70_BPM_ambient_piano_relax_music.wav) запрос 70 BPM, ambient piano relax music  

- Пример вызова по API есть в [Документации API](https://vsegpt.ru/Docs/API "Docs / API").
- Также есть клиент для тестирования генерации – доступен на странице Инструменты либо через меню.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Google Lyria 2 (генерация музыки) [?](#mar370taskfull) tta-google/lyria2  Профессиональный За вызов: 20.0 р. генерация музыки 20 руб/генерация | 0.0 | 0.0 | 2048 | 21 мая 25 | нет |
| Cassete Music Generator (генерация музыки) [?](#mar317taskfull) tta-cassette/music-generator  Профессиональный генерация музыки 6 руб/минута | 6000.0 | 0.0 | 2048 | 1 апр 25 | нет |
| Stable Audio (генерация музыки) [?](#mar185taskfull) tta-stable/stable-audio  Профессиональный За вызов: 5.00 р. генерация музыки 5 руб/генерация | 0.0 | 0.0 | 2048 | 28 авг 24 | нет |

X

### Google Lyria 2 (генерация музыки)

Модель предназначена для генерации музыки (30 секунд).  
  
Поддерживает параметр "negative\_prompt", показывающий, чего НЕ должно быть в музыке.  
  
Рекомендуется распространенный промт, например: "A lush, ambient soundscape featuring the serene sounds of a flowing river, complemented by the distant chirping of birds, and a gentle, melancholic piano melody that slowly unfolds."

Закрыть

X

### Cassete Music Generator (генерация музыки)

Модель предназначена для генерации музыки.   
  
При биллинге идет округление с точностью до минуты; во входе учитывается число полных минут.  
  
Максимальный размер генерации - 3 минуты.  
  
Лучше всего работает с большим промтом, например:  
"Soothing piano composition with gentle flowing arpeggios and light melodic phrases. The piece should evoke a sense of peaceful contemplation, with soft dynamics and occasional delicate harmonies. Include moments of silence to enhance the calming atmosphere. Key: F Major, Tempo: 68 BPM. Imagine waves gently caressing a shore at sunset, with a warm, intimate recording quality that captures the natural resonance of the piano."

Закрыть

X

### Stable Audio (генерация музыки)

Модель предназначена для генерации музыки.   
  
Допустимое время от 10 до 40 секунд.

Закрыть

  

## Text-to-Song-модели (генерация песен, бета-тест)

  

**Предназначены для генерации песен по текстовому запросу и референсу**.   
   
**Особенности:**

- При вызове генерации стоимость списывается сразу, но запрос ставится в очередь. К сожалению, он может не выполнится, а деньги будут списаны – пока это часть рисков использования модели. Мы будем отслеживать такие ситуации.
- Среднее время генерации – около 1–2 минут на ролик в Minimax Music.
- Вам нужно будет проверять готовность ролика специальными запросами к API
- Готовые файлы будут доступны в течение 2 часов (пока)

   
Примеры генерации:   

- [Пример 1](https://vsegpt.ru/pdfs/generated_dozhd_pesnya.mp3)

   

- Есть клиент для тестирования генерации – доступен через меню Сервисы.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || Minimax Music (генерация песни по тексту и аудиореференсу, временно отключена) [?](#mar243taskfull) txt2sng-minimax/music  Профессиональный (не Тестовый) За вызов: 10.0 р. генерация песен | 0.0 | 0.0 | 2000 | 29 дек 24 | нет |

X

### Minimax Music (генерация песни по тексту и аудиореференсу, временно отключена)

Создавайте музыку на основе текстовых запросов с помощью модели MiniMax, которая использует передовые технологии искусственного интеллекта для создания качественных и разнообразных музыкальных композиций.

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Text-to-Speech-модели (генерация речи) - OpenAI TTS, Vosk TTS

Источник: https://vsegpt.ru/Docs/Models/TTS

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Text-to-Speech-модели (генерация речи)

  

**Предназначены для генерации речи по тексту**.   
Условия использования моделей OpenAI: вы обязаны явно декларировать, что используете голос ИИ.  
   
**Временные особенности:**

- Не поддерживают стриминг
- Пример вызова по API есть в [Документации API](https://vsegpt.ru/Docs/API "Docs / API").
- Также есть клиент для тестирования генерации – доступен на странице Инструменты либо через меню.
- [Примеры настроек для gpt-4o-mini для задания инструкций, в каком стиле генерировать озвучку](https://vsegpt.ru/Docs/API/gpt4ominitts "Docs / API / gpt 4 ominitts")

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || OpenAI: gpt-4o-mini-tts (с поддержкой стриминга) [?](#mar584taskfull) tts-openai/gpt-4o-mini-tts-stream  Профессиональный (не Тестовый) рекомендуется настройка интонаций для чтения текста | 11.0 | 0.0 | 4096 | 29 янв | да |
| Vosk TTS 0.7 (очень быстрый) [?](#mar331taskfull) tts-vosk/ru-0.7 | 1.5 | 0.0 | 1000 | 12 апр 25 | нет |
| OpenAI: gpt-4o-mini-tts [?](#mar307taskfull) tts-openai/gpt-4o-mini-tts  Базовый и выше (не Тестовый) рекомендуется настройка интонаций для чтения текста | 7.5 | 0.0 | 4096 | 22 мар 25 | да |
| OpenAI: TTS-1-HD [?](#mar130taskfull) tts-openai/tts-1-hd  Профессиональный | 6.4 | 0.0 | 4096 | 14 июн 24 | да |
| OpenAI: TTS-1 [?](#mar129taskfull) tts-openai/tts-1 | 3.2 | 0.0 | 4096 | 14 июн 24 | нет |

X

### OpenAI: gpt-4o-mini-tts (с поддержкой стриминга)

Модель OpenAI: gpt-4o-mini-tts - изначальная версия от 22 марта 2025.  
Эта версия поддерживает стриминг ответа для уменьшения латентности (паузы между запросом и ответом)  
  
Это последняя модель от OpenAI, поддерживающая задания интонаций при чтении текста.  
Примеры: https://vsegpt.ru/Docs/API/gpt4ominitts  
  
Поддерживаемые голоса: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse  
Поддерживаемые response\_format: mp3, opus, aac, flac, wav, pcm

Закрыть

X

### Vosk TTS 0.7 (очень быстрый)

Модель VOSK TTS для генерации речи.  
  
Поддерживаемые голоса: 0, 1, 2, 3, 4 (строки) (3 женщины и 2 мужчин. Также допускается голос "nova" - он будет преобразован в 2)  
  
Поддерживаемые response\_format: wav  
  
Максимум - 1000 символов за раз.   
Поддерживается только русский язык, все другие символы должны быть предварительно сконвертированы в русскую речь.

Закрыть

X

### OpenAI: gpt-4o-mini-tts

Модель OpenAI: gpt-4o-mini-tts  
  
Последняя модель от OpenAI, поддерживающая задания интонаций при чтении текста.  
Примеры: https://vsegpt.ru/Docs/API/gpt4ominitts  
  
Поддерживаемые голоса: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse  
Поддерживаемые response\_format: mp3, opus, aac, flac, wav, pcm

Закрыть

X

### OpenAI: TTS-1-HD

Модель OpenAI: TTS HD  
  
Поддерживаемые голоса: alloy, echo, fable, onyx, nova, shimmer  
Поддерживаемые response\_format: mp3, opus, aac, flac, wav, pcm

Закрыть

X

### OpenAI: TTS-1

Модель OpenAI: TTS-1  
  
Поддерживаемые голоса: alloy, echo, fable, onyx, nova, shimmer  
Поддерживаемые response\_format: mp3, opus, aac, flac, wav, pcm

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Модели генерации изображений - FLUX 2, Google Nano Banana Pro...

Источник: https://vsegpt.ru/Docs/Models/Txt2Img

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Text-to-image (генерация изображений по тексту)

### OpenAI Dall-E

  

**Модели для генерации изображений по тексту**.   
**Доступны только для платных пользователей тарифа Базовый+GPT4 – на тестовом тарифе не доступны!**  
Стоимость: Dall-E 2 от 3 р. 10 к., Dall-E 3 от 7 р. 76 к. – подробнее стоимости генерации при разном разрешении и качестве по кнопке “?"  
Особенности показа: каждый символ стоит 1 копейку, в статистике генерируется число входных символов в соответствии с прайсом.  
   
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/file.gif)Отчет: сравнение моделей генерации изображений](https://vsegpt.ru/pdfs/Image_models.pdf)  
   
Для ознакомления с возможностями Dalle-3 рекомендуем статью от OpenAI [![](https://vsegpt.ru/themes/bs5vsegpt/icons/web.gif)Что нового в Dalle-3](https://cookbook.openai.com/articles/what_is_new_with_dalle_3 "Внешняя ссылка (откроется в новом окне)")

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| OpenAI: Dall-E 3 [?](#mar70taskfull) openai/dall-e-3  Профессиональный (не Тестовый) генерация изображений | 10.0 | 0.0 | 4096 | 13 мар 24 | нет |

X

### OpenAI: Dall-E 3

Флагманская модель для генерации изображений от OpenAI  
  
Цены за 1 изображение:  
Качество standard:  
- 1024x1024 - 7 р. 76 к.  
- 1024x1792 - 15 р. 52 к.  
- 1792x1024 - 15 р. 52 к.  
  
Качество hd:  
- 1024x1024 - 15 р. 52 к.  
- 1024x1792 - 23 р. 28 к.  
- 1792x1024 - 23 р. 28 к.

Закрыть

  

### Другие модели (FLUX 2, Google Nano Banana Pro...)

  

**Модели для генерации изображений по тексту**.   
**Доступны только для платных пользователей тарифа Базовый+GPT4 – на тестовом тарифе не доступны!**  
Подробнее о стоимости генерации при разном разрешении и качестве по кнопке “?", там же описание дополнительных параметров, доступных при вызове модели.  
Особенности показа: каждый символ стоит 1 копейку, в статистике генерируется число входных символов в соответствии с прайсом.  
   
[![](https://vsegpt.ru/themes/bs5vsegpt/icons/file.gif)Отчет: сравнение моделей генерации изображений](https://vsegpt.ru/pdfs/Image_models.pdf)

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| OpenAI: GPT-5.4 Image 2 (ChatGPT Images 2.0) [?](#mar659taskfull) img-openai/gpt-image-2  Профессиональный (не Тестовый) топ от 22 апреля отличная типографика 3.5 / 18 / 60 р. за изображение | 10.0 | 0.0 | 2000 | 22 апр | нет |
| Google Nano Banana 2 (Flash Image 3.1) [?](#mar611taskfull) img-google/nano-banana-2  Профессиональный (не Тестовый) с поддержкой русского текста генерация изображений 19.9 р. за изображение | 19.9 | 0.0 | 2000 | 27 фев | нет |
| Flux 2 [klein] 9B Base [?](#mar579taskfull) img-flux/flux-2-klein-9b  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 4.9 / 9.9 р. за 1 изображение | 10.0 | 0.0 | 2000 | 15 янв | да |
| Flux 2 [klein] 4B [?](#mar577taskfull) img-flux/flux-2-klein-4b  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 3.9 р. за 1 изображение | 3.9 | 0.0 | 2000 | 15 янв | нет |
| ByteDance Seedream 4.5, Text-to-Image [?](#mar558taskfull) img-bytedance/seedream-v4.5  Профессиональный (не Тестовый) конкурент Nano Banana Pro с поддержкой русского текста 13.9 р. за изображение | 13.9 | 0.0 | 2000 | 8 дек 25 | да |
| FLUX 2 Pro [?](#mar553taskfull) img-flux/flux-2-pro  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 9 р. за 1 изображение | 10.0 | 0.0 | 2000 | 26 ноя 25 | нет |
| FLUX 2 [?](#mar552taskfull) img-flux/flux-2  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 3.6 р. за 1 изображение | 10.0 | 0.0 | 2000 | 26 ноя 25 | нет |
| FLUX 2 (flex) [?](#mar550taskfull) img-flux/flux-2-flex  Базовый и выше (не Тестовый) с поддержкой русского текста генерация изображений 18/36 р. за 1 изображение | 10.0 | 0.0 | 2000 | 26 ноя 25 | нет |
| Google Nano Banana Pro (Gemini Image Pro 3 Preview), Text-to-Image [?](#mar546taskfull) img-google/nano-banana-pro  Профессиональный (не Тестовый) топ с поддержкой русского текста генерация изображений 29.9 р. за изображение | 29.9 | 0.0 | 2000 | 20 ноя 25 | да |
| Reve [?](#mar506taskfull) img-reve  Профессиональный (не Тестовый) генерация изображений 8.9 р. за изображение | 8.9 | 0.0 | 2000 | 24 окт 25 | нет |
| GPT Image 1 mini [?](#mar504taskfull) img-openai/gpt-image-1-mini  Профессиональный (не Тестовый) генерация изображений 5.0 р. за изображение | 5.0 | 0.0 | 2000 | 24 окт 25 | нет |
| ByteDance Seedream 4.0 [?](#mar471taskfull) img-bytedance/seedream-v4  Базовый и выше (не Тестовый) генерация изображений 6.9 р. за 1 изображение | 6.9 | 0.0 | 2000 | 11 сен 25 | нет |
| Google Flash Image 2.5 (Nano Banana) [?](#mar456taskfull) img-google/flash-25  Профессиональный (не Тестовый) генерация изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 26 авг 25 | нет |
| Juggernaut Lightning Flux (крайне быстрая генерация изображений FLUX) [?](#mar430taskfull) img-flux/juggernaut-lightning  Базовый и выше (не Тестовый) генерация изображений 1.80 р. за 1 изображение | 10.0 | 0.0 | 2000 | 17 июл 25 | нет |
| Stable Diffusion XL Lightning (быстрая генерация SDXL) [?](#mar429taskfull) img-stable/stable-diffusion-xl-lightning  Базовый и выше (не Тестовый) генерация изображений 0.30 р. за 1 изображение | 10.0 | 0.0 | 2000 | 17 июл 25 | нет |
| Google Imagen 4 Ultra (preview) [?](#mar405taskfull) img-google/imagen4-preview-ultra  Профессиональный (не Тестовый) генерация изображений 20 р. за изображение | 20.0 | 0.0 | 2000 | 2 июл 25 | нет |
| Google Imagen 4 Fast (preview) [?](#mar404taskfull) img-google/imagen4-preview-fast  Профессиональный (не Тестовый) генерация изображений 5.9 р. за изображение | 5.9 | 0.0 | 2000 | 2 июл 25 | нет |
| FLUX.1 Kontext [max] [?](#mar387taskfull) img-flux/kontext-max  Профессиональный (не Тестовый) генерация изображений 15.0 р. за изображение | 15.0 | 0.0 | 2000 | 2 июн 25 | нет |
| FLUX.1 Kontext [pro] [?](#mar386taskfull) img-flux/kontext-pro  Профессиональный (не Тестовый) генерация изображений 7.5 р. за изображение | 7.5 | 0.0 | 2000 | 2 июн 25 | нет |
| Google Imagen 4 (preview) [?](#mar369taskfull) img-google/imagen4-preview  Профессиональный (не Тестовый) генерация изображений 11.9 р. за изображение | 11.9 | 0.0 | 2000 | 21 мая 25 | нет |
| Recraft V3 (более 30 стилей для изображений!) [?](#mar352taskfull) img-recraft/v3  Профессиональный (не Тестовый) генерация изображений 9.9 р. за изображение | 9.9 | 0.0 | 2000 | 2 мая 25 | нет |
| Ideogram V3 [?](#mar351taskfull) img-ideogram/v3  Профессиональный (не Тестовый) генерация изображений 7.9 р. за изображение | 10.0 | 0.0 | 2000 | 2 мая 25 | нет |
| FLUX.1.1 [pro] [?](#mar206taskfull) img-flux/pro1.1  Профессиональный (не Тестовый) генерация изображений 14.9 р. за изображение | 10.0 | 0.0 | 2000 | 4 окт 24 | нет |
| FLUX.1 [pro] [?](#mar188taskfull) img-flux/pro  Профессиональный (не Тестовый) генерация изображений 14.9 р. за изображение | 10.0 | 0.0 | 2000 | 28 авг 24 | нет |
| FLUX.1 [dev] [?](#mar187taskfull) img-flux/dev  Профессиональный (не Тестовый) генерация изображений 7.5 р. за изображение | 10.0 | 0.0 | 2000 | 28 авг 24 | нет |
| FLUX.1 [schnell] [?](#mar186taskfull) img-flux/schnell  Профессиональный (не Тестовый) генерация изображений 1.8 р. за изображение | 10.0 | 0.0 | 2048 | 28 авг 24 | нет |
| Dummy Image [?](#mar71taskfull) img-dummy/image  За вызов: 0.005 р. | 0.00 | 0.00 | 4096 | 13 мар 24 | нет |

X

### OpenAI: GPT-5.4 Image 2 (ChatGPT Images 2.0)

Стоимость за генерацию зависит от качества:  
- low: 3.5 р.  
- medium: 18 р. (по умолчанию)  
- high: 60 р.  
  
Модель поддерживает разрешения (выбирайте их вручную в выпадающем списке!):  
- 1024x1024  
- 1024x768, 768x1024  
- 1280x720, 720x1280  
  
(Если вам ОЧЕНЬ нужны дополнительные разрешения для данной модели, пожалуйста, обратитесь в техподдержку)  
  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Google Nano Banana 2 (Flash Image 3.1)

Топовая модель от Google для генерации изображений.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Flux 2 [klein] 9B Base

Генерация изображений из текста с помощью FLUX.2 klein 9B от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает разрешения по цене в 4.9 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 9.9 р / генерация  
  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Flux 2 [klein] 4B

Генерация изображений из текста с помощью FLUX.2 klein 4B от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Любые размеры изображений, вплоть до 4К.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения по цене в 18 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 36 р / генерация  
  
Подробное описание возможностей:  
  
- Управление цветовым кодом HEX  
Указывайте точные цвета с помощью HEX-кодов для точного подбора цвета и соблюдения фирменного стиля. Для достижения наилучших результатов используйте ключевое слово "color" или "hex" перед кодом.  
  
Например:   
  
"a wall painted in color #2ECC71"  
"gradient from hex #FF6B6B to hex #4ECDC4"  
"the car in color #1A1A1A with accents in #FFD700"  
  
- Ссылки на изображения с помощью @  
  
Ссылайтесь на загруженные изображения непосредственно в промптах, используя символ @ для интуитивной работы с несколькими изображениями.  
  
Например:   
"@image1 wearing the outfit from @image2"  
"combine the style of @image1 with the composition of @image2"  
"the person from @image1 in the setting from @image3"  
  
- JSON-промт  
  
Для точного контроля над сложной генерацией используйте структурированные JSON промпты вместо естественного языка. JSON промптинг обеспечивает детальную спецификацию элементов сцены, объектов, настроек камеры и композиции.  
  
Basic JSON structure:  
{  
"scene": "Overall setting description",  
"subjects": [  
{  
"type": "Subject category",  
"description": "Physical attributes and details",  
"pose": "Action or stance",  
"position": "foreground/midground/background"  
}  
],  
"style": "Artistic rendering approach",  
"color\_palette": ["color1", "color2", "color3"],  
"lighting": "Lighting conditions and direction",  
"mood": "Emotional atmosphere",  
"composition": "rule of thirds/centered/dynamic diagonal",  
"camera": {  
"angle": "eye level/low angle/high angle",  
"distance": "close-up/medium shot/wide shot",  
"lens": "35mm/50mm/85mm"  
}  
}

Закрыть

X

### ByteDance Seedream 4.5, Text-to-Image

Топовая модель с поддержкой русского текста на картинках.   
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json".  
  
Соотношение сторон задается автоматически, но вы можете задать его в текстовом промте добавив фразу типа следующей: "The image has a 4:3 aspect ratio"

Закрыть

X

### FLUX 2 Pro

Генерация изображений из текста с помощью FLUX.2 Pro от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения по цене в 9 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 18 р / генерация  
  
Подробное описание возможностей:  
  
- Управление цветовым кодом HEX  
Указывайте точные цвета с помощью HEX-кодов для точного подбора цвета и соблюдения фирменного стиля. Для достижения наилучших результатов используйте ключевое слово "color" или "hex" перед кодом.  
  
Например:   
  
"a wall painted in color #2ECC71"  
"gradient from hex #FF6B6B to hex #4ECDC4"  
"the car in color #1A1A1A with accents in #FFD700"  
  
- Ссылки на изображения с помощью @  
  
Ссылайтесь на загруженные изображения непосредственно в промптах, используя символ @ для интуитивной работы с несколькими изображениями.  
  
Например:   
"@image1 wearing the outfit from @image2"  
"combine the style of @image1 with the composition of @image2"  
"the person from @image1 in the setting from @image3"  
  
- JSON-промт  
  
Для точного контроля над сложной генерацией используйте структурированные JSON промпты вместо естественного языка. JSON промптинг обеспечивает детальную спецификацию элементов сцены, объектов, настроек камеры и композиции.  
  
Basic JSON structure:  
{  
"scene": "Overall setting description",  
"subjects": [  
{  
"type": "Subject category",  
"description": "Physical attributes and details",  
"pose": "Action or stance",  
"position": "foreground/midground/background"  
}  
],  
"style": "Artistic rendering approach",  
"color\_palette": ["color1", "color2", "color3"],  
"lighting": "Lighting conditions and direction",  
"mood": "Emotional atmosphere",  
"composition": "rule of thirds/centered/dynamic diagonal",  
"camera": {  
"angle": "eye level/low angle/high angle",  
"distance": "close-up/medium shot/wide shot",  
"lens": "35mm/50mm/85mm"  
}  
}

Закрыть

X

### FLUX 2

Генерация изображений из текста с помощью FLUX.2 от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения по цене в 3.6 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 7.2 р / генерация  
  
Подробное описание возможностей:  
  
- Управление цветовым кодом HEX  
Указывайте точные цвета с помощью HEX-кодов для точного подбора цвета и соблюдения фирменного стиля. Для достижения наилучших результатов используйте ключевое слово "color" или "hex" перед кодом.  
  
Например:   
  
"a wall painted in color #2ECC71"  
"gradient from hex #FF6B6B to hex #4ECDC4"  
"the car in color #1A1A1A with accents in #FFD700"  
  
- Ссылки на изображения с помощью @  
  
Ссылайтесь на загруженные изображения непосредственно в промптах, используя символ @ для интуитивной работы с несколькими изображениями.  
  
Например:   
"@image1 wearing the outfit from @image2"  
"combine the style of @image1 with the composition of @image2"  
"the person from @image1 in the setting from @image3"  
  
- JSON-промт  
  
Для точного контроля над сложной генерацией используйте структурированные JSON промпты вместо естественного языка. JSON промптинг обеспечивает детальную спецификацию элементов сцены, объектов, настроек камеры и композиции.  
  
Basic JSON structure:  
{  
"scene": "Overall setting description",  
"subjects": [  
{  
"type": "Subject category",  
"description": "Physical attributes and details",  
"pose": "Action or stance",  
"position": "foreground/midground/background"  
}  
],  
"style": "Artistic rendering approach",  
"color\_palette": ["color1", "color2", "color3"],  
"lighting": "Lighting conditions and direction",  
"mood": "Emotional atmosphere",  
"composition": "rule of thirds/centered/dynamic diagonal",  
"camera": {  
"angle": "eye level/low angle/high angle",  
"distance": "close-up/medium shot/wide shot",  
"lens": "35mm/50mm/85mm"  
}  
}

Закрыть

X

### FLUX 2 (flex)

Генерация изображений из текста с помощью FLUX.2 [flex] от Black Forest Labs. Улучшенные возможности типографики и рендеринга текста.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения по цене в 18 р / генерация  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
а также  
- 1920x1080, 1080x1920 - по цене в 36 р / генерация  
  
Подробное описание возможностей:  
  
- Управление цветовым кодом HEX  
Указывайте точные цвета с помощью HEX-кодов для точного подбора цвета и соблюдения фирменного стиля. Для достижения наилучших результатов используйте ключевое слово "color" или "hex" перед кодом.  
  
Например:   
  
"a wall painted in color #2ECC71"  
"gradient from hex #FF6B6B to hex #4ECDC4"  
"the car in color #1A1A1A with accents in #FFD700"  
  
- Ссылки на изображения с помощью @  
  
Ссылайтесь на загруженные изображения непосредственно в промптах, используя символ @ для интуитивной работы с несколькими изображениями.  
  
Например:   
"@image1 wearing the outfit from @image2"  
"combine the style of @image1 with the composition of @image2"  
"the person from @image1 in the setting from @image3"  
  
- JSON-промт  
  
Для точного контроля над сложной генерацией используйте структурированные JSON промпты вместо естественного языка. JSON промптинг обеспечивает детальную спецификацию элементов сцены, объектов, настроек камеры и композиции.  
  
Basic JSON structure:  
{  
"scene": "Overall setting description",  
"subjects": [  
{  
"type": "Subject category",  
"description": "Physical attributes and details",  
"pose": "Action or stance",  
"position": "foreground/midground/background"  
}  
],  
"style": "Artistic rendering approach",  
"color\_palette": ["color1", "color2", "color3"],  
"lighting": "Lighting conditions and direction",  
"mood": "Emotional atmosphere",  
"composition": "rule of thirds/centered/dynamic diagonal",  
"camera": {  
"angle": "eye level/low angle/high angle",  
"distance": "close-up/medium shot/wide shot",  
"lens": "35mm/50mm/85mm"  
}  
}

Закрыть

X

### Google Nano Banana Pro (Gemini Image Pro 3 Preview), Text-to-Image

Топовая модель с поддержкой русского текста на картинках.   
Поддерживает установку соотношения сторон финальной картинки - не забывайте настроить это в интерфейсе.   
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Reve

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### GPT Image 1 mini

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")

Закрыть

X

### ByteDance Seedream 4.0

Новая модель создания изображений от ByteDance, Seedream 4.0  
Нативное разрешение 1280x1280.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Google Flash Image 2.5 (Nano Banana)

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
Поддерживает параметр aspect\_ratio:str = "1:1", "16:9" и т.д.

Закрыть

X

### Juggernaut Lightning Flux (крайне быстрая генерация изображений FLUX)

Практически моментальная генерация изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536

Закрыть

X

### Stable Diffusion XL Lightning (быстрая генерация SDXL)

Практически моментальная генерация изображений  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
Поддерживает опцию output\_format:str = "jpeg" | "png" (по умолчанию "jpeg")  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)  
  
Модель поддерживает разрешения  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536

Закрыть

X

### Google Imagen 4 Ultra (preview)

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
Модели надо передавать aspect\_ratio="1:1" (или другие значения) вместо size при запросе.  
  
Модель неплохо работает с текстом на русском языке, но если использовать буквы в нижнем регистре, например, в таком промте: "Здание в середине современного города с надписью "библиотека". Фотореалистичный стиль."

Закрыть

X

### Google Imagen 4 Fast (preview)

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
Модели надо передавать aspect\_ratio="1:1" (или другие значения) вместо size при запросе.

Закрыть

X

### FLUX.1 Kontext [max]

FLUX.1 Kontext [max] text-to-image - это новая премиум-модель, обеспечивающая максимальную производительность во всех аспектах с значительно улучшенным следованием промпту.  
  
Модель поддерживает aspect\_ratio вместо передачи ширины и высоты.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 Kontext [pro]

Модель FLUX.1 Kontext [pro] для преобразования текста в изображение обеспечивает современные результаты генерации изображений с беспрецедентным следованием запросам, фотореалистичным рендерингом и безупречной типографикой.  
  
Модель поддерживает aspect\_ratio вместо передачи ширины и высоты.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Google Imagen 4 (preview)

Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
Модели надо передавать aspect\_ratio="1:1" (или другие значения) вместо size при запросе.

Закрыть

X

### Recraft V3 (более 30 стилей для изображений!)

Стоимость за генерацию - 9.90 р.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Ideogram V3

Стоимость за генерацию зависит от качества:  
- TURBO: 7.90 р.  
- BALANCED: 14.90 р.  
- QUALITY: 19.90 р.  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1.1 [pro]

14.9 рублей за генерацию  
  
Модель поддерживает разрешения  
- 512x512  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 [pro]

14.9 рублей за генерацию  
  
Модель поддерживает разрешения  
- 512x512  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 [dev]

4.0 рублей за 512x512  
7.5 рублей за остальные разрешения  
  
Модель поддерживает разрешения  
- 512x512  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
Модель поддерживает дополнительные параметры в body\_json:  
- "guidance\_scale" (по умолчанию 3.5)  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### FLUX.1 [schnell]

0.9 рублей за 512x512  
1.8 рублей за остальные разрешения  
  
Модель поддерживает разрешения  
- 512x512  
- 1024x1024  
- 1152x896  
- 896x1152  
- 1216x832  
- 832x1216  
- 1344x768  
- 768x1344  
- 1536x640  
- 640x1536  
  
Модель поддерживает ТОЛЬКО response\_format="b64\_json"  
  
С цензурой - если запрос не проходит safety\_check, будет возвращен черный квадрат. По вопросам отключения напишите на support (пока не поддерживается)

Закрыть

X

### Dummy Image

Модель, предназначенная для тестирования API.  
Возвращает простой рисунок с запросом и выбранным размером.  
  
Поддерживает response\_format="url" и response\_format="b64\_json"

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Вспомогательные модели (конвертация документов PDF, DOCX в текст)

Источник: https://vsegpt.ru/Docs/Models/Utils

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Utils, вспомогательные модели (конвертация документов PDF, DOCX в текст)

  

**Предназначены для решения ряда дополнительных задач на сервисе.**.   

- utils/extract-text работает хорошо с текстовыми документами
- utils/pdf-ocr работает со всеми PDF-документами, применяя к ним оптическое распознавание

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || PDF OCR (распознавание PDF-файлов любого типа, до 1000 страниц) [?](#mar312taskfull) utils/pdf-ocr-1.0  Профессиональный (не Тестовый) За вызов: 0.10 р. конвертация документов 0.55 р за страницу | 0.0 | 55.0 | 2000 | 30 мар 25 | нет |
| Extract Text (конвертация файлов DOCX, PDF в текст) [?](#mar277taskfull) utils/extract-text-1.0  За вызов: 0.50 р. конвертация документов | 0.0 | 0.0 | 2000 | 16 фев 25 | нет |

X

### PDF OCR (распознавание PDF-файлов любого типа, до 1000 страниц)

Вызов позволяет конвертировать файлы PDF в текст через API.  
  
(Ввиду сложности процесса мы не гарантируем точность результатов в 100% случаев)  
  
Пример вызова доступен на странице документации API или через меню Сервисы > PDF OCR  
  
Ответ будет содержать текст в формате Markdown.  
В дополнительных полях будет текст по страницам, картинки и пр.  
  
Стоимость считается постранично; число страниц будет доступно как число выходных токенов \* 10.

Закрыть

X

### Extract Text (конвертация файлов DOCX, PDF в текст)

Вызов позволяет конвертировать файлы DOCX, PDF в текст через API.  
  
(Ввиду сложности процесса мы не гарантируем точность результатов в 100% случаев)  
  
Пример вызова доступен на странице документации API.

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Модели генерации видео - Kling, Sora 2, Veo 3.1, LTX ...

Источник: https://vsegpt.ru/Docs/Models/Video

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

[Генерация видео](#h216-1)

[Text-to-Video-модели (генерация видео, бета-тест)](#h216-2)

[Image-to-Video-модели (генерация видео, бета-тест)](#h216-3)

  

## Генерация видео

### Text-to-Video-модели (генерация видео, бета-тест)

  

**Предназначены для генерации видео по текстовому запросу**.   
   
**Особенности:**

- При вызове генерации стоимость списывается сразу, но запрос ставится в очередь. К сожалению, он может не выполнится, а деньги будут списаны – пока это часть рисков использования модели. Мы будем отслеживать такие ситуации.
- Среднее время генерации – около 3 минут на ролик в Kling, 1–2 минуты для LTX Video 0.9.5
- Вам нужно будет проверять готовность ролика специальными запросами к API
- Готовые файлы будут доступны в течение 2 часов (пока)

   
Примеры генерации видео:   

- Kling Pro V1.6 [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/kling_pro16_img_vsegpt_kosmos.mp4)
- Kling Standart 1.6 [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/kling_standart16_panda_on_river.mp4), [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/kling_standart16_img_vsegpt_kosmos.mp4)
- Kling Pro V1.5 [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/kling_pro15_panda_on_river.mp4), [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/kling_pro15_img_vsegpt_kosmos.mp4)
- Kling Standart [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/kling_standart_panda_on_river.mp4), [Panda playing guitar in Paris 9:16](https://vsegpt.ru/videos/txt2vid/kling_standart_panda_in_paris.mp4), [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/kling_standart_img_vsegpt_kosmos.mp4)
- Haiper 2.0 [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/haiper20_panda_on_river.mp4), [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/haiper20_img_vsegpt_kosmos.mp4)
- LTX Video 0.9.5 [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/ltx_095_panda_on_river.mp4)
- LTX Video 0.9.7 Distilled [Panda playing guitar on river 16:9](https://vsegpt.ru/videos/txt2vid/ltx_097_panda_on_river2.mp4) [VseGPT в космосе, генерация по картинке 1:1](https://vsegpt.ru/videos/txt2vid/ltx_097_img_vsegpt_kosmos.mp4)

  
   

- Пример вызова по API есть в [Документации API](https://vsegpt.ru/Docs/API "Docs / API").
- Также есть клиент для тестирования генерации – доступен на странице Инструменты либо через меню.

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || LTX 2.3 (Pro, Text-to-Video, 6-20s, с аудио) [?](#mar627taskfull) txt2vid-ltx/pro-2.3-xsec-with-audio  Профессиональный (не Тестовый) 15 р. за секунду | 15.0 | 0.0 | 2000 | 10 мар | нет |
| LTX 2.3 Fast (Text-to-Video, 6-20s, с аудио) [?](#mar626taskfull) txt2vid-ltx/fast-2.3-xsec-with-audio  Профессиональный (не Тестовый) 10 р. за секунду | 10.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Standart (Text-to-Video, 3-15s, с аудио) [?](#mar621taskfull) txt2vid-kling/o3-standart-xsec-with-audio  Профессиональный (не Тестовый) топ по цена/качество 28 р. за секунду | 28.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Standart (Text-to-Video, 3-15s) [?](#mar620taskfull) txt2vid-kling/o3-standart-xsec  Профессиональный (не Тестовый) топ по цена/качество 19.9 р. за секунду | 19.9 | 0.0 | 2000 | 10 мар | нет |
| Kling Pro Turbo 2.5 (Text-to-Video, 5s) [?](#mar529taskfull) txt2vid-kling/pro25-turbo  Профессиональный (не Тестовый) За вызов: 89.9 р. топ по цена/качество | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 (With audio, 8s) [?](#mar524taskfull) txt2vid-openai/sora-2-audio-8s  Профессиональный (не Тестовый) За вызов: 198.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 (With audio, 4s) [?](#mar523taskfull) txt2vid-openai/sora-2-audio  Профессиональный (не Тестовый) За вызов: 99.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Google Veo 3.1 Fast (With audio) [?](#mar515taskfull) txt2vid-google/veo3.1-fast-with-audio  Профессиональный (не Тестовый) За вызов: 149.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Google Veo 3.1 Fast (No audio) [?](#mar514taskfull) txt2vid-google/veo3.1-fast-no-audio  Профессиональный (не Тестовый) За вызов: 99.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Kling Master Text-to-Video v2.1 [?](#mar476taskfull) txt2vid-kling/master21  Профессиональный (не Тестовый) За вызов: 299.9 р. топ | 0.0 | 0.0 | 2000 | 11 сен 25 | нет |
| LTX 0.9.7 Text-to-Video (быстрая) [?](#mar364taskfull) txt2vid-ltx/097-distilled  За вызов: 12.0 р. | 0.0 | 0.0 | 2000 | 17 мая 25 | нет |
| LTX 0.9.5 Text-to-Video [?](#mar294taskfull) txt2vid-ltx/video-095  За вызов: 12.0 р. | 0.0 | 0.0 | 2000 | 14 мар 25 | нет |
| Kling Pro V1.6 Text-to-Video (ВРЕМЕННО НЕДОСТУПНА) [?](#mar246taskfull) txt2vid-kling/pro16  Профессиональный (не Тестовый) За вызов: 149.9 р. | 0.0 | 0.0 | 2000 | 8 янв 25 | нет |
| Kling Standart Text-to-Video v1.6 [?](#mar244taskfull) txt2vid-kling/standart16  Профессиональный (не Тестовый) За вызов: 49.9 р. | 0.0 | 0.0 | 2000 | 8 янв 25 | нет |
| Kling Pro V1.5 Text-to-Video [?](#mar230taskfull) txt2vid-kling/pro15  Профессиональный (не Тестовый) За вызов: 149.9 р. | 0.0 | 0.0 | 2000 | 9 дек 24 | нет |
| Kling Standart Text-to-Video [?](#mar228taskfull) txt2vid-kling/standart  Профессиональный (не Тестовый) За вызов: 49.9 р. | 0.0 | 0.0 | 2000 | 8 дек 24 | нет |

X

### LTX 2.3 (Pro, Text-to-Video, 6-20s, с аудио)

Модель LTX 2.3 (Pro) для генерации видео по тексту.  
  
Длительность сгенерированного видео - от 6 до 20 секунд, только четные значения.  
Поддерживает соотношения сторон: 16:9, 9:16.  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### LTX 2.3 Fast (Text-to-Video, 6-20s, с аудио)

Модель LTX 2.3 Fast для генерации видео по тексту.  
  
Длительность сгенерированного видео - от 6 до 20 секунд, только четные значения.  
Поддерживает соотношения сторон: 16:9, 9:16.  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Kling O3 Standart (Text-to-Video, 3-15s, с аудио)

Модель Kling O3 Standart для генерации видео по тексту.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
Поддерживает соотношения сторон: 16:9, 9:16, 1:1  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling O3 Standart (Text-to-Video, 3-15s)

Модель Kling O3 Standart для генерации видео по тексту.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
Поддерживает соотношения сторон: 16:9, 9:16, 1:1  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling Pro Turbo 2.5 (Text-to-Video, 5s)

Модель Kling Pro Turbo 2.5 для генерации видео по тексту.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживает соотношения сторон: 16:9, 9:16, 1:1  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### OpenAI: Sora 2 (With audio, 8s)

Sora 2 от OpenAI!  
  
Длительность сгенерированного видео - 8 секунд.  
  
**Минимальный баланс для вызова модели: 200р.**

Закрыть

X

### OpenAI: Sora 2 (With audio, 4s)

Sora 2 от OpenAI!  
  
Длительность сгенерированного видео - 4 секунды.  
  
**Минимальный баланс для вызова модели: 100р.**

Закрыть

X

### Google Veo 3.1 Fast (With audio)

Более быстрая и экономичная версия Google Veo 3.1!  
Также генерирует аудио (более дорогая).  
  
Длительность сгенерированного видео - 4 секунды.  
  
**Минимальный баланс для вызова модели: 150р.**

Закрыть

X

### Google Veo 3.1 Fast (No audio)

Более быстрая и экономичная версия Google Veo 3.1!  
  
Длительность сгенерированного видео - 4 секунды.  
  
**Минимальный баланс для вызова модели: 100р.**

Закрыть

X

### Kling Master Text-to-Video v2.1

Модель Kling Master 2.1 для генерации видео по тексту.  
  
Длительность сгенерированного видео - 5 секунд.  
Время генерации - около 4 минут.  
  
**Минимальный баланс для вызова модели: 300р.**

Закрыть

X

### LTX 0.9.7 Text-to-Video (быстрая)

Модель LTX Video-0.9.7 13B Distilled для генерации видео.  
  
Длительность сгенерированного видео - 4 секунды.  
Поддерживаются соотношения сторон 16:9, 9:16  
Время генерации - до 1 минуты при отсутствии очереди.  
  
  
**Минимальный баланс для вызова модели: 20р.**

Закрыть

X

### LTX 0.9.5 Text-to-Video

Модель LTX Video 0.9.5 для генерации видео.  
  
Длительность сгенерированного видео - 4 секунды.  
Поддерживаются соотношения сторон 16:9, 9:16  
Время генерации - около 2 минут.  
  
  
**Минимальный баланс для вызова модели: 20р.**

Закрыть

X

### Kling Pro V1.6 Text-to-Video (ВРЕМЕННО НЕДОСТУПНА)

Модель Kling Pro V1.6 для генерации видео.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

X

### Kling Standart Text-to-Video v1.6

Модель Kling Standart 1.6 для генерации видео.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Kling Pro V1.5 Text-to-Video

Модель Kling Pro V1.5 для генерации видео.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

X

### Kling Standart Text-to-Video

Модель Kling Standart для генерации видео.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.  
  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

  

### Image-to-Video-модели (генерация видео, бета-тест)

  

**Предназначены для генерации видео по текстовому запросу и изображения**.   
   
Условия аналогичны text-to-video

  

Модель и ID | Руб за 1000 символов входных данных | Руб за 1000 символов генерации модели | Размер конте кста | Дата обнов ления | Авто моде ра ция || LTX 2.3 (Pro, Image-to-Video, 6-20s, с аудио, опционально указание последнего кадра) [?](#mar628taskfull) img2vid-ltx/pro-2.3-xsec-with-audio  Профессиональный (не Тестовый) 15 р. за секунду | 15.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Pro (Image-to-Video, 3-15s, с аудио, опциональный последний кадр) [?](#mar625taskfull) img2vid-kling/o3-pro-xsec-with-audio  Профессиональный (не Тестовый) 38.0 р. за секунду | 38.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Pro (Image-to-Video, 3-15s, опциональный последний кадр) [?](#mar624taskfull) img2vid-kling/o3-pro-xsec  Профессиональный (не Тестовый) 28.0 р. за секунду | 28.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Standart (Image-to-Video, 3-15s, с аудио, опциональный последний кадр) [?](#mar623taskfull) img2vid-kling/o3-standart-xsec-with-audio  Профессиональный (не Тестовый) топ по цена/качество 28.0 р. за секунду | 28.0 | 0.0 | 2000 | 10 мар | нет |
| Kling O3 Standart (Image-to-Video, 3-15s, опциональный последний кадр) [?](#mar622taskfull) img2vid-kling/o3-standart-xsec  Профессиональный (не Тестовый) топ по цена/качество 19.9 р. за секунду | 19.9 | 0.0 | 2000 | 10 мар | нет |
| Kling Standart Turbo 2.5 (Image-to-Video, 10s) [?](#mar533taskfull) img2vid-kling/standart25-turbo-10s  Профессиональный (не Тестовый) За вызов: 99.0 р. топ по цена/качество | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Kling Standart Turbo 2.5 (Image-to-Video, 5s) [?](#mar532taskfull) img2vid-kling/standart25-turbo  Профессиональный (не Тестовый) За вызов: 49.9 р. топ по цена/качество | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Kling Pro Turbo 2.5 (Image-to-Video, 10s) [?](#mar531taskfull) img2vid-kling/pro25-turbo-10s  Профессиональный (не Тестовый) За вызов: 179.9 р. топ по цена/качество | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Kling Pro Turbo 2.5 (Image-to-Video, 5s) [?](#mar530taskfull) img2vid-kling/pro25-turbo  Профессиональный (не Тестовый) За вызов: 89.9 р. топ по цена/качество | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 Pro (Image-to-Video, With audio, 8s) [?](#mar528taskfull) img2vid-openai/sora-2-pro-audio-8s  Профессиональный (не Тестовый) За вызов: 599.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 Pro (Image-to-Video, With audio, 4s) [?](#mar527taskfull) img2vid-openai/sora-2-pro-audio  Профессиональный (не Тестовый) За вызов: 299.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 (Image-to-Video, With audio, 8s) [?](#mar526taskfull) img2vid-openai/sora-2-audio-8s  Профессиональный (не Тестовый) За вызов: 198.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| OpenAI: Sora 2 (Image-to-Video, With audio, 4s) [?](#mar525taskfull) img2vid-openai/sora-2-audio  Профессиональный (не Тестовый) За вызов: 99.0 р. | 0.0 | 0.0 | 2000 | 4 ноя 25 | нет |
| Google Veo 3.1 Fast (указание первого и последнего фрейма видео) (With audio) [?](#mar519taskfull) img2vid-google/veo3.1-fast-first-last-frame-with-audio  Профессиональный (не Тестовый) За вызов: 239.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Google Veo 3.1 Fast (указание первого и последнего фрейма видео) (No audio) [?](#mar518taskfull) img2vid-google/veo3.1-fast-first-last-frame-no-audio  Профессиональный (не Тестовый) За вызов: 159.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Google Veo 3.1 Fast (Image-to-Video) (With audio) [?](#mar517taskfull) img2vid-google/veo3.1-fast-with-audio  Профессиональный (не Тестовый) За вызов: 239.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Google Veo 3.1 Fast (Image-to-Video) (No audio) [?](#mar516taskfull) img2vid-google/veo3.1-fast-no-audio  Профессиональный (не Тестовый) За вызов: 159.0 р. топ | 0.0 | 0.0 | 2000 | 31 окт 25 | нет |
| Kling Master Image-to-Video v2.1 [?](#mar475taskfull) img2vid-kling/master21  Профессиональный (не Тестовый) За вызов: 299.9 р. топ | 0.0 | 0.0 | 2000 | 11 сен 25 | нет |
| Kling Pro Image-to-Video v2.1 [?](#mar474taskfull) img2vid-kling/pro21  Профессиональный (не Тестовый) За вызов: 149.9 р. | 0.0 | 0.0 | 2000 | 11 сен 25 | нет |
| Kling Standart Image-to-Video v2.1 [?](#mar473taskfull) img2vid-kling/standart21  Профессиональный (не Тестовый) За вызов: 59.9 р. | 0.0 | 0.0 | 2000 | 11 сен 25 | нет |
| LTX 0.9.7 Image-To-Video (быстрая) [?](#mar365taskfull) img2vid-ltx/097-distilled  За вызов: 12.0 р. | 0.0 | 0.0 | 2000 | 17 мая 25 | нет |
| LTX 0.9.5 Image-To-Video [?](#mar295taskfull) img2vid-ltx/video-095  За вызов: 12.0 р. | 0.0 | 0.0 | 2000 | 14 мар 25 | нет |
| Kling Pro V1.6 (Image-To-Video) [?](#mar247taskfull) img2vid-kling/pro16  Профессиональный (не Тестовый) За вызов: 149.9 р. | 0.0 | 0.0 | 2000 | 8 янв 25 | нет |
| Kling Standart 1.6 (Image-To-Video) [?](#mar245taskfull) img2vid-kling/standart16  Профессиональный (не Тестовый) За вызов: 49.9 р. | 0.0 | 0.0 | 2000 | 8 янв 25 | нет |
| Kling Pro V1.5 (Image-To-Video) [?](#mar231taskfull) img2vid-kling/pro15  Профессиональный (не Тестовый) За вызов: 149.9 р. | 0.0 | 0.0 | 2000 | 9 дек 24 | нет |
| Kling Standart (Image-To-Video) [?](#mar229taskfull) img2vid-kling/standart  Профессиональный (не Тестовый) За вызов: 49.9 р. | 0.0 | 0.0 | 2000 | 8 дек 24 | нет |

X

### LTX 2.3 (Pro, Image-to-Video, 6-20s, с аудио, опционально указание последнего кадра)

Модель LTX 2.3 (Pro) для генерации видео по изображению.  
  
Длительность сгенерированного видео - от 6 до 20 секунд, только четные значения.  
Поддерживает соотношения сторон: 16:9, 9:16.  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Kling O3 Pro (Image-to-Video, 3-15s, с аудио, опциональный последний кадр)

Модель Kling O3 Pro для генерации видео по изображению. Опционально можно задать последний кадр видео.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling O3 Pro (Image-to-Video, 3-15s, опциональный последний кадр)

Модель Kling O3 Pro для генерации видео по изображению. Опционально можно задать последний кадр видео.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling O3 Standart (Image-to-Video, 3-15s, с аудио, опциональный последний кадр)

Модель Kling O3 Standart для генерации видео по изображению. Опционально можно задать последний кадр видео.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling O3 Standart (Image-to-Video, 3-15s, опциональный последний кадр)

Модель Kling O3 Standart для генерации видео по изображению. Опционально можно задать последний кадр видео.  
  
Длительность сгенерированного видео - от 3 до 15 секунд.  
  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### Kling Standart Turbo 2.5 (Image-to-Video, 10s)

Модель Kling Standart Turbo 2.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 10 секунд.  
  
**Минимальный баланс для вызова модели: 100р.**

Закрыть

X

### Kling Standart Turbo 2.5 (Image-to-Video, 5s)

Модель Kling Standart Turbo 2.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Kling Pro Turbo 2.5 (Image-to-Video, 10s)

Модель Kling Pro Turbo 2.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 10 секунд.  
  
**Минимальный баланс для вызова модели: 180р.**

Закрыть

X

### Kling Pro Turbo 2.5 (Image-to-Video, 5s)

Модель Kling Pro Turbo 2.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
  
**Минимальный баланс для вызова модели: 90р.**

Закрыть

X

### OpenAI: Sora 2 Pro (Image-to-Video, With audio, 8s)

Sora 2 от OpenAI!  
Современная видеомодель от OpenAI, способная создавать детализированные динамичные клипы со звуком.  
  
Длительность сгенерированного видео - 8 секунд.  
  
Поддерживает соотношения сторон: 16:9, 9:16  
  
**Минимальный баланс для вызова модели: 600р.**

Закрыть

X

### OpenAI: Sora 2 Pro (Image-to-Video, With audio, 4s)

Sora 2 от OpenAI!  
Современная видеомодель от OpenAI, способная создавать детализированные динамичные клипы со звуком.  
  
Длительность сгенерированного видео - 4 секунды.  
  
Поддерживает соотношения сторон: 16:9, 9:16  
  
**Минимальный баланс для вызова модели: 300р.**

Закрыть

X

### OpenAI: Sora 2 (Image-to-Video, With audio, 8s)

Sora 2 от OpenAI!  
  
Длительность сгенерированного видео - 8 секунд.  
  
Поддерживает соотношения сторон: 16:9, 9:16  
  
**Минимальный баланс для вызова модели: 200р.**

Закрыть

X

### OpenAI: Sora 2 (Image-to-Video, With audio, 4s)

Sora 2 от OpenAI!  
  
Длительность сгенерированного видео - 4 секунды.  
  
Поддерживает соотношения сторон: 16:9, 9:16  
  
**Минимальный баланс для вызова модели: 100р.**

Закрыть

X

### Google Veo 3.1 Fast (указание первого и последнего фрейма видео) (With audio)

Более быстрая и экономичная версия Google Veo 3.1!   
С поддержкой указания первого и последнего фрейма видео.  
  
Длительность сгенерированного видео - 8 секунд.  
  
**Минимальный баланс для вызова модели: 240р.**

Закрыть

X

### Google Veo 3.1 Fast (указание первого и последнего фрейма видео) (No audio)

Более быстрая и экономичная версия Google Veo 3.1!   
С поддержкой указания первого и последнего фрейма видео.  
  
Длительность сгенерированного видео - 8 секунд.  
  
**Минимальный баланс для вызова модели: 160р.**

Закрыть

X

### Google Veo 3.1 Fast (Image-to-Video) (With audio)

Более быстрая и экономичная версия Google Veo 3.1!  
  
Длительность сгенерированного видео - 8 секунд.  
  
**Минимальный баланс для вызова модели: 160р.**

Закрыть

X

### Google Veo 3.1 Fast (Image-to-Video) (No audio)

Более быстрая и экономичная версия Google Veo 3.1!  
  
Длительность сгенерированного видео - 8 секунд.  
  
**Минимальный баланс для вызова модели: 160р.**

Закрыть

X

### Kling Master Image-to-Video v2.1

Модель Kling Master 2.1 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Время генерации - около 4 минут.  
  
**Минимальный баланс для вызова модели: 300р.**

Закрыть

X

### Kling Pro Image-to-Video v2.1

Модель Kling Pro 2.1 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Время генерации - около 3 минут.  
  
**Минимальный баланс для вызова модели: 150р.**

Закрыть

X

### Kling Standart Image-to-Video v2.1

Модель Kling Standart 2.1 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Время генерации - около 3 минут.  
  
**Минимальный баланс для вызова модели: 60р.**

Закрыть

X

### LTX 0.9.7 Image-To-Video (быстрая)

Модель LTX Video-0.9.7 13B Distilled для генерации видео по изображению.  
  
Длительность сгенерированного видео - 4 секунды.  
Время генерации - до 1 минуты при отсутствии очереди.

Закрыть

X

### LTX 0.9.5 Image-To-Video

Модель LTX Video 0.9.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 4 секунды.  
Поддерживаются соотношения сторон 16:9, 9:16  
Время генерации - около 2 минут.  
  
В отличие от большинства других сетей при генерации картинка будет обрезана до формата 16:9 или 9:16 - т.е. генерация не будет производиться по формату картинки.

Закрыть

X

### Kling Pro V1.6 (Image-To-Video)

Модель Kling Pro V1.6 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

X

### Kling Standart 1.6 (Image-To-Video)

Модель Kling Standart 1.6 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

X

### Kling Pro V1.5 (Image-To-Video)

Модель Kling Pro V1.5 для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

X

### Kling Standart (Image-To-Video)

Модель Kling Standart для генерации видео по изображению.  
  
Длительность сгенерированного видео - 5 секунд.  
Поддерживаются соотношения сторон 16:9, 9:16, 1:1  
Время генерации - около 6 минут.

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Vision-модели (вопросы по изображению, OCR) - Gemini 3 Flash и пр.

Источник: https://vsegpt.ru/Docs/Models/Vision

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

[Модели](https://vsegpt.ru/Docs/Models)[По новизне](https://vsegpt.ru/Docs/ModelsNew)[Документация API](https://vsegpt.ru/Docs/API)[Статистика](https://vsegpt.ru/Docs/Uptime)

    
  

- [Текстовые модели](https://vsegpt.ru/Docs/Models)
- [Генерация изображений](https://vsegpt.ru/Docs/Models/Txt2Img)
- [Редактирование изображений / по референсам](https://vsegpt.ru/Docs/Models/Img2Img)
- [Эмбеддинги (для RAG)](https://vsegpt.ru/Docs/Models/Embeddings)
- [Vision (распознавание изображений, OCR)](https://vsegpt.ru/Docs/Models/Vision)
- [Speech-To-Text (распознавание речи)](https://vsegpt.ru/Docs/Models/STT)
- [Text-to-Speech-модели (генерация речи)](https://vsegpt.ru/Docs/Models/TTS)
- [Text-to-Audio (генерация музыки)](https://vsegpt.ru/Docs/Models/TTA)
- [Генерация видео](https://vsegpt.ru/Docs/Models/Video)
- [Вспомогательные (PDF OCR и пр.)](https://vsegpt.ru/Docs/Models/Utils)

   

## Vision-модели (вопросы по изображению, OCR)

  

**ВАЖНО:** кроме этих моделей, ТАКЖЕ обрабатывают изображения любые модели из [общего списка текстовых моделей](https://vsegpt.ru/Docs/ModelsNew "Docs / Models New"), у которых есть тег   vision . **Данный список УСТАРЕЛ, и мы рекомендуем переходить на новые модели из общего списка.**

  

**Vision-модели предназначены для совместной обработки текста и изображений**.   
   
**Временные особенности:**

- Для запуска любого запроса вам нужно иметь определенный минимум на балансе (нажмите ? чтобы узнать, какой именно минимум, от 5 р. для LLava до 50 р. для GPT-4-Vision)
- **Стоимость приведена «за токен», а не «за символ»**. По результатам запроса провайдером будут переведены ваши изображения в стоимость входных токенов, и за них будет взята плата.
- Токены вычисляются провайдером; мы не комментируем их вычисления и не принимаем по этому поводу претензии.
- Пример вызова по API есть в [Документации API](https://vsegpt.ru/Docs/API "Docs / API"); веб-интерфейс доступен через меню «Сервисы».

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Anthropic: Claude Opus 4.6 (Vision-версия) [?](#mar646taskfull) vis-anthropic/claude-opus-4.6  Профессиональный (не Тестовый) tools structured-outputs | 1.2 | 6.7 | 1000000 | 27 мар | да |
| Anthropic: Claude Sonnet 4.6 (Vision-версия) [?](#mar645taskfull) vis-anthropic/claude-sonnet-4.6  Профессиональный (не Тестовый) tools structured-outputs | 0.8 | 4.0 | 1000000 | 27 мар | да |
| Google: Gemini 3 Flash Preview (Thinking) (Vision) [?](#mar576taskfull) vis-google/gemini-3-flash-pre-thinking  Базовый и выше (не Тестовый) около 0.15 р. за изображение tools structured-outputs | 0.15 | 0.90 | 1000000 | 11 янв | нет |
| Google: Gemini 3 Flash Preview (Vision-версия) [?](#mar575taskfull) vis-google/gemini-3-flash-pre  Базовый и выше (не Тестовый) около 0.15 р. за изображение tools structured-outputs | 0.15 | 0.90 | 1000000 | 11 янв | нет |
| Z.AI: GLM 4.5V (MoE 106B всего, 12B активных) [?](#mar466taskfull) vis-z-ai/glm-4.5v  Профессиональный (не Тестовый) около 0.20 р. за изображение tools | 0.18 | 0.54 | 65000 | 29 авг 25 | нет |
| Mistral: Mistral Medium 3.1 (Vision-версия) [?](#mar465taskfull) vis-mistralai/mistral-medium-3.1  Профессиональный (не Тестовый) около 0.12 р. за изображение tools structured-outputs | 0.12 | 0.60 | 131000 | 29 авг 25 | нет |
| Anthropic: Claude Opus 4.1 (Vision-версия) [?](#mar464taskfull) vis-anthropic/claude-opus-4.1  Профессиональный (не Тестовый) ТОП! около 5 р. за изображение tools | 4.5 | 21.0 | 200000 | 29 авг 25 | да |
| Anthropic: Claude Sonnet 4 (Vision-версия) [?](#mar463taskfull) vis-anthropic/claude-sonnet-4  Профессиональный (не Тестовый) около 1.3 р. за изображение tools | 1.1 | 6.0 | 1000000 | 29 авг 25 | да |
| OpenAI: GPT-5 (Thinking) (Vision-версия) [?](#mar462taskfull) vis-openai/gpt-5  Профессиональный (не Тестовый) топ около 0.30 р. за изображение tools structured-outputs | 0.37 | 3.00 | 400000 | 29 авг 25 | да |
| OpenAI: GPT-5 Thinking Mini (Vision-версия) [?](#mar460taskfull) vis-openai/gpt-5-mini  Профессиональный (не Тестовый) около 0.20 р. за изображение tools structured-outputs | 0.075 | 0.60 | 400000 | 29 авг 25 | да |
| OpenAI: GPT-5 Nano (Vision-версия) [?](#mar459taskfull) vis-openai/gpt-5-nano  Профессиональный (не Тестовый) дешевая и с большим контекстом около 0.07 р. за изображение tools structured-outputs | 0.015 | 0.12 | 400000 | 29 авг 25 | да |
| Google: Gemini 2.5 Pro (vision-версия) [?](#mar428taskfull) vis-google/gemini-2.5-pro  Профессиональный tools structured-outputs | 0.37 | 3.0 | 1000000 | 17 июн 25 | нет |
| Google: Gemini 2.5 Flash (vision-версия) [?](#mar427taskfull) vis-google/gemini-2.5-flash  tools structured-outputs | 0.09 | 0.75 | 1000000 | 17 июн 25 | нет |
| Google: Gemini 2.5 Pro Preview (5 июня, vision-версия) [?](#mar396taskfull) vis-google/gemini-2.5-pro-preview  Профессиональный (не Тестовый) около 0.6 р за изображение tools structured-outputs | 0.37 | 3.0 | 1000000 | 10 июн 25 | нет |
| Google: Gemini 2.5 Flash Preview 05 20 (vision-версия) (с 16 июля перенаправляется в 2.5 Flash) [?](#mar368taskfull) vis-google/gemini-2.5-flash-pre-05-20  дешевая и с большим контекстом около 0.05 р. за изображение tools structured-outputs | 0.045 | 0.15 | 1000000 | 20 мая 25 | нет |
| OpenAI: o4-mini (vision-версия) [?](#mar345taskfull) vis-openai/o4-mini  Профессиональный (не Тестовый) биллинг с учетом размышлений (см. ?) около 0.80 р. за изображение размышления, математика tools structured-outputs | 0.28 | 1.12 | 200000 | 16 апр 25 | да |
| Google: Gemini 2.5 Flash Preview (vision-версия) (с 16 июля перенаправляется в 2.5 Flash) [?](#mar343taskfull) vis-google/gemini-2.5-flash-pre  дешевая и с большим контекстом около 0.05 р. за изображение structured-outputs | 0.045 | 0.15 | 1000000 | 18 апр 25 | нет |
| Llama 4 Scout (быстрая, Vision-версия) [?](#mar324taskfull) vis-meta-llama/llama-4-scout  fast около 0.09-0.20 р за изображение tools | 0.05 | 0.16 | 328000 | 10 апр 25 | нет |
| Llama 4 Maverick (Vision-версия) [?](#mar323taskfull) vis-meta-llama/llama-4-maverick  Профессиональный около 0.14-0.35 р. за изображение tools structured-outputs | 0.06 | 0.24 | 1000000 | 10 апр 25 | нет |
| Gemma 3 27B (опенсорс, vision-версия) [?](#mar301taskfull) vis-google/gemma-3-27b-it  0.04 р. за изображение | 0.07 | 0.16 | 128000 | 19 мар 25 | нет |
| Qwen2.5 VL 72B Instruct [?](#mar297taskfull) vis-qwen/qwen2.5-vl-72b-instruct  Профессиональный За вызов: 0.07 р. топ! около 0.30 р. за изображение | 0.30 | 0.30 | 32768 | 19 мар 25 | нет |
| Qwen2-VL 72B Instruct [?](#mar195taskfull) vis-qwen/qwen-2-vl-72b-instruct  Профессиональный За вызов: 0.07 р. топ! около 0.05 р. за изображение | 0.60 | 0.60 | 32768 | 21 сен 24 | нет |
| OpenAI: GPT-4o (2024-08-06) (vision-версия) [?](#mar173taskfull) vis-openai/gpt-4o-2024-08-06  Профессиональный топ! около 0.15 р. за изображение tools structured-outputs | 0.55 | 2.20 | 128000 | 6 авг 24 | да |
| OpenAI: gpt-4o-mini (vision-версия) vis-openai/gpt-4o-mini  Профессиональный (не Тестовый) около 0.80 р. за изображение | 0.037 | 0.15 | 128000 | 27 июл 24 | да |
| Google: Gemini Flash 1.5 (vision-версия) (выключена, перенаправляется в vis-Flash 2.5) [?](#mar125taskfull) vis-google/gemini-flash-1.5  Профессиональный очень дешевая 0.03 р. за изображение | 0.045 | 0.10 | 1000000 | 14 авг 24 | нет |
| OpenAI: GPT-4o (vision) [?](#mar116taskfull) vis-openai/gpt-4o  Профессиональный топ! | 1.10 | 3.30 | 128000 | 31 мая 24 | да |
| OpenAI: GPT-4 Vision Turbo [?](#mar95taskfull) vis-openai/gpt-4-turbo  Профессиональный топ! около 1.7 р. за 1 изображение | 2.00 | 6.00 | 128000 | 27 апр 24 | да |
| Anthropic: Claude 3 Haiku (vision) [?](#mar85taskfull) vis-anthropic/claude-3-haiku  Профессиональный около 0.1 р за 1 изображение tools | 0.066 | 0.3 | 200000 | 14 мар 24 | да |

X

### Anthropic: Claude Opus 4.6 (Vision-версия)

Anthropic: Claude Opus 4.6 (Vision-версия)  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 200р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4.6 (Vision-версия)

Anthropic: Claude Sonnet 4.6 (Vision-версия)  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 50р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3 Flash Preview (Thinking) (Vision)

Gemini 3 Flash Preview — это высокоскоростная модель, разработанная для агентных рабочих процессов, многоходовых чатов и помощи в программировании. Она обеспечивает рассуждения и производительность использования инструментов почти на уровне Pro при существенно более низкой задержке, чем у более крупных вариантов Gemini, что делает её хорошо подходящей для интерактивной разработки, длительных циклов работы агентов и совместных задач по программированию. По сравнению с Gemini 2.5 Flash она обеспечивает широкие улучшения качества в области рассуждений, мультимодального понимания и надёжности.  
  
Размышляющая версия.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 3 Flash Preview (Vision-версия)

Gemini 3 Flash Preview — это высокоскоростная модель, разработанная для агентных рабочих процессов, многоходовых чатов и помощи в программировании. Она обеспечивает рассуждения и производительность использования инструментов почти на уровне Pro при существенно более низкой задержке, чем у более крупных вариантов Gemini, что делает её хорошо подходящей для интерактивной разработки, длительных циклов работы агентов и совместных задач по программированию. По сравнению с Gemini 2.5 Flash она обеспечивает широкие улучшения качества в области рассуждений, мультимодального понимания и надёжности.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Z.AI: GLM 4.5V (MoE 106B всего, 12B активных)

GLM-4.5V — это мультимодальная фундаментальная модель для приложений с визуально-языковыми агентами. Построенная на архитектуре Mixture-of-Experts (MoE) со 106 млрд параметров и 12 млрд активированных параметров, она достигает передовых результатов в понимании видео, ответах на вопросы по изображениям, оптическом распознавании символов (OCR) и анализе документов, а также демонстрирует значительные улучшения в фронтенд-разработке, определении объектов и пространственном мышлении.  
  
  
Для включения режима "без размышлений" добавьте в промт фразу /nothink  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Mistral: Mistral Medium 3.1 (Vision-версия)

Mistral Medium 3.1 — это обновленная версия Mistral Medium 3, высокопроизводительной языковой модели корпоративного уровня, разработанной для обеспечения передовых возможностей при значительно сниженных операционных затратах. Она сочетает в себе современные возможности рассуждения и мультимодальную производительность с в 8 раз более низкой стоимостью по сравнению с традиционными крупными моделями, что делает её подходящей для масштабируемых развертываний в профессиональных и промышленных сценариях использования.  
  
Модель превосходно работает в таких областях, как программирование, STEM-рассуждения и корпоративная адаптация. Она поддерживает гибридные развертывания, развертывания на собственных серверах и в VPC, и оптимизирована для интеграции в пользовательские рабочие процессы. Mistral Medium 3.1 предлагает конкурентоспособную точность по сравнению с более крупными моделями, такими как Claude Sonnet 3.5/3.7, Llama 4 Maverick и Command R+, при этом сохраняя широкую совместимость в облачных средах.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 10р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Opus 4.1 (Vision-версия)

Claude Opus 4.1 — это обновленная версия флагманской модели Anthropic, предлагающая улучшенную производительность в программировании, рассуждениях и агентных задачах. Она достигает 74,5% на SWE-bench Verified и демонстрирует заметные улучшения в рефакторинге многофайлового кода, точности отладки и детально-ориентированных рассуждениях. Модель поддерживает расширенное мышление до 64К токенов и оптимизирована для задач, включающих исследования, анализ данных и рассуждения с использованием инструментов.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 150р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Anthropic: Claude Sonnet 4 (Vision-версия)

Claude Sonnet 4 значительно расширяет возможности своего предшественника, Sonnet 3.7, превосходя его как в задачах программирования, так и в задачах рассуждения с улучшенной точностью и управляемостью. Достигая передовых результатов на SWE-bench (72,7%), Sonnet 4 балансирует между производительностью и вычислительной эффективностью, что делает его подходящим для широкого спектра приложений: от рутинных задач кодирования до сложных проектов разработки программного обеспечения. Ключевые улучшения включают усовершенствованную автономную навигацию по кодовой базе, сниженное количество ошибок в рабочих процессах, управляемых агентами, и повышенную надежность в следовании сложным инструкциям. Sonnet 4 оптимизирован для практического повседневного использования, обеспечивая продвинутые возможности рассуждения при сохранении эффективности и отзывчивости в различных внутренних и внешних сценариях.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 50р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: GPT-5 (Thinking) (Vision-версия)

GPT-5 — это самая продвинутая модель OpenAI, предлагающая значительные улучшения в рассуждениях, качестве кода и пользовательском опыте.   
Данная версия размышляющая. Как описывают разработчики, можно углубить размышления модели, добавив фразу "think hard about this".  
  
Внимание: на некоторых запросах, которая GPT-5 считает простыми, она сама отключает размышления. К сожалению, это не регулируется.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 30р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Thinking Mini (Vision-версия)

GPT-5 Mini — это компактная версия GPT-5, разработанная для выполнения менее ресурсоемких задач рассуждения. Она обеспечивает те же преимущества в следовании инструкциям и настройке безопасности, что и GPT-5, но с уменьшенной задержкой и стоимостью. GPT-5 Mini является преемником модели o4-mini от OpenAI.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### OpenAI: GPT-5 Nano (Vision-версия)

GPT-5-Nano — это самый маленький и быстрый вариант в системе GPT-5, оптимизированный для инструментов разработчиков, быстрых взаимодействий и сред с ультранизкой задержкой. Хотя он ограничен в глубине рассуждений по сравнению с более крупными аналогами, он сохраняет ключевые функции следования инструкциям и безопасности. Это преемник GPT-4.1-nano и предлагает легковесный вариант для чувствительных к стоимости или работающих в реальном времени приложений.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**  
**Максимальный размер выходной генерации для модели: 128000 токенов**

Закрыть

X

### Google: Gemini 2.5 Pro (vision-версия)

Gemini 2.5 Pro — это передовая ИИ-модель Google, разработанная для решения сложных задач в области рассуждений, программирования, математики и науки. Она использует возможности "мышления", что позволяет ей формулировать ответы с повышенной точностью и учетом нюансов контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Минимальный баланс для вызова модели: 30р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash (vision-версия)

Gemini 2.5 Flash — передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "размышления", позволяющие предоставлять ответы с большей точностью и нюансированной обработкой контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
  
  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Pro Preview (5 июня, vision-версия)

Gemini 2.5 Pro — это передовая ИИ-модель Google, разработанная для решения сложных задач в области рассуждений, программирования, математики и науки. Она использует возможности "мышления", что позволяет ей формулировать ответы с повышенной точностью и учетом нюансов контекста.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash Preview 05 20 (vision-версия) (с 16 июля перенаправляется в 2.5 Flash)

Gemini 2.5 Flash — это передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "мышления", позволяющие ей предоставлять ответы с большей точностью и учитывать нюансы контекста.  
  
Примечание: Эта модель доступна в двух вариантах: с мышлением и без мышления. Стоимость выходных данных значительно варьируется в зависимости от того, активна ли функция мышления.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 4р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### OpenAI: o4-mini (vision-версия)

ОБЩЕЕ ОПИСАНИЕ:  
OpenAI o4-mini — это компактная модель рассуждения в o-серии, оптимизированная для быстрой и экономичной производительности, сохраняющая при этом сильные мультимодальные и агентные возможности. Она поддерживает использование инструментов и демонстрирует конкурентоспособные показатели в рассуждениях и программировании по таким критериям, как AIME (99,5% с Python) и SWE-bench, превосходя своего предшественника o3-mini и даже приближаясь к o3 в некоторых областях.  
  
Несмотря на свой меньший размер, o4-mini демонстрирует высокую точность в задачах STEM, решении визуальных проблем (например, MathVista, MMMU) и редактировании кода. Она особенно хорошо подходит для сценариев с высокой пропускной способностью, где критичны задержки или стоимость. Благодаря эффективной архитектуре и усовершенствованному обучению с подкреплением, o4-mini может связывать инструменты, генерировать структурированные выходные данные и решать многоэтапные задачи с минимальной задержкой — часто менее чем за минуту.  
  
ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:  
До выдачи результатов по API модель размышляет над ответом. Это стоит довольно много токенов, но не показывается в ответе.  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.  
В случае, если в процессе рассуждения достигнут лимит Макс токенов выхода, будет выдан пустой ответ - но он будет тарифицирован.  
Также мы рекомендуем указывать повышенное время timeout, если вы используете API - модель может думать иногда 10 минут и более на сложных задачах.  
  
ВРЕМЕННО:  
- не работает со стримингом. Т.е. недоступна через обычный чат, но можно воспользоваться специальным в Сервисах.  
**Минимальный баланс для вызова модели: 20р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini 2.5 Flash Preview (vision-версия) (с 16 июля перенаправляется в 2.5 Flash)

Gemini 2.5 Flash — это передовая рабочая модель Google, специально разработанная для сложных задач рассуждения, программирования, математики и научных исследований. Она включает встроенные возможности "мышления", позволяющие ей предоставлять ответы с большей точностью и учитывать нюансы контекста.  
  
Примечание: Эта модель доступна в двух вариантах: с мышлением и без мышления. Стоимость выходных данных значительно варьируется в зависимости от того, активна ли функция мышления.  
  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 4р.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Scout (быстрая, Vision-версия)

Llama 4 Scout 17B Instruct (16E) - vision-версия  
  
Для запуска используется сет провайдеров:  
- Быстрый инференс (до 400 токенов в секунду) предоставляется, если вход не превышает 128К токенов, а требуемый выход - 8К токенов  
- В противном случае используются дополнительные провайдеры, которые могут обрабатывать вход и выход вплоть до 328К токенов  
  
Поддержка tools не декларировалась официально, но присутствует.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 3р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Llama 4 Maverick (Vision-версия)

Llama 4 Maverick 17B Instruct (128E) - версия для работы с изображениями.  
  
Поддержка tools не декларировалась официально, но присутствует.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 10р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Gemma 3 27B (опенсорс, vision-версия)

Gemma 3 27B, vision-версия  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1р.**

Закрыть

X

### Qwen2.5 VL 72B Instruct

Qwen2.5 VL 72B - это мультимодальная LLM от команды Qwen.  
  
Qwen2.5-VL искусно распознает обычные объекты, такие как цветы, птицы, рыбы и насекомые. Он также весьма способен анализировать тексты, диаграммы, значки, графику и макеты внутри изображений.  
  
Использование этой модели регулируется ЛИЦЕНЗИОННЫМ СОГЛАШЕНИЕМ Tongyi Qianwen.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 30р.**

Закрыть

X

### Qwen2-VL 72B Instruct

Qwen2 VL 72B - это мультимодальная LLM от команды Qwen со следующими ключевыми улучшениями:  
  
Передовое понимание изображений различного разрешения и соотношения сторон: Qwen2-VL достигает наилучших результатов в тестах на визуальное понимание, включая MathVista, DocVQA, RealWorldQA, MTVQA и др.  
  
Агент, способный управлять вашими мобильными устройствами, роботами и т.д.: благодаря способностям к сложным рассуждениям и принятию решений, Qwen2-VL может быть интегрирован с такими устройствами, как мобильные телефоны, роботы и т.д., для автоматического управления на основе визуальной среды и текстовых инструкций.  
  
Многоязычная поддержка: для обслуживания глобальных пользователей, помимо английского и китайского, Qwen2-VL теперь поддерживает понимание текстов на разных языках внутри изображений, включая большинство европейских языков, японский, корейский, арабский, вьетнамский и др.  
  
Использование этой модели регулируется ЛИЦЕНЗИОННЫМ СОГЛАШЕНИЕМ Tongyi Qianwen.  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 30р.**

Закрыть

X

### OpenAI: GPT-4o (2024-08-06) (vision-версия)

Multimodal-версия OpenAI: GPT-4o  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 10р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**  
**Поддерживает вызов structure outputs в стандартном OpenAI формате, см. Документацию.**

Закрыть

X

### Google: Gemini Flash 1.5 (vision-версия) (выключена, перенаправляется в vis-Flash 2.5)

Google: Gemini Flash 1.5  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 1р.**

Закрыть

X

### OpenAI: GPT-4o (vision)

Multimodal-версия OpenAI: GPT-4o  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 10р.**

Закрыть

X

### OpenAI: GPT-4 Vision Turbo

Новейшая модель GPT-4 Turbo с возможностями машинного зрения. Запросы Vision теперь могут использовать режим JSON и вызов функций. Данные обучения: до декабря 2023 г.  
  
Эта модель обновлена OpenAI, чтобы указать на последнюю версию GPT-4 Turbo , в настоящее время gpt-4-turbo-2024-04-09 (по состоянию на апрель 2024 г.).  

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 50р.**

Закрыть

X

### Anthropic: Claude 3 Haiku (vision)

Vision-вариант Haiku   

**ОСОБЕННОСТИ БИЛЛИНГА И ВЫЗОВА:**  
Биллинг осуществляется по данным провайдера - сколько токенов было затрачено на вход и выход, в соответствии с этим идет тарификация. Мы не комментируем и не принимаем претензии, связанные с вычислением токенов у провайдера.

  
**Минимальный баланс для вызова модели: 10р.**  
**Поддерживает вызов tools в стандартном OpenAI формате, см. Документацию.**

Закрыть

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

# 3. Тарифы

## Тарифы

Источник: https://vsegpt.ru/Docs/Tariffs

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Тарифы

  

[Обычные](https://vsegpt.ru/Docs/Tariffs)[Расширенные](https://vsegpt.ru/Docs/Tariffs/Ext)

  

## Базовый

### 199р за 30 дней

  
**+ стоимость генераций текста [согласно прайсу на модели](https://vsegpt.ru/Docs/Models "Docs / Models")**   
[примеры калькуляции стоимости](/Docs/Tariffs/Example)  
  
*[Все модели](https://vsegpt.ru/Docs/Models "Docs / Models"), КРОМЕ топовых маркированных  Профессиональный  , т.е. GPT-5, o4 (разных версий), Claude Sonnet/Opus, Vision. Идеально для старта*   
  
**Доступ к API.**   
**Разрешаются сторонние программы для автоматизации и боты.**   
**Без лимитов числа оплачиваемых генераций**  
  
**Бесплатный тестовый период** сразу после регистрации.  
  
Ограничения: 1 запрос в секунду c [дополнительными условиями](https://vsegpt.ru/Docs/Tariffs/Limits "Docs/Tariffs/Limits")  
  
Модели, требующие более высокого плана, чем Базовый маркируются в [списке моделей](https://vsegpt.ru/Docs/Models "Docs / Models")   
  
Для физлиц.

## Профессиональный

### 399р за 30 дней или 99р за 3 дня

  
**+ стоимость генераций текста [согласно прайсу на модели](https://vsegpt.ru/Docs/Models "Docs / Models")**   
[примеры калькуляции стоимости](/Docs/Tariffs/Example)  
  
*[Все модели](https://vsegpt.ru/Docs/Models "Docs / Models"), ВКЛЮЧАЯ GPT-5, последний Claude Sonnet/Opus, Mistral Medium+, Vision, Kling, FLUX.  
Для тех, кому нужны самые мощные модели*   
  
**Доступ к API.**   
**Разрешаются сторонние программы для автоматизации и боты.**   
**Без лимитов числа оплачиваемых генераций**  
  
**Бесплатный тестовый период** сразу после регистрации.  
  
Ограничения: 1 запрос в секунду c [дополнительными условиями](https://vsegpt.ru/Docs/Tariffs/Limits "Docs/Tariffs/Limits") (Нужно больше? Посмотрите [тариф FAST](https://vsegpt.ru/Docs/Tariffs/Ext "Docs / Tariffs / Ext")).  
  
Для физлиц.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## VseGPT : Docs / Tariffs / Example

Источник: https://vsegpt.ru/Docs/Tariffs/Example

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

## Оплатите подписку и генерации

  
Если вы пополнили баланс на 300 р. и не активировали подписку...  
...вы не можете генерировать тексты/обращаться к API, т.к. у вас **нет активной подписки**.  
  
Если вы пополнили баланс на 399 р. и активировали подписку за 399 р...  
...то на балансе остался 0, и вы не можете генерировать тексты, т.к. **каждая генерация должна быть оплачена**. При запросе оценивается стоимость генерации, и если она выше остатка на вашем балансе, то запрос не проходит.   
  
Если вы пополнили баланс на 499 р. и активировали подписку за 399 р....   
...то у вас осталось 100 на балансе. Далее вы делаете запрос к модели ChatGPT, и он стоит 0.1 р. На балансе у вас остается 99.9 р. **Далее вы можете делать запросы к моделям, пока у вас активна подписка и не исчерпался баланс.**

## Генерации – дешевые

  
Запрос ниже **«Напиши 5 идей для детского праздника»** стоил **0.117 р.** (нейросеть gpt-4o-mini)  
  
Таких запросов **за 500 рублей** вы можете сделать **4270 – это по 25 запросов в час (каждые 2 минуты), работая 20 дней по 8 часов**  
  
![](https://vsegpt.ru/pdfs/example_account12.png)
  

## Как считается стоимость запроса?

  
Она складывается из стоимости входа (ваш запрос) + стоимость выхода (генерация модели). Для [разных моделей цены разные](https://vsegpt.ru/Docs/Models "Docs / Models"), топовые модели обойдутся дороже.  
  
Посчитаем пример выше для нейросети **OpenAI: gpt-4o-mini** (стоимость [согласно нашей таблице моделей](https://vsegpt.ru/Docs/Models "Docs / Models") 0.02 за 1000 входа, 0.08 за 1000 выхода).  
  
**Вход:** 67 символов – это вход, включая служебные символы. Считаем стоимость входа: 65\*0.02/1000 = 0.0013  
**Выход:** 1446 символов было сгенерировано. Считаем стоимость выхода: 1446\*0.08/1000 = 0.11568  
**Всего:** 0.11568+0.0013 = 0.117 (с округлением)

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Командные тарифы

Источник: https://vsegpt.ru/Docs/Tariffs/ExampleTeam

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Командные тарифы

  

[Общее описание](#h131-2)

[Общая механика работы + скриншот интерфейса](#h131-3)

[Пример тарификации](#h131-4)

  

## Общее описание

  
**Ключевая функция:** головной аккаунт с данным тарифом получает секретный ключ, по которому к нему может присоединиться до 10 допаккаунтов – членов команды. Головной аккаунт осуществляет централизированное управление средствами: может перечислять средства на счет членов, а также возвращать их обратно.  
  
Каждый член команды имеет свой кабинет, API-ключ и должен **самостоятельно** оплачивать подписку и дополнительные траты; подписка для членов команды **не включена** в данный тариф. Также на головном аккаунте доступны функции генерации (тариф Профессиональный).  
  

Тариф не ориентирован на экономию средств – он ориентирован на **увеличение управляемости средств и аккаунтов**.

  

## Общая механика работы + скриншот интерфейса

  
1. Вы активируете тариф Командный  
2. Далее вы заходите в меню **Кабинет > Команда**. Там вы можете сгенерировать секретный ключ для подключения других членов команды.  
3. Вы передаете ключ тем людям, которых хотите подключить. Они регистрируются на сервисе самостоятельно (вариант: вы их регистрируете на свой мейл, и выдаете логин пароль) – после они заходят в меню **Кабинет > Команда**, выбирают «Присоединиться» и вводят ключ. После этого они появляются в вашей команде, и вы можете передавать им средства.  
4. Вы передаете средства на баланс подчиненного аккаунта.  
5. Подчиненный аккаунт, используя средства, активирует подписку и тратит их на генерации.  
  
Пример интерфейса:  
  

![](https://vsegpt.ru/pdfs/vsegpt_team_interface1.png)

  

## Пример тарификации

  
**Пример 1:**   
1. Вы пополнили баланс на 3000 р. и активировали Командную подписку (699 р. на месяц). У вас осталось 2301 р.   
2. Ваш SEO-специалист зарегистрировался и присоединился к вам в команду.  
3. Вы перевели ему на аккаунт 1000 р., у вас осталось 1301 р.   
4. Ему нужно GPT-4, и он активировал у себя на аккаунте подписку Профессиональный – с него списалось 399 р. за месяц. На оставшиеся 601 он может генерировать. Если его работа закончена и больше не требуется, вы можете вернуть эти деньги.  
5. Ваш специалист по ботам зарегистрировался и присоединился к вам в команду.  
6. Вы перевели ему на аккаунт 1000 р., у вас осталось 301 р.   
7. Ему не нужно GPT-4, и он активировал у себя на аккаунте подписку Базовый – с него списалось 199 р. за месяц. На оставшиеся 801 р. можно запускать бота с API-ключом, выписанным на этот аккаунт.   
  
Через месяц с ваших аккаунтов будут взяты деньги за продление тарифов – 699 за Командный аккаунт, 399 за аккаунт SEO специалиста, 199 р за аккаунт специалиста по ботам.  
  
Если денег на аккаунте у кого-то из специалистов не будет, подписка аккаунта конкретного специалиста будет просто приостановлена.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Тарифы

Источник: https://vsegpt.ru/Docs/Tariffs/Ext

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Тарифы

 
  

[Обычные](https://vsegpt.ru/Docs/Tariffs)[Расширенные](https://vsegpt.ru/Docs/Tariffs/Ext)

  
  

**Расширенные тарифы ВКЛЮЧАЮТ все функции тарифа Профессиональный:**

- Доступно API, разрешается подключение сторонних программ для автоматизации и ботов.
- Нет лимитов на платные генерации
- Доступны [все модели](https://vsegpt.ru/Docs/Models "Docs / Models")

  

## Командный

### 699р за 30 дней и 4 подаккаунта

### 999р за 30 дней и 10 подаккаунтов

  
**+ стоимость генерации текста [в соответствии с использованием моделей](https://vsegpt.ru/Docs/Models "Docs / Models")**  
  
Возможность присоединять членов команды и управлять их балансом.  
  
Для команд до 4 или 10 человек (также есть варианты до 20, 50 и пр.).  
  
**Ключевая функция:** головной аккаунт с данным тарифом получает секретный ключ, по которому к нему может присоединиться до 10 допаккаунтов – членов команды. Головной аккаунт осуществляет централизированное управление кредитами: может перечислять средства на баланс допаккаунтов, а также возвращать их обратно – **таким образом, оплачивая подписку и генерации за всю команду**.   
  
Каждый допаккаунт имеет свой кабинет и API-ключ, и должен активировать подписку. **Подписка для каждого подаккаунта НЕ включена в данный тариф**. Средства допаккаунт обычно получает с головного аккаунта.  
  
[Примеры тарификации для команды](/Docs/Tariffs/ExampleTeam)  
  
Для физлиц.  
  
Не в публичном доступе; подключаем по заявке.  
  
[Заявка на подключение](/Docs/Tariffs/TeamStart)

## FAST

### 999р за 30 дней

  
**+ стоимость генерации текста [в соответствии с использованием моделей](https://vsegpt.ru/Docs/Models "Docs / Models")**  
  
Повышенные лимиты на число запросов в секунду  
  
Ограничения: под вопросом, в тестировании. Мы спокойно принимаем до 10–20 запросов в секунду; потенциально до 100 запросов в секунду. **Вам нужно будет перенастроить вызовы OpenAI endpoint на другой URL для быстрых запросов**  
  
Для физлиц.  
  
Тариф не находится в публичном доступе, чтобы мы могли адекватно подключать мощности по мере роста числа высокоскоростных пользователей. Обычно подключаем без проблем по заявке. **Напишите заявку на e-mail, указанный в [контактах](https://vsegpt.ru/Kontakty "Контакты")**

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Расширенные тарифы

Источник: https://vsegpt.ru/Docs/Tariffs/Fast

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Расширенные тарифы

 

## Профессиональный FAST

### 999р за 30 дней

  
**+ стоимость генерации текста [в соответствии с использованием моделей](https://vsegpt.ru/Docs/Models "Docs / Models")**  
[примеры тарификации](/Docs/Tariffs/Example)  
  
*[Все модели](https://vsegpt.ru/Docs/Models "Docs / Models"). Для профессионалов*  
  
**Доступ к API. Разрешается подключение сторонних программ для автоматизации и ботов. Без лимитов числа оплачиваемых генераций**  
  
Ограничения: под вопросом, в тестировании. Мы спокойно принимаем до 10–20 запросов в секунду; потенциально до 100 запросов в секунду. **Вам нужно будет перенастроить вызовы OpenAI endpoint на другой URL для быстрых запросов**  
  
Для физлиц.  
  
Тариф не находится в публичном доступе, чтобы мы могли адекватно подключать мощности по мере роста числа высокоскоростных пользователей. Обычно подключаем без проблем по заявке. **Напишите заявку на e-mail, указанный в [контактах](https://vsegpt.ru/Kontakty "Контакты")**

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Дополнительные условия по лимитам

Источник: https://vsegpt.ru/Docs/Tariffs/Limits

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Дополнительные условия по лимитам

  
По умолчанию лимит на запросы составляет 1 запрос в 1 секунду; но в случаях большой нагрузки мы оставляем за собой право повышать его вплоть до 1 запроса в 2–3 секунды.  
  
Если вам нужны увеличенные лимиты с большим RPS, обратитесь к тарифу [FAST](https://vsegpt.ru/Docs/Tariffs/Fast "Docs / Tariffs / Fast")

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

## Как подключить тариф Командный

Источник: https://vsegpt.ru/Docs/Tariffs/TeamStart

[VseGPT.ru](https://vsegpt.ru/)

120+ нейросетей с аптаймом 99%  
доступ из России без VPN и блокировок  
OpenAI API для автоматизаций

[Вход](https://vsegpt.ru/Login "Login")

- [Преимущества](/)
- [Тарифы](/Docs/Tariffs)
- [Модели](/Docs/Models)
- [Готовые интеграции](/ExtTools)
- [Документация](#)
  - [Модели по новизне](/Docs/ModelsNew)
  - [Документация API](/Docs/API)
  - [Статистика Uptime](/Docs/Uptime)
  - [Туториалы](/Tutorials)
- [Бесплатный тест + API](/Reg)

# Как подключить тариф Командный

  
1. Внимательно ознакомьтесь с [подробным описанием тарифа](https://vsegpt.ru/Docs/Tariffs/ExampleTeam "Docs / Tariffs / Example Team") – надеемся, там все будет понятно.  
2. Пополните баланс так, чтобы на нем было не менее 1500 р.  
3. Активируйте тариф Профессиональный (если не активирован)  
4. Напишите заявку на e-mail, указанный в [контактах](https://vsegpt.ru/Kontakty "Контакты"), укажите какой именно тариф вы хотите – Командный на 4 человека или на 10 и пр.  
  
**Обычно в течение суток мы:**  
1. Активируем вам тариф  
2. Спишем разницу в стоимости тарифа за 1 месяц с баланса.  
  
Если вы не получили ответа – это наша ошибка, пожалуйста, напишите вновь.

VseGPT, © 2023–2026 | [Контакты](https://vsegpt.ru/Kontakty "Контакты") | [Правила сервиса](https://vsegpt.ru/docs/TermsOfUse "docs / Terms Of Use") | [Договор-оферта](https://vsegpt.ru/docs/oferta "docs / oferta") | [Политика конфиденциальности](https://vsegpt.ru/privacy "privacy") | [Для юрлиц](https://vsegpt.ru/BusinessAction "Business Action") | [Сотрудничество](https://vsegpt.ru/Docs/Partner "Docs / Partner")

---

