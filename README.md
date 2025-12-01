## ❗Немного о проекте
Собственная система аутентификации и авторизации, реализованная на Django REST Framework с использованием JWT токенов и ролевой моделью доступа

## 🚀 Основные возможности

- **Регистрация и аутентификация** пользователей по email и паролю
    
- **JWT токены** с системой blacklist для безопасного logout
    
- **Ролевая модель доступа** с гибкой системой разрешений
    
- **Мягкое удаление** пользователей с сохранением данных
    
- **RESTful API** с полной документацией
## 📒 Структура проекта
```
backend/
├── apps/
│   ├── authentication/    # JWT, auth
│   ├── users/              # Кастомный User + профиль
│   ├── permissions/        # Ресурсы, роли, права
│   └── social/             # Посты (демо бизнес-логики)
├── config/
│   ├── settings.py         # python-decouple + .env
│   └── urls.py
└── fixtures/               
```
## 📃 Схема системы управления доступом

### 🎭 Сущности

| Сущность               | Описание                                                            |
| ---------------------- | ------------------------------------------------------------------- |
| **User**               | Кастомный пользователь                                              |
| **Role**               | Название роли (user, moderator, admin, manager…)                    |
| **Resource**           | Логический объект системы (posts, users, orders, resources, roles…) |
| **UserRole**           | Привязка роли к пользователю + поле `is_active`                     |
| **RoleResourceAccess** | Какие действия роль может выполнять над ресурсом                    |
### 📁 Схема базы данных
```
users_user           -- Пользователи системы
├── id
├── email
├── password
├── first_name
├── last_name
├── middle_name
├── is_active
├── is_superuser
└── is_staff

permmissons_role           -- Роли пользователей
├── id
├── name
├── is_active
└── description

permissoins_user_roles     -- Связь пользователей с ролями
├── user_id
└── role_id

permissions_resource      -- Ресурсы системы
├── id
├── name
├── code
└── description

access_permission    -- Разрешения (роль → ресурс → действие)
├── role_id
├── resource_id
├── can_create
├── can_read
├── ...
├── can_delete
└── can_delete_all
```
### 🍋 Права

| Право            | Описание                            | Пример использования              |
| ---------------- | ----------------------------------- | --------------------------------- |
| `can_create`     | Создавать новые объекты             | POST /posts/                      |
| `can_read`       | Читать свои объекты                 | GET /posts/5                      |
| `can_read_all`   | Читать все объекты ресурса          | GET /posts/                       |
| `can_update`     | Редактировать свои объекты          | PATCH /posts/5/                   |
| `can_update_all` | Редактировать любые объекты ресурса | PATCH /posts/999/ (админ)         |
| `can_delete`     | Удалять свои объекты                | DELETE /posts/5/                  |
| `can_delete_all` | Удалять любые объекты ресурса       | ELETE /posts/5/ (модератор/админ) |

## 🔎 Установка и запуск
### 1. Клонирование репозитория
```
git clone <repository-url>
cd django-auth-service
```
### 2. Настройка виртуального окружения
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
### 3. Установка зависимостей
```
pip install -r requirements.txt
```
### 4. Настройка базы данных
```
python manage.py migrate
cd fixtures
python ../manage.py loaddata initial   # загрузка начальных фикстур
```
### 5. Запуск сервера

```
cd ..
python manage.py runserver
```
## 📋 API Документация

### 🔓 Базовые endpoints аутентификации и авторизации
#### 🔐 Регистрация пользователя
```
POST /api/auth/register/
Content-Type: application/json
{
  "email": "user@example.com",
  "first_name": "Artur",
  "last_name": "Sagiev",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```
#### 🔑 Вход в систему
```
POST /api/auth/login/
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
#### 💫 Ответы
```
{
    "user": {
        "email": "admin@admin.ru",
        "first_name": "",
        "last_name": "",
        "middle_name": null,
        "role": []
    },
    "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ..."
    }
}
```
#### 🔄 Обновление токенов
```
POST /api/auth/refresh/
Content-Type: application/json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ..."
}
```
#### 🚪 Выход из системы
```
POST /api/auth/logout/
Authorization: Bearer <access_token>
```
### 😯 Управление профилем
#### 👤 Получение профиля

```
GET /api/users/profile/
Authorization: Bearer <access_token>
```
#### ✏️ Обновление профиля
```
PATCH /api/users/profile/update
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "first_name": "NewName",
  "last_name": "Sagiev"
}
```

### 📆 Управление системой ролей
#### 📜 Создание ресурса (суперюзер/у кого достаточно прав) 
```
POST /api/permissions/resources/
Authorization: Bearer <access_token>
Content-Type: application/json
{ 
	"code": "posts",
	"name": "Посты"
}
```
#### 💎 Создание роли (суперюзер/у кого достаточно прав) 
```
POST /api/permissions/reles/
Authorization: Bearer <access_token>
Content-Type: application/json
{ 
	"name": "Moderator"
}
```
#### 📝 Назначение роли пользователю (суперюзер/у кого достаточно прав) 
```
POST api/permissions/user-roles/
Authorization: Bearer <access_token>
Content-Type: application/json
{
    "user": 2,
    "role_id": 2
}
```
#### 🌂 Назначение прав роли (суперюзер/у кого достаточно прав) 
```
POST /api/permissions/role-resource-access/
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "role_id": 2,
  "resource_id": 3,
  "can_create": true,
  "can_read": true,
  "can_read_all": false,
  "can_update": true,
  "can_update_all": false,
  "can_delete": false,
  "can_delete_all": false
}
```
#### 🚁 Обновление прав роли (суперюзер/у кого достаточно прав)
```
PATCH /api/permissions/role-resource-access/{id}
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "role_id": 2,
  "resource_id": 3,
  "can_create": false,
  "can_read": true,
  "can_read_all": true,
  "can_update": false,
  "can_update_all": false,
  "can_delete": false,
  "can_delete_all": false
}
```

#### ⚠️Получение списка ролей
```
GET /api/permissions/roles/
Authorization: Bearer <access_token>
Content-Type: application/json
```
##### Ответ
```
[
    {
        "id": 1,
        "name": "user",
        "description": "Обычный пользователь",
        "users_count": 1
    },
    {
        "id": 2,
        "name": "testrole",
        "description": null,
        "users_count": 1
    }
]
```
#### ⛽ Получить информацию об определенной роли
```
GET /api/permissions/roles/{id}
Authorization: Bearer <access_token>
Content-Type: application/json
```
##### Ответ
```
{
	"id": 1,
	"name": "user",
	"description": "Обычный пользователь",
	"users_count": 1
}
```

### 💢 Пример отработки ошибок

#### 😒 У пользователя нет прав на просмотр ролей:
```
GET /api/permissions/roles/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NjQ2MDQyMTUsImlhdCI6MTc2NDYwMDYxNSwianRpIjoiYjA2ZGZhY2QtMDBlMS00N2ViLTg3YTEtNTNiNWY1Yzk5NjUzIiwidG9rZW5fdHlwZSI6ImFjY2VzcyJ9.1z0jRwvENromY36iUGKcyu54bgQ9yIeMwp5lFEBFcuM
```
##### Ответ
```
# 403 - Forbidden
{
    "detail": "You do not have permission to perform this action."
}
```
#### 😳 Просмотр профиля без токена
```
GET /api/users/profile/
```
##### Ответ
```
# 401 - Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```
