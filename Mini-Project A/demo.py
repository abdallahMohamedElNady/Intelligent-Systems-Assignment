
from iskit.graph import Graph

data = """
{
    "directed": false,
    "edges": [
        ["A", "B", 2],
        ["B", "C", 3],
        ["A", "C", 7]
    ]
}
"""

graph = Graph.from_json(data)

bfs_path, expanded = graph.bfs("A", "C")
print("BFS path:", bfs_path)
print("Nodes expanded:", expanded)

dijkstra_path, cost = graph.dijkstra("A", "C")
print("Dijkstra path:", dijkstra_path)
print("Dijkstra cost:", cost)

astar_path, astar_cost = graph.astar(
    "A", "C", lambda node: 0
)
print("A* path:", astar_path)
print("A* cost:", astar_cost)
