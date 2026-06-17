Техніка Помідора – це метод управління часом, що може бути використаний для будь-яких завдань. Для багатьох людей час є ворогом. Тривожність, викликана «цоканням годинника», особливо за наявності дедлайну, веде до неефективних звичок в роботі й навчанні, які в свою чергу призводять до прокрастинації (відкладання завдань).

Ціль техніки Помідора полягає в тому, щоб використовувати час як цінного союзника в досягненні того, чого ми хочемо, тим шляхом, яким ми хочемо, й дати нам можливість постійно вдосконалювати те, як ми працюємо чи навчаємося.

---

## 🚀 Інструкція із запуску проекту

### 📋 Передумови
Створи файл `.env` в корені проекту та вкажи налаштування (шаблон у `.env.example`).
Приклад для локального запуску:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=pomodoro
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=pomodoro
CACHE_HOST=127.0.0.1
CACHE_PORT=6379
CACHE_DB=0
```
*(Для запуску повністю в Docker вкажи `DB_HOST=db` та `CACHE_HOST=cache`).*

---

### 🐳 Варіант 1: Запуск через Docker (Найпростіший)

1. **Запусти Docker контейнери:**
   ```bash
   docker-compose up --build -d
   ```
2. **Запусти міграції бази даних:**
   ```bash
   docker-compose exec app alembic upgrade head
   ```
3. **Створи тестову БД (для тестів):**
   ```bash
   docker-compose exec db psql -U postgres -c 'CREATE DATABASE "pomodoro-test";'
   ```
4. **Перевірка:** Додаток доступний за адресою `http://localhost:8000`.

---

### 💻 Варіант 2: Локальний запуск (через Poetry)

1. **Запусти БД та Redis у Docker:**
   ```bash
   docker-compose up -d db cache
   ```
2. **Встанови залежності:**
   ```bash
   poetry install
   ```
3. **Запусти міграції:**
   ```bash
   poetry run alembic upgrade head
   ```
4. **Створи тестову БД:**
   ```bash
   docker-compose exec db psql -U postgres -c 'CREATE DATABASE "pomodoro-test";'
   ```
5. **Запусти додаток:**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

---

### 🧪 Запуск тестів
```bash
poetry run pytest
```
