<h1 align="center">ETL-конвейер для анализа отзывов пользователей с маркетплейсов</h1>

<p align="center">
  Автоматизированный пайплайн извлечения, трансформации и загрузки данных отзывов. Очистка, агрегация и подготовка данных для анализа тональности и трендов по брендам.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg?style=flat&logo=python" alt="Python" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Pandas-2.2-red.svg?style=flat&logo=pandas" alt="Pandas" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/SQLite-3-green.svg?style=flat&logo=sqlite" alt="SQLite" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Airflow-2.10-orange.svg?style=flat&logo=apache-airflow" alt="Airflow" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Docker-Compose-blue.svg?style=flat&logo=docker" alt="Docker" />
</p>

---

## 📊 Архитектура ETL-процесса

<p align="center">
  <img src="https://github.com/user-attachments/assets/a1a28a1c-4e17-466d-9ac3-01df1d53b654" width="80%" alt="Схема ETL-конвейера" />
</p>

Конвейер реализует классическую схему **ETL** с автоматизацией через Apache Airflow:

1.  **Extract (Извлечение):** 
    Система автоматически считывает исходные данные из CSV-файла. 
    * [Скачать marketplace_reviews.csv](marketplace_reviews.csv)
2.  **Transform (Трансформация):** 
    Очистка текста, нормализация форматов и расчет тональности.
3.  **Load (Загрузка):** 
    Сохранение структурированных данных и агрегатов в SQLite базу.
---

## 🛠 Технологический стек

* **Язык программирования:** Python 3.12
* **Обработка данных:** `pandas`, `pyarrow` (формат Parquet)
* **Оркестрация:** Apache Airflow (LocalExecutor)
* **Хранилище данных:** SQLite
* **Контейнеризация:** Docker, Docker Compose
* **Тестирование:** pytest

---

## 📂 Структура проекта

```bash
├── dags/                  # DAG-файлы Apache Airflow
│   └── reviews_etl_dag.py # Основной сценарий пайплайна
├── etl/                   # Модули с логикой этапов ETL
│   ├── extract.py         # Извлечение данных
│   ├── transform.py       # Очистка и преобразование
│   └── load.py            # Загрузка в SQLite и агрегация
├── tests/                 # Модульные тесты (pytest)
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── docker-compose.yaml    # Конфигурация инфраструктуры (Airflow + PostgreSQL)
├── pytest.ini             # Настройки для тестов
├── requirements.txt       # Зависимости Python
└── .env                   # Переменные окружения
```


## 🚀 Инструкция по запуску

Шаги по установке и запуску:

1. **Клонируйте репозиторий на свой компьютер:**

```bash
git clone https://github.com/Parsik1/etl-reviews-pipeline.git
```

2. **Запустите инфраструктуру:**

Запустите контейнеры с помощью Docker Compose:

```bash
docker-compose up -d
```

3. **Дождитесь инициализации базы данных и служб Airflow (это займет пару минут).**


4. **Работа с Airflow:**
*  URL: http://localhost:8080
*  Логин: admin
*  Пароль: admin
*  Найдите в списке DAG с именем reviews_etl_dag.
*  Переведите его в положение Unpause (активируйте переключатель).
*  Запустите выполнение кнопкой Trigger DAG (значок воспроизведения).

## 🧪 Тестирование

В проекте реализованы unit-тесты для проверки корректности работы каждого этапа конвейера. Чтобы запустить их локально:

1. **Создайте и активируйте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Запустите тесты через pytest:**
```bash
python -m pytest
```
