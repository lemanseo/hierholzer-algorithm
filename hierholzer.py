from collections import deque

def build_adjacency(n, edges):
    """
    Строит список смежности для неориентированного мультиграфа.

    Каждому ребру присваивается уникальный номер edge_id.
    Нужно, чтобы различать параллельные рёбра между одной
    и той же парой вершин.
    """
    adj = [[] for _ in range(n)]

    for edge_id, (u, v) in enumerate(edges):
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("Номер вершины превышает границу")

        # Так как граф неориентированный, добавляем ребро в оба списка.
        adj[u].append((v, edge_id))
        adj[v].append((u, edge_id))

    return adj


def has_eulerian_cycle(n, edges):
    """
    Проверяет критерий Эйлера для неориентированного мультиграфа.

    Эйлеров цикл существует тогда и только тогда, когда:
    1. все вершины ненулевой степени лежат в одной компоненте связности
    2. степени всех вершин чётные.
    """
    if n <= 0:
        return len(edges) == 0

    adj = build_adjacency(n, edges)
    degree = [len(adj[v]) for v in range(n)]

    # Проверяем чётность степеней всех вершин.
    for v in range(n):
        if degree[v] % 2 != 0:
            return False

    # Находим любую вершину, у которой есть хотя бы одно ребро.
    # Изолированные вершины не мешают эйлерову циклу.
    start = None
    for v in range(n):
        if degree[v] > 0:
            start = v
            break

    # Если рёбер нет, эйлеров цикл тривиальный.
    if start is None:
        return True

    # Проверяем связность всех вершин ненулевой степени с помощью BFS.
    visited = [False] * n
    queue = deque([start])
    visited[start] = True

    while queue:
        v = queue.popleft()

        for to, _ in adj[v]:
            if not visited[to]:
                visited[to] = True
                queue.append(to)

    # Есть ли непосещенные вершины с ребрами
    for v in range(n):
        if degree[v] > 0 and not visited[v]:
            return False

    return True


def find_eulerian_cycle(n, edges):
    """
    Ищет эйлеров цикл с помощью алгоритма Хирхольцера.

    Если эйлеров цикл существует, возвращает список вершин в порядке обхода.
    Если эйлерова цикла нет, возвращает None.
    """
    if not has_eulerian_cycle(n, edges):
        return None

    if n == 0:
        return []

    if len(edges) == 0:
        return [0]

    adj = build_adjacency(n, edges)

    # used[edge_id] показывает, было ли ребро уже использовано.
    used = [False] * len(edges)

    # ptr[v] хранит индекс первого ещё не проверенного ребра в списке смежности v.
    # Это позволяет не просматривать использованные рёбра заново с самого начала.
    ptr = [0] * n

    # Стартуем из любой вершины ненулевой степени.
    start = 0
    for v in range(n):
        if len(adj[v]) > 0:
            start = v
            break

    # stack хранит текущий путь алгоритма.
    # answer хранит вершины итогового цикла в обратном порядке.
    stack = [start]
    answer = []

    while stack:
        v = stack[-1]

        # Пропускаем уже использованные рёбра.
        while ptr[v] < len(adj[v]) and used[adj[v][ptr[v]][1]]:
            ptr[v] += 1

        # Если из вершины больше нет неиспользованных рёбер,
        # она завершена и переносится в ответ.
        if ptr[v] == len(adj[v]):
            answer.append(v)
            stack.pop()
        else:
            # Иначе идём по найденному неиспользованному ребру.
            to, edge_id = adj[v][ptr[v]]
            used[edge_id] = True
            stack.append(to)

    # Ответ был построен в обратном порядке, поэтому разворачиваем его.
    answer.reverse()
    return answer


def is_valid_eulerian_cycle(n, edges, cycle):
    """
    Вспомогательная функция для тестов.

    Проверяет, что найденный цикл:
    1) замкнут
    2) имеет правильную длину
    3) использует каждое ребро исходного графа ровно один раз.
    """
    if cycle is None:
        return False

    if len(edges) == 0:
        return cycle == [] or len(cycle) == 1

    # В эйлеровом цикле количество вершин в записи маршрута
    # должно быть на 1 больше количества рёбер.
    if len(cycle) != len(edges) + 1:
        return False

    # Цикл должен начинаться и заканчиваться в одной вершине.
    if cycle[0] != cycle[-1]:
        return False

    # Считаем, сколько раз каждое неориентированное ребро есть в графе.
    # Для мультиграфа важно хранить количество одинаковых рёбер.
    unused = {}
    for u, v in edges:
        key = tuple(sorted((u, v)))
        unused[key] = unused.get(key, 0) + 1

    # Каждый переход в цикле должен соответствовать существующему ребру.
    for i in range(len(cycle) - 1):
        u = cycle[i]
        v = cycle[i + 1]
        key = tuple(sorted((u, v)))

        if unused.get(key, 0) == 0:
            return False

        unused[key] -= 1

    # Все рёбра должны быть использованы ровно один раз.
    return all(count == 0 for count in unused.values())

