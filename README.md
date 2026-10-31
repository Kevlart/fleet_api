# 🚀 REST API для управления космическим флотом

Учебный проект, реализующий REST API на **Flask** для управления космическими кораблями и миссиями. 
Данные хранятся в оперативной памяти (сбрасываются при перезапуске сервера).

## 📋 Функционал
- Создание, просмотр, удаление космических кораблей.
- Смена статуса кораблей (доступен, в миссии, на ремонте).
- Создание и управление миссиями (исследование, защита).
- Добавление кораблей в миссии.
- Валидация входящих данных и обработка ошибок (400, 404, 500).

## 📁 Структура проекта

```text
fleet-api/
├── app.py             # Главный файл с маршрутами Flask
├── fleet.py           # Классы Spaceship, Mission, CrewMember
├── requirements.txt   # Зависимости проекта
└── README.md          # Описание проекта
```
🛠️ Установка и запуск
Клонируйте репозиторий:
```
bash
git clone https://github.com/ВАШ_ЛОГИН/fleet-api.git
cd fleet-api
```
Установите зависимости:
```
bash
pip install -r requirements.txt
```
Запустите сервер:
```
bash
python app.py
```
Сервер запустится по адресу: http://127.0.0.1:5000

📡 Эндпоинты API
🛸 Корабли (Spaceships)
```
Метод	URL	Описание

GET	/api/v1/spaceships	Получить список всех кораблей

POST	/api/v1/spaceships	Создать новый корабль

GET	/api/v1/spaceships/<id>	Получить корабль по ID

PATCH	/api/v1/spaceships/<id>/status	Обновить статус корабля

DELETE	/api/v1/spaceships/<id>	Удалить корабль
```
🌌 Миссии (Missions)
```
Метод	URL Описание

GET	/api/v1/missions	Получить список всех миссий

POST	/api/v1/missions	Создать новую миссию

GET	/api/v1/missions/<id>	Получить миссию по ID

PATCH	/api/v1/missions/<id>/status	Обновить статус миссии

POST	/api/v1/missions/<id>/spaceships	Добавить корабль в миссию

DELETE	/api/v1/missions/<id>/spaceships/<ship_id>	Убрать корабль из миссии

DELETE	/api/v1/missions/<id>	Удалить миссию
```
📝 Допустимые значения
```
Тип корабля (type): research (исследовательский), combat (боевой).

Статус корабля (status): available, in_mission, under_repair.

Цель миссии (goal): research, defense.

Статус миссии (status): planned, in_progress, completed.
```
⚠️ Обработка ошибок
```
Сервер возвращает корректные HTTP-статусы и JSON-сообщения:

200 OK — Успешный запрос.

201 Created — Объект успешно создан.

400 Bad Request — Ошибка в данных (например, неверный статус или тип).

404 Not Found — Объект с таким ID не найден.

500 Internal Server Error — Внутренняя ошибка сервера.
```
