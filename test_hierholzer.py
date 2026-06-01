import unittest

from hierholzer import (
    has_eulerian_cycle,
    find_eulerian_cycle,
    is_valid_eulerian_cycle,
)


class TestHierholzerAlgorithm(unittest.TestCase):

    def test_triangle(self):
        n = 3
        edges = [(0, 1), (1, 2), (2, 0)]

        cycle = find_eulerian_cycle(n, edges)

        self.assertTrue(has_eulerian_cycle(n, edges))
        self.assertTrue(is_valid_eulerian_cycle(n, edges, cycle))

    def test_parallel_edges(self):
        n = 2
        edges = [(0, 1), (0, 1)]

        cycle = find_eulerian_cycle(n, edges)

        self.assertTrue(has_eulerian_cycle(n, edges))
        self.assertTrue(is_valid_eulerian_cycle(n, edges, cycle))

    def test_not_eulerian_path_graph(self):
        n = 3
        edges = [(0, 1), (1, 2)]

        cycle = find_eulerian_cycle(n, edges)

        self.assertFalse(has_eulerian_cycle(n, edges))
        self.assertIsNone(cycle)

    def test_disconnected_graph_with_edges(self):
        n = 6
        edges = [
            (0, 1), (1, 2), (2, 0),
            (3, 4), (4, 5), (5, 3),
        ]

        cycle = find_eulerian_cycle(n, edges)

        self.assertFalse(has_eulerian_cycle(n, edges))
        self.assertIsNone(cycle)

    def test_single_vertex_without_edges(self):
        n = 1
        edges = []

        cycle = find_eulerian_cycle(n, edges)

        self.assertTrue(has_eulerian_cycle(n, edges))
        self.assertEqual(cycle, [0])

    def test_cycle_with_isolated_vertex(self):
        n = 4
        edges = [(0, 1), (1, 2), (2, 0)]

        cycle = find_eulerian_cycle(n, edges)

        self.assertTrue(has_eulerian_cycle(n, edges))
        self.assertTrue(is_valid_eulerian_cycle(n, edges, cycle))

    def test_eulerian_graph_with_five_vertices(self):
        n = 5
        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 0),
            (0, 2),
            (2, 4),
            (4, 0),
        ]
    
        cycle = find_eulerian_cycle(n, edges)
    
        self.assertTrue(has_eulerian_cycle(n, edges))
        self.assertTrue(is_valid_eulerian_cycle(n, edges, cycle))


if __name__ == "__main__":
    unittest.main()
