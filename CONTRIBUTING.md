# Искусственный интеллект для создания сцен

Этот проект состоит из двух интерфейсов: один использует React, а другой - Streamlit.

## Project Structure
- **Frontend**: Основной интерфейс, созданный с помощью React.
- **Frontend-Test**: Тестирование интерфейса, созданного с помощью Streamlit.

## Документация и URL-адреса интерфейса
- **Документация по API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Интерфейс React**: [http://localhost:5173/](http://localhost:5173/)
- **Интерфейс Streamlit**: [http://localhost:8501](http://localhost:8501)

## Требования
Перед запуском проекта убедитесь, что выполнены все требования:



```sh
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --no-cache-dir
pip install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0.0 --no-cache-dir
```
Кроме того, требуются Node.js и npm.

## Запуск проекта локально

### Шаг 1: Запустите серверную часть
Откройте окно терминала и запустите:
```sh
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Шаг 2: Запустите интерфейс React
Откройте второе окно терминала и запустите:
```sh
cd frontend
npm install
npm run dev
```

### Альтернативный вариант: Запустите интерфейс Streamlit
Чтобы запустить автоматизированный конвейер, откройте окно терминала и запустите:
```sh
cd frontend-test
streamlit run app.py
```

## Запуск с помощью Docker

Чтобы запустить все приложение с помощью Docker (необходимо исправить поддержку графического процессора), используйте следующие команды:
```sh
docker-compose build
docker-compose up
```

