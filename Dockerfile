FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.1.3"

COPY pyproject.toml poetry.lock ./

# в Docker-контейнерах, где среда уже изолирована, и виртуальное окружение не нужно
RUN poetry config virtualenvs.create false

# устанавливает зависимости без установки самого проекта и без вопросов
RUN poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "app.main:app", "-c", "app/core/gunicorn.conf.py"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
