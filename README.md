# ToDoList - Phase 3 (FastAPI Web API)

این فاز، برنامه‌ی ToDoList را به یک وب‌سرویس کامل با FastAPI تبدیل می‌کند. لایه‌ها به‌صورت Controller → Service → Repository طراحی شده‌اند و اعتبارسنجی داده‌ها با Pydantic انجام می‌شود. CLI فاز قبلی از رده خارج شده و به‌جای آن باید از وب‌سرویس استفاده کنید.

## راه‌اندازی
- پیش‌نیاز: Python 3.10+, Poetry، و PostgreSQL در دسترس.
- نصب وابستگی‌ها:
```bash
poetry install
```
- تنظیم متغیرها در `.env` (مقادیر نمونه موجود است). مهم‌ترین متغیرها:
  - `DATABASE_URL` برای اتصال به پایگاه داده
  - `MAX_NUMBER_OF_PROJECT`، `MAX_NUMBER_OF_TASK`، `TITLE_MAX`، `DESC_MAX`، `STATUS_VALUES`
- اجرای مهاجرت‌ها (در صورت نیاز):
```bash
poetry run alembic upgrade head
```

## اجرا
وب‌سرویس را با Uvicorn اجرا کنید:
```bash
poetry run uvicorn main:app --reload
```
- مستندات خودکار: `http://127.0.0.1:8000/api/v1/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/api/v1/openapi.json`
- CLI قدیمی (`cli.py`) پشتیبانی نمی‌شود و برای استفاده‌ی جدید پیشنهاد نمی‌گردد.

## ساختار پروژه
```
.
├── app
│   ├── api                     # API Layer
│   │   ├── controllers
│   │   │   └── projects_controller.py
│   │   ├── controller_schemas  # Pydantic models for request/response
│   │   │   ├── requests
│   │   │   │   ├── project_request_schema.py
│   │   │   │   └── task_request_schema.py
│   │   │   └── responses
│   │   │       ├── project_response_schema.py
│   │   │       └── task_response_schema.py
│   │   └── routers.py
│   ├── core                    # Settings/config
│   │   └── config.py
│   ├── repositories            # Data access layer
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   ├── services                # Business logic layer
│   │   ├── exceptions.py
│   │   ├── project_service.py
│   │   └── task_service.py
│   ├── db.py
│   └── models.py
├── main.py                     # FastAPI initialization
├── pyproject.toml
├── alembic/...
├── .env
└── cli.py (deprecated)
```

## مسیرهای کلیدی API
- پروژه‌ها:
  - `GET /api/v1/projects` (لیست)
  - `POST /api/v1/projects` (ایجاد)
  - `GET /api/v1/projects/{project_id}` (جزئیات + تسک‌ها)
  - `PUT /api/v1/projects/{project_id}` (ویرایش)
  - `DELETE /api/v1/projects/{project_id}` (حذف)
- تسک‌ها (زیرمجموعه‌ی هر پروژه):
  - `GET /api/v1/projects/{project_id}/tasks`
  - `POST /api/v1/projects/{project_id}/tasks`
  - `GET /api/v1/projects/{project_id}/tasks/{task_id}`
  - `PUT /api/v1/projects/{project_id}/tasks/{task_id}`
  - `PATCH /api/v1/projects/{project_id}/tasks/{task_id}/status`
  - `DELETE /api/v1/projects/{project_id}/tasks/{task_id}`

## نکات پیاده‌سازی
- استفاده از Pydantic v2 و Field constraints برای کنترل طول و نوع داده.
- جداسازی لایه‌ها مطابق معماری لایه‌ای؛ کنترلرها فقط سرویس‌ها را صدا می‌زنند.
- استفاده از FastAPI برای مستندسازی خودکار (Swagger / OpenAPI).
- از env برای محدودیت‌ها و مقدارهای مجاز وضعیت‌ها استفاده می‌شود.

