# Лабораторная работа 4, про тома и рюкзак плюс доп задания
# Вариант 10: инвентарь 3x3 (9 ячеек), болезни нет, стартовые очки = 10


class Item:
    def __init__(self, name, symbol, size, points):
        self.name = name        # название предмета
        self.symbol = symbol    # обозначение в инвентаре
        self.size = size        # сколько ячеек занимает
        self.points = points    # очки выживания


# Таблица предметов из задания
ALL_ITEMS = [
    Item("rifle", "r", 3, 25),
    Item("pistol", "p", 2, 15),
    Item("ammo", "a", 2, 15),
    Item("medkit", "m", 2, 20),
    Item("inhaler", "i", 1, 5),
    Item("knife", "k", 1, 15),
    Item("axe", "x", 3, 20),
    Item("talisman", "t", 1, 25),
    Item("flask", "f", 1, 15),
    Item("antidot", "d", 1, 10),
    Item("supplies", "s", 2, 20),
    Item("crossbow", "c", 2, 20),
]

# Параметры варианта 10
ROWS = 3
COLS = 3
START_POINTS = 10
DISEASE = "нет"     # "нет", "астма" или "паранойя"


def total_points(items):
    # сумма очков всех предметов (нужна для штрафа за оставленные вещи)
    s = 0
    for item in items:
        s += item.points
    return s


def final_score(taken, items, start):
    # взятые предметы прибавляют очки, оставленные - вычитают
    taken_sum = 0
    for item in taken:
        taken_sum += item.points
    left_sum = total_points(items) - taken_sum
    return start + taken_sum - left_sum


def knapsack(items, capacity, required=None):
    # Метод ветвей и границ брала как из примера 
    # Так как итоговый счёт = start + 2 * (взятые очки) - (сумма всех очков),
    # то максимизировать итоговый счёт то же самое, что максимизировать
    # сумму очков взятых предметов.
    # required - предмет, который обязательно должен быть в рюкзаке

    start_taken = []
    start_size = 0
    start_value = 0
    rest = []
    for item in items:
        if required is not None and item.name == required:
            start_taken.append(item)
            start_size += item.size
            start_value += item.points
        else:
            rest.append(item)

    if start_size > capacity:
        return None, None   # обязательный предмет не помещается

    # сортируем по ценности одной ячейки (по убыванию)
    rest = sorted(rest, key=lambda x: x.points / x.size, reverse=True)

    best = {"value": -1, "items": []}

    def bound(i, size, value):
        # верхняя оценка: добираем предметы по порядку, последний - дробно
        j = i
        while j < len(rest) and size + rest[j].size <= capacity:
            size += rest[j].size
            value += rest[j].points
            j += 1
        if j < len(rest):
            value += (capacity - size) * (rest[j].points / rest[j].size)
        return value

    def branch_bound(i, size, value, taken):
        if size <= capacity and value > best["value"]:
            best["value"] = value
            best["items"] = list(taken)
        if i == len(rest):
            return
        if bound(i, size, value) <= best["value"]:
            return  # дальше искать нет смысла
        # ветка 1: берём предмет
        if size + rest[i].size <= capacity:
            taken.append(rest[i])
            branch_bound(i + 1, size + rest[i].size, value + rest[i].points, taken)
            taken.pop()
        # ветка 2: не берём предмет
        branch_bound(i + 1, size, value, taken)

    branch_bound(0, start_size, start_value, list(start_taken))
    return best["value"], best["items"]


def print_inventory(taken, rows, cols):
    # заполняем ячейки по порядку: предмет размера n занимает n ячеек
    cells = []
    for item in taken:
        for _ in range(item.size):
            cells.append("[" + item.symbol + "]")
    while len(cells) < rows * cols:
        cells.append("[ ]")   # пустая ячейка
    for r in range(rows):
        print(",".join(cells[r * cols:(r + 1) * cols]))


def solve(capacity, rows, cols, start, disease):
    required = None
    if disease == "астма":
        required = "inhaler"
    elif disease == "паранойя":
        required = "antidot"

    value, taken = knapsack(ALL_ITEMS, capacity, required)
    if taken is None:
        print("Решения нет: обязательный предмет не помещается.")
        return
    score = final_score(taken, ALL_ITEMS, start)

    print("Взято предметов:", ", ".join(i.name for i in taken))
    print()
    print_inventory(taken, rows, cols)
    print()
    print("Итоговые очки выживания:", score)
    if score > 0:
        print("Счёт положительный - Том дойдёт до вышки!")
    else:
        print("Счёт НЕ положительный - решения нет.")


def all_combinations(capacity, start):
    # Допзадание: перебираем все 2^12 наборов предметов
    # и оставляем те, что помещаются и дают положительный счёт
    n = len(ALL_ITEMS)
    result = []
    for mask in range(2 ** n):
        taken = []
        size = 0
        for k in range(n):
            if mask & (1 << k):
                taken.append(ALL_ITEMS[k])
                size += ALL_ITEMS[k].size
        if size > capacity:
            continue
        score = final_score(taken, ALL_ITEMS, start)
        if score > 0:
            result.append((score, size, taken))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


if __name__ == '__main__':
    capacity = ROWS * COLS

    print("=== Основное задание: вариант 10 (3x3, без болезни, 10 очков) ===")
    solve(capacity, ROWS, COLS, START_POINTS, DISEASE)

    print()
    print("=== Допзадание 1: инвентарь на 7 ячеек ===")
    # 7 ячеек не раскладываются на сетку, поэтому выводим одной строкой 1x7
    solve(7, 1, 7, START_POINTS, DISEASE)

    print()
    print("=== Допзадание 2: все комбинации с положительным счётом (3x3) ===")
    combos = all_combinations(capacity, START_POINTS)
    print("Всего комбинаций:", len(combos))
    num = 1
    for score, size, taken in combos:
        names = ",".join(i.symbol for i in taken)
        print(str(num) + ") [" + names + "]  ячеек: " + str(size) + ", очки: " + str(score))
        num += 1
