
import json
import math
import heapq
from collections import deque


class Graph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_edge(self, u, v, w=1.0):
        """Add an edge with a finite, non-negative weight."""

        if (
            not isinstance(w, (int, float))
            or isinstance(w, bool)
            or not math.isfinite(w)
            or w < 0
        ):
            raise ValueError(
                "Weight must be a finite, non-negative number"
            )

        self.adj.setdefault(u, {})
        self.adj.setdefault(v, {})

        self.adj[u][v] = float(w)

        if not self.directed:
            self.adj[v][u] = float(w)

    def neighbors(self, u):
        """Return neighbors and their edge weights."""
        return self.adj.get(u, {}).items()

    @classmethod
    def from_json(cls, text):
        """Create a graph from JSON text."""

        try:
            data = json.loads(text)
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError("Invalid JSON text") from exc

        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")

        directed = data.get("directed", False)
        edges = data.get("edges")

        if not isinstance(directed, bool):
            raise ValueError("'directed' must be a boolean")

        if not isinstance(edges, list):
            raise ValueError("'edges' must be a list")

        graph = cls(directed=directed)

        for edge in edges:
            if not isinstance(edge, list) or len(edge) not in (2, 3):
                raise ValueError(
                    "Each edge must have 2 or 3 items"
                )

            u, v = edge[0], edge[1]
            weight = edge[2] if len(edge) == 3 else 1.0

            graph.add_edge(u, v, weight)

        return graph

    def bfs(self, s, goal):
        """Find a path with the fewest edges using BFS."""

        if s not in self.adj or goal not in self.adj:
            return None, 0

        queue = deque([s])
        parent = {s: None}
        nodes_expanded = 0

        while queue:
            node = queue.popleft()
            nodes_expanded += 1

            if node == goal:
                path = []
                current = goal

                while current is not None:
                    path.append(current)
                    current = parent[current]

                return path[::-1], nodes_expanded

            for neighbor, weight in self.neighbors(node):
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)

        return None, nodes_expanded

    def dijkstra(self, s, goal):
        """Find the lowest-cost path using Dijkstra's algorithm."""

        if s not in self.adj or goal not in self.adj:
            return None, math.inf

        distances = {s: 0.0}
        parent = {s: None}
        priority_queue = [(0.0, 0, s)]
        counter = 0

        while priority_queue:
            cost, _, node = heapq.heappop(priority_queue)

            # Ignore outdated entries.
            if cost > distances.get(node, math.inf):
                continue

            if node == goal:
                path = []
                current = goal

                while current is not None:
                    path.append(current)
                    current = parent[current]

                return path[::-1], cost

            for neighbor, weight in self.neighbors(node):
                new_cost = cost + weight

                if new_cost < distances.get(neighbor, math.inf):
                    distances[neighbor] = new_cost
                    parent[neighbor] = node
                    counter += 1

                    heapq.heappush(
                        priority_queue,
                        (new_cost, counter, neighbor)
                    )

        return None, math.inf

    def astar(self, s, goal, h):
        """Find a lowest-cost path using A*."""

        if s not in self.adj or goal not in self.adj:
            return None, math.inf

        start_h = h(s)

        if (
            not isinstance(start_h, (int, float))
            or isinstance(start_h, bool)
            or not math.isfinite(start_h)
            or start_h < 0
        ):
            raise ValueError(
                "Heuristic must be finite and non-negative"
            )

        g_score = {s: 0.0}
        parent = {s: None}
        priority_queue = [(start_h, 0, s)]
        counter = 0

        while priority_queue:
            f_score, _, current = heapq.heappop(priority_queue)

            # Ignore outdated entries.
            expected_f = g_score[current] + h(current)

            if f_score > expected_f:
                continue

            if current == goal:
                path = []
                node = goal

                while node is not None:
                    path.append(node)
                    node = parent[node]

                return path[::-1], g_score[goal]

            for neighbor, weight in self.neighbors(current):
                new_cost = g_score[current] + weight

                if new_cost < g_score.get(neighbor, math.inf):
                    heuristic = h(neighbor)

                    if (
                        not isinstance(heuristic, (int, float))
                        or isinstance(heuristic, bool)
                        or not math.isfinite(heuristic)
                        or heuristic < 0
                    ):
                        raise ValueError(
                            "Heuristic must be finite and non-negative"
                        )

                    g_score[neighbor] = new_cost
                    parent[neighbor] = current
                    counter += 1

                    heapq.heappush(
                        priority_queue,
                        (
                            new_cost + heuristic,
                            counter,
                            neighbor
                        )
                    )

        return None, math.inf
