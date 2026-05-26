FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY . .

RUN uv run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "wings.wsgi:application", "--bind", "0.0.0.0:8000"]
