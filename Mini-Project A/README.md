# Reusable Graph Toolkit with Tests

## Overview

A reusable Python graph toolkit that supports directed and undirected graphs, weighted edges, JSON input, and graph search algorithms.

## Features

- Create directed and undirected graphs.
- Add weighted edges with input validation.
- Retrieve the neighbors of a node.
- Build a graph from JSON text.
- Find paths using Breadth-First Search (BFS).
- Find minimum-cost paths using Dijkstra's algorithm.
- Find paths using A* search.
- Run automated unit tests using Python's `unittest`.
- Measure test coverage using Coverage.py.

## Project Structure

```text
project/
├── iskit/
│   ├── __init__.py
│   └── graph.py
├── tests/
│   └── test_graph.py
├── demo.py
└── README.md
```

## Requirements

- Python 3.9 or later.
- No external dependencies are required to use the graph toolkit or run its unit tests.
- Coverage.py is optional and is only required for measuring test coverage.

## Usage

```python
from iskit.graph import Graph

graph = Graph(directed=False)

graph.add_edge("A", "B", 2)
graph.add_edge("B", "C", 3)
graph.add_edge("A", "C", 7)

path, expanded = graph.bfs("A", "C")
print("BFS:", path)

path, cost = graph.dijkstra("A", "C")
print("Dijkstra:", path, cost)

path, cost = graph.astar("A", "C", lambda node: 0)
print("A*:", path, cost)
```

BFS returns the path and the number of expanded nodes. Dijkstra and A* return the path and its total cost.

## Loading a Graph from JSON

```python
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
```

Each edge contains two nodes and an optional weight. If the weight is omitted, it defaults to `1.0`.

## Running the Demo

```bash
python demo.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Measuring Test Coverage

Install Coverage.py:

```bash
python -m pip install coverage
```

Run the tests with coverage:

```bash
python -m coverage run -m unittest discover -s tests
python -m coverage report -m
```

Generate an HTML coverage report:

```bash
python -m coverage html
```

The HTML report is generated in the `htmlcov/` directory.

## Algorithm Notes

- **BFS:** Finds a path with the fewest edges; it does not necessarily minimize total weight.
- **Dijkstra:** Finds a minimum-cost path when edge weights are non-negative.
- **A\*:** Uses the accumulated path cost and a heuristic estimate to guide the search. Its optimality depends on the heuristic and the implementation's search behavior.

## Validation and Testing

The toolkit validates edge weights and checks the structure of JSON input. Automated unit tests cover graph construction, edge validation, JSON parsing, and pathfinding behavior.

The current test suite contains 19 tests. In the latest recorded run, all 19 tests passed. The reported coverage for `iskit/graph.py` was 96%.

Coverage results may vary when the test suite or implementation changes.