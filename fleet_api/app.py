from flask import Flask, request, jsonify
from fleet import Spaceship, Mission

# ============================================================
# Приложение и «база данных» в памяти
# ============================================================
app = Flask(__name__)
app.json.ensure_ascii = False #для записи на русском языке

spaceships = {}        # {id: Spaceship}
missions = {}          # {id: Mission}

next_ship_id = 1       # счётчик для новых кораблей
next_mission_id = 1    # счётчик для новых миссий


# ============================================================
# Хелпер для ошибок
# ============================================================
def error(message, code=400):
    return jsonify({"error": message}), code


# ============================================================
# Служебный маршрут — проверка, что сервер жив
# ============================================================
@app.route("/api/v1", methods=["GET"])
def home():
    return jsonify({"message": "Сервер работает!"}), 200


# ============================================================
# Корабли
# ============================================================
@app.route("/api/v1/spaceships", methods=["GET"])
def list_spaceships():
    # можно фильтровать: ?status=available&type=research
    status = request.args.get("status")
    type_ = request.args.get("type")

    result = list(spaceships.values())
    if status:
        result = [s for s in result if s.status == status]
    if type_:
        result = [s for s in result if s.type_ == type_]

    return jsonify([s.to_dict() for s in result]), 200


@app.route("/api/v1/spaceships", methods=["POST"])
def create_spaceship():
    global next_ship_id

    data = request.get_json(silent=True)
    if not data:
        return error("тело запроса должно быть JSON")

    name = data.get("name")
    type_ = data.get("type")
    status = data.get("status", "available")

    if not name or not isinstance(name, str):
        return error("поле 'name' обязательно и должно быть строкой")
    if type_ not in ("research", "combat"):
        return error("поле 'type' должно быть 'research' или 'combat'")
    if status not in Spaceship.STATUSES:
        return error(f"статус '{status}' не разрешён, можно: {Spaceship.STATUSES}")

    ship = Spaceship(next_ship_id, name, type_, status)
    spaceships[next_ship_id] = ship
    next_ship_id += 1

    return jsonify(ship.to_dict()), 201


@app.route("/api/v1/spaceships/<int:ship_id>", methods=["GET"])
def get_spaceship(ship_id):
    ship = spaceships.get(ship_id)
    if not ship:
        return error(f"корабль с id {ship_id} не найден", 404)
    return jsonify(ship.to_dict()), 200


@app.route("/api/v1/spaceships/<int:ship_id>/status", methods=["PATCH", "PUT"])
def update_spaceship_status(ship_id):
    ship = spaceships.get(ship_id)
    if not ship:
        return error(f"корабль с id {ship_id} не найден", 404)

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if not new_status:
        return error("поле 'status' обязательно")

    try:
        ship.update_status(new_status)
    except ValueError as e:
        return error(str(e))

    return jsonify(ship.to_dict()), 200


@app.route("/api/v1/spaceships/<int:ship_id>", methods=["DELETE"])
def delete_spaceship(ship_id):
    if ship_id not in spaceships:
        return error(f"корабль с id {ship_id} не найден", 404)

    ship = spaceships.pop(ship_id)

    # вычищаем удалённый корабль из всех миссий
    for mission in missions.values():
        if ship in mission.spaceships:
            mission.spaceships.remove(ship)

    return jsonify({"message": f"корабль '{ship.name}' удалён"}), 200


# ============================================================
# Миссии
# ============================================================
@app.route("/api/v1/missions", methods=["GET"])
def list_missions():
    status = request.args.get("status")
    result = list(missions.values())
    if status:
        result = [m for m in result if m.status == status]
    return jsonify([m.to_dict() for m in result]), 200


@app.route("/api/v1/missions", methods=["POST"])
def create_mission():
    global next_mission_id

    data = request.get_json(silent=True)
    if not data:
        return error("тело запроса должно быть JSON")

    name = data.get("name")
    goal = data.get("goal")
    status = data.get("status", "planned")

    if not name or not isinstance(name, str):
        return error("поле 'name' обязательно и должно быть строкой")
    if goal not in ("research", "defense"):
        return error("поле 'goal' должно быть 'research' или 'defense'")
    if status not in Mission.STATUSES:
        return error(f"статус '{status}' не разрешён, можно: {Mission.STATUSES}")

    mission = Mission(next_mission_id, name, goal, status)
    missions[next_mission_id] = mission
    next_mission_id += 1

    return jsonify(mission.to_dict()), 201


@app.route("/api/v1/missions/<int:mission_id>", methods=["GET"])
def get_mission(mission_id):
    mission = missions.get(mission_id)
    if not mission:
        return error(f"миссия с id {mission_id} не найдена", 404)
    return jsonify(mission.to_dict()), 200


@app.route("/api/v1/missions/<int:mission_id>/status", methods=["PATCH", "PUT"])
def update_mission_status(mission_id):
    mission = missions.get(mission_id)
    if not mission:
        return error(f"миссия с id {mission_id} не найдена", 404)

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if not new_status:
        return error("поле 'status' обязательно")

    try:
        mission.update_status(new_status)
    except ValueError as e:
        return error(str(e))

    return jsonify(mission.to_dict()), 200


@app.route("/api/v1/missions/<int:mission_id>/spaceships", methods=["POST"])
def add_spaceship_to_mission(mission_id):
    mission = missions.get(mission_id)
    if not mission:
        return error(f"миссия с id {mission_id} не найдена", 404)

    data = request.get_json(silent=True) or {}
    ship_id = data.get("spaceship_id")
    if not ship_id:
        return error("поле 'spaceship_id' обязательно")

    ship = spaceships.get(ship_id)
    if not ship:
        return error(f"корабль с id {ship_id} не найден", 404)

    if ship in mission.spaceships:
        return error(f"корабль '{ship.name}' уже в этой миссии")

    mission.add_spaceship(ship)
    return jsonify(mission.to_dict()), 200


@app.route("/api/v1/missions/<int:mission_id>/spaceships/<int:ship_id>", methods=["DELETE"])
def remove_spaceship_from_mission(mission_id, ship_id):
    mission = missions.get(mission_id)
    if not mission:
        return error(f"миссия с id {mission_id} не найдена", 404)

    ship = spaceships.get(ship_id)
    if not ship or ship not in mission.spaceships:
        return error(f"корабль с id {ship_id} не участвует в этой миссии", 404)

    mission.spaceships.remove(ship)
    return jsonify(mission.to_dict()), 200


@app.route("/api/v1/missions/<int:mission_id>", methods=["DELETE"])
def delete_mission(mission_id):
    if mission_id not in missions:
        return error(f"миссия с id {mission_id} не найдена", 404)
    missions.pop(mission_id)
    return jsonify({"message": f"миссия {mission_id} удалена"}), 200


# ============================================================
# Общие обработчики ошибок
# ============================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "ресурс не найден"}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "некорректный запрос"}), 400


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "внутренняя ошибка сервера"}), 500


# ============================================================
# Запуск
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)