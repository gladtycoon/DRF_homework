# 🎓 LMS API (Django REST Framework)

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Репозиторий содержит backend-часть платформы для онлайн-обучения (LMS).**  
Проект построен на архитектуре REST API с разделением логики через ViewSets и Generic-классы, что делает код гибким и масштабируемым.

---

## 📌 О проекте

В мире стремительного роста онлайн-образования важно не только уметь учиться, но и создавать инфраструктуру для обучения.  
Данный проект — это **SPA-совместимый бэкенд**, который отдает данные в формате JSON для фронтенда или мобильных приложений.

### Ключевые возможности
- 👤 **Кастомная модель пользователя** с авторизацией по Email.
- 📚 **Управление курсами** (название, описание, превью).
- 🎬 **Управление уроками** (видео-ссылки, привязка к курсам).
- 🛠 **Гибкая архитектура CRUD**:
  - *Курсы* — через **ViewSet** (быстрый роутинг).
  - *Уроки* — через **Generic-классы** (тонкая настройка методов).

---

## 🛠 Технологии

- **Backend:** Python 3.14+, Django 6.0.6+
- **API:** Django REST Framework (DRF)
- **База данных:** PostgreSQL (по умолчанию, легко меняется на SQLite3)
- **Документация:** Поддерживается OpenAPI (drf-spectacular) — *опционально*.

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/gladtycoon/DRF_homework.git
cd DRF_homework
