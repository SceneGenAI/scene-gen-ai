# Искусственный интеллект для создания сцен

Этот проект состоит из двух интерфейсов: один использует React, а другой - Streamlit.

## Project Structure
- **Frontend**: Основной интерфейс, созданный с помощью React.
- **Backend**: FastAPI бэкенд с обращением к ML моделям.
  
## Документация и URL-адреса интерфейса
- **Документация по API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Интерфейс React**: [http://localhost:5173/](http://localhost:5173/)

## Требования
Перед запуском проекта убедитесь, что установлены все зависимости:



```sh
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --no-cache-dir
pip install -qq -U diffusers datasets transformers accelerate ftfy pyarrow==9.0.0 --no-cache-dir
```
Кроме того, требуются Node.js и npm.
https://nodejs.org/en/download/prebuilt-installer

## Запуск проекта локально

### Шаг 1: Запустите серверную часть
Откройте окно терминала и запустите:
```sh
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
Note: лучше подождать появления подобного сообщения о запуске сервера перед запуском фронтенда:
```
INFO:     Started server process [16160]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
### Шаг 2: Запустите интерфейс React
Откройте второе окно терминала и запустите:
```sh
cd frontend
npm install
npm run dev
```

