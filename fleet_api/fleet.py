# ============================================================
# Класс 1. Космический корабль
# ============================================================
class Spaceship:
    # Разрешённые статусы. Кортеж — чтобы никто случайно не поменял список.
    STATUSES = ("available", "in_mission", "under_repair")

    def __init__(self, spaceship_id, name, type_, status="available"):
        self.spaceship_id = spaceship_id   # номер корабля
        self.name = name                   # название
        self.type_ = type_                 # "research" или "combat"
        self.status = status               # по умолчанию "available"

    def update_status(self, new_status):
        # Если статус непонятный — ругаемся и не меняем ничего
        if new_status not in self.STATUSES:
            raise ValueError(f"нет такого статуса: {new_status!r}, можно: {self.STATUSES}")
        self.status = new_status

    def to_dict(self):
        # Превращаем объект в словарь — пригодится для JSON во Flask
        return {
            "id": self.spaceship_id,
            "name": self.name,
            "type": self.type_,
            "status": self.status,
        }

    def __repr__(self):
        # Чтобы print(ship) показывал нормальную строку
        return (f"Spaceship(id={self.spaceship_id}, name={self.name!r}, "
                f"type={self.type_!r}, status={self.status!r})")


# ============================================================
# Класс 2. Миссия
# ============================================================
class Mission:
    # Разрешённые статусы миссии
    STATUSES = ("planned", "in_progress", "completed")

    def __init__(self, mission_id, name, goal, status="planned"):
        self.mission_id = mission_id
        self.name = name
        self.goal = goal                # "research" или "defense"
        self.status = status            # по умолчанию "planned"
        self.spaceships = []            # сюда складываем корабли миссии

    def add_spaceship(self, spaceship):
        # Проверяем, что дали именно корабль, а не что-то другое
        if not isinstance(spaceship, Spaceship):
            raise TypeError(f"ждали Spaceship, а пришло {type(spaceship).__name__}")
        # Если такой корабль уже есть — второй раз не добавляем
        if spaceship in self.spaceships:
            return
        self.spaceships.append(spaceship)

    def update_status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError(f"нет такого статуса: {new_status!r}, можно: {self.STATUSES}")
        self.status = new_status

    def to_dict(self):
        # Список id кораблей — так JSON получается короче и понятнее
        return {
            "id": self.mission_id,
            "name": self.name,
            "goal": self.goal,
            "status": self.status,
            "spaceship_ids": [s.spaceship_id for s in self.spaceships],
        }

    def __repr__(self):
        ships = ", ".join(s.name for s in self.spaceships) or "—"
        return (f"Mission(id={self.mission_id}, name={self.name!r}, "
                f"goal={self.goal!r}, status={self.status!r}, ships=[{ships}])")


# ============================================================
# Класс 3. Член экипажа
# ============================================================
class CrewMember:
    # Разрешённые роли
    ROLES = ("captain", "engineer", "pilot")

    def __init__(self, member_id, name, role):
        # Роль проверяем сразу — потом можно спокойно на неё рассчитывать
        if role not in self.ROLES:
            raise ValueError(f"нет такой роли: {role!r}, можно: {self.ROLES}")
        self.member_id = member_id
        self.name = name
        self.role = role

    def to_dict(self):
        return {
            "id": self.member_id,
            "name": self.name,
            "role": self.role,
        }

    def __repr__(self):
        return f"CrewMember(id={self.member_id}, name={self.name!r}, role={self.role!r})"


# ============================================================
# Быстрая проверка, что всё работает (запускается только напрямую)
# ============================================================
if __name__ == "__main__":
    ship1 = Spaceship(1, "Аврора", "research")
    ship2 = Spaceship(2, "Титан", "combat")

    mission = Mission(101, "Патруль окраин", "defense")
    mission.add_spaceship(ship1)
    mission.add_spaceship(ship2)

    captain = CrewMember(1, "Иван Петров", "captain")

    for obj in (ship1, ship2, mission, captain):
        print(obj)