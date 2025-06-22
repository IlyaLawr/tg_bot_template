##                       Hamster Combat from Ali Express

**Инструкция по запуску проекта и тестов через Makefile**

# Для запуска проекта и тестов необходимо чтобы в системе были установлены Docker daemom и Docker compose.

1. Клонируем репозиторий и переходим в папку проекта:
```bash
    git clone <https://github.com/IlyaLawr/tg_bot_template.git>
    cd tg_bot_template
```

2. Необходимо заполнить переменные окружения в файлах `.env.example` и `.env.test.example` актуальными данными.

3. Для запуска проекта:
```bash
    make up 
```

3. Для запуска тестов:
```bash
    make test 
```

