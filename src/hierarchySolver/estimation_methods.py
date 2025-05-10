from collections import deque
from time import perf_counter
from contextlib import contextmanager

#метод обхода графа в ширину
def bfs(start_node, count_depth=True, count_all=True):
    def bfs_inner(node):
        queue = deque([(node, 0)])
        total = 0
        max_d = 0

        while queue:
            current, depth = queue.popleft()

            total += 1
            max_d = max(max_d, depth)

            for node in current.links:
                queue.append((node, depth + 1))

        return max_d, total

    if not start_node:
        return None

    max_depth, total_nodes = bfs_inner(start_node)

    if count_depth and count_all:
        return max_depth, total_nodes
    elif count_depth:
        return max_depth
    elif count_all:
        return total_nodes
    else:
        return None

@contextmanager
def timer():
    start_time = perf_counter()
    elapsed_time = None
    yield lambda: elapsed_time
    end_time = perf_counter()
    elapsed_time = end_time - start_time