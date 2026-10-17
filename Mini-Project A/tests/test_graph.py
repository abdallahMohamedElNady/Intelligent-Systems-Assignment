
import unittest
import math

from iskit.graph import Graph


class TestGraph(unittest.TestCase):

    def test_add_edge_undirected(self):
        graph = Graph()
        graph.add_edge("A", "B", 2)

        self.assertEqual(graph.adj["A"]["B"], 2.0)
        self.assertEqual(graph.adj["B"]["A"], 2.0)

    def test_add_edge_directed(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "B", 3)

        self.assertIn("B", graph.adj["A"])
        self.assertNotIn("A", graph.adj["B"])

    def test_negative_weight(self):
        graph = Graph()

        with self.assertRaises(ValueError):
            graph.add_edge("A", "B", -1)

    def test_neighbors(self):
        graph = Graph()
        graph.add_edge("A", "B", 2)
        graph.add_edge("A", "C", 3)

        self.assertEqual(
            dict(graph.neighbors("A")),
            {"B": 2.0, "C": 3.0}
        )

    def test_from_json(self):
        data = '''
        {
            "directed": false,
            "edges": [
                ["A", "B", 2],
                ["B", "C", 3]
            ]
        }
        '''

        graph = Graph.from_json(data)

        self.assertEqual(graph.adj["A"]["B"], 2.0)
        self.assertEqual(graph.adj["C"]["B"], 3.0)

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            Graph.from_json("not json")

    def test_bfs(self):
        graph = Graph()
        graph.add_edge("A", "B", 2)
        graph.add_edge("B", "C", 3)
        graph.add_edge("A", "C", 7)

        path, expanded = graph.bfs("A", "C")

        self.assertEqual(path, ["A", "C"])
        self.assertGreater(expanded, 0)

    def test_bfs_no_path(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("C", "D", 1)

        path, expanded = graph.bfs("A", "D")

        self.assertIsNone(path)
        self.assertGreater(expanded, 0)

    def test_dijkstra(self):
        graph = Graph()
        graph.add_edge("A", "B", 2)
        graph.add_edge("B", "C", 3)
        graph.add_edge("A", "C", 7)

        path, cost = graph.dijkstra("A", "C")

        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 5.0)

    def test_dijkstra_no_path(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("C", "D", 1)

        path, cost = graph.dijkstra("A", "D")

        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_astar(self):
        graph = Graph()
        graph.add_edge("A", "B", 2)
        graph.add_edge("B", "C", 3)
        graph.add_edge("A", "C", 7)

        path, cost = graph.astar(
            "A", "C", lambda node: 0
        )

        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 5.0)

    def test_astar_no_path(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("C", "D", 1)

        path, cost = graph.astar(
            "A", "D", lambda node: 0
        )

        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_from_json_invalid_directed(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"directed": "yes", "edges": []}')

    def test_from_json_invalid_edges(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"edges": "not a list"}')

    def test_from_json_invalid_edge_format(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"edges": [["A"]]}')

    def test_dijkstra_missing_node(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)

        path, cost = graph.dijkstra("A", "Z")
        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_astar_missing_node(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)

        path, cost = graph.astar("A", "Z", lambda node: 0)
        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_astar_invalid_heuristic(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)

        for invalid_value in [-1, float("inf"), float("nan"), True, "invalid"]:
            with self.subTest(value=invalid_value):
                with self.assertRaises(ValueError):
                    graph.astar("A", "B", lambda node: invalid_value)

    def test_dijkstra_ignores_outdated_queue_entries(self):
        graph = Graph()
        graph.add_edge("A", "B", 10)
        graph.add_edge("A", "C", 1)
        graph.add_edge("C", "B", 1)
        graph.add_edge("B", "D", 1)

        path, cost = graph.dijkstra("A", "D")
        self.assertEqual(path, ["A", "C", "B", "D"])
        self.assertEqual(cost, 3.0)


if __name__ == "__main__":
    unittest.main()

    def test_zero_weight_edge(self):
        graph = Graph()
        graph.add_edge("A", "B", 0)
        graph.add_edge("B", "C", 2)

        path, cost = graph.dijkstra("A", "C")

        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2.0)

    def test_same_start_and_goal(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)

        path, cost = graph.dijkstra("A", "A")

        self.assertEqual(path, ["A"])
        self.assertEqual(cost, 0.0)

    def test_directed_graph_no_reverse_path(self):
        graph = Graph(directed=True)
        graph.add_edge("A", "B", 1)

        path, cost = graph.dijkstra("B", "A")

        self.assertIsNone(path)
        self.assertTrue(math.isinf(cost))

    def test_invalid_weights(self):
        graph = Graph()

        for weight in [-1, float("inf"), float("nan"), True]:
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError):
                    graph.add_edge("A", "B", weight)

    def test_default_edge_weight_from_json(self):
        data = '{"edges": [["A", "B"]]}'
        graph = Graph.from_json(data)

        self.assertEqual(graph.adj["A"]["B"], 1.0)
        self.assertEqual(graph.adj["B"]["A"], 1.0)

    def test_astar_with_heuristic(self):
        graph = Graph()
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        graph.add_edge("A", "C", 5)

        heuristic = {"A": 2, "B": 1, "C": 0}

        path, cost = graph.astar(
            "A", "C", lambda node: heuristic[node]
        )

        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 2.0)
