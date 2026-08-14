<h1 align="center">ETL-конвейер для анализа отзывов пользователей с маркетплейсов</h1>

<p align="center">
  Автоматизированный пайплайн извлечения, трансформации и загрузки данных отзывов. Очистка, агрегация и подготовка данных для анализа тональности и трендов по брендам в реальном времени.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python" alt="Python" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Pandas-2.0+-red.svg?style=flat&logo=pandas" alt="Pandas" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/SQLite-3.45+-green.svg?style=flat&logo=sqlite" alt="SQLite" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Airflow-2.0+-orange.svg?style=flat&logo=apache-airflow" alt="Airflow" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Docker-20.10+-blue.svg?style=flat&logo=docker" alt="Docker" />
</p>

---

## 📊 Архитектура ETL-процесса

<p align="center">
  <img src="https://github.com/user-attachments/assets/a1a28a1c-4e17-466d-9ac3-01df1d53b654" width="80%" alt="Схема ETL-конвейера" />
  <br>
  <i>Последовательность шагов: извлечение из CSV → трансформация (очистка, фильтрация, расчёт тональности) → загрузка в SQLite с агрегацией.</i>
</p>

---

## 🛠 Технологический стек и инженерные решения

Проект построен на базе проверенных библиотек и подходов к обработке данных:

* **Язык программирования:** Python 3.8+.
* **Обработка данных:** `Pandas` – мощный инструмент для фильтрации, трансформации и агрегации.
* **Хранилище:** `SQLite` – лёгкая встраиваемая БД для финального хранения очищенных данных и агрегатов.
* **Промежуточный формат:** `Parquet` – колоночное хранение для ускорения чтения/записи и экономии места.
* **Оркестрация:** `Apache Airflow` – запуск конвейера по расписанию с мониторингом и веб-интерфейсом.
* **Контейнеризация:** `Docker` + `Docker Compose` – для воспроизводимого окружения и лёгкого развёртывания.
* **Тестирование:** `pytest` – модульные тесты для проверки корректности трансформаций.

---

## 📂 Структура проекта

```bash
├── .pytest_cache/           # Кэш тестов
├── dags/                    # DAG-файлы Airflow
│   └── reviews_etl_dag.py   # Основной DAG конвейера
├── data/
│   ├── raw/                 # Исходные CSV-файлы (marketplace_reviews.csv)
│   └── processed/           # Промежуточные Parquet и финальная база reviews.db
├── etl/                     # Модули ETL
│   ├── extract.py           # Извлечение данных из CSV
│   ├── transform.py         # Трансформация и очистка
│   └── load.py              # Загрузка в SQLite и агрегация
├── logs/                    # Логи Airflow
├── plots/                   # Графики и визуализации (опционально)
├── plugins/                 # Плагины Airflow (при необходимости)
├── tests/                   # Модульные тесты
│   └── test_transform.py    # Тесты для функций трансформации
├── venv/                    # Виртуальное окружение (локально)
├── .env                     # Переменные окружения
├── docker-compose.yaml      # Оркестрация контейнеров (Airflow + Postgres + Redis)
├── pytest.ini               # Конфигурация pytest
├── requirements.txt         # Зависимости Python
├── reviews_agg_daily.csv    # Экспортированная агрегация (пример)
└── reviews.db               # Финальная база данных SQLite
