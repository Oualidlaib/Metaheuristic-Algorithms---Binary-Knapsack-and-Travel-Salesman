import numpy as np
from tsp.tsp_strategy import Strategy
from tsp.nondeterministic_greedy import NonDeterministicGreedyStrategy


class GeneticStrategy(Strategy):

    def selectOperator(self, solutions):
        """
        Tournament selection: keeps 50% of the population.
        """
        selected = []
        target = len(solutions) // 2

        for _ in range(target):
            i, j = np.random.choice(len(solutions), size=2, replace=False)
            d_i = solutions[i]["distance"]
            d_j = solutions[j]["distance"]

            winner = solutions[i] if d_i < d_j else solutions[j]
            selected.append(winner)
 
        return selected

    def crossover(self, solutions):
        """
        Ordered Crossover (OX) with a single cut-point (split into 2 segments).
        """
        children = []
        indices = list(range(len(solutions)))
        np.random.shuffle(indices)

        def ox(parent_a, parent_b, cut):
            """OX with a single cut point."""
            segment = parent_a[:cut]
            in_segment = set(segment)
            tail = [city for city in parent_b if city not in in_segment]
            return segment + tail

        for idx in range(0, len(indices) - 1, 2):
            p1 = solutions[indices[idx]]["path"]
            p2 = solutions[indices[idx + 1]]["path"]

            # Starting city
            depot = p1[0] 

            # Strip depot from both ends 
            p1_inner = p1[1:-1]
            p2_inner = p2[1:-1]
            n = len(p1_inner)

            # Random cut point inside the interior
            k = np.random.randint(1, n - 1)

            child1_inner = ox(p1_inner, p2_inner, k)
            child2_inner = ox(p2_inner, p1_inner, k)

            # Re-attach depot at both ends to close the tour
            children.append([depot] + child1_inner + [depot])
            children.append([depot] + child2_inner + [depot])

        return children

    def mutate(self, children, mutation_rate=0.05):
        """
        Swap mutation applied to ~1% of the children.
        """
        mutated = []
        for path in children:
            path = list(path)
            if np.random.random() < mutation_rate:
                
                i, j = np.random.choice(range(1, len(path) - 1), size=2, replace=False)

                # Swap two cities
                path[i], path[j] = path[j], path[i]

            mutated.append(path)

        return mutated

    def _path_to_solution(self, path, instance):
        """
        Compute the total distance of a closed path and return a solution dict.
        """
        total = 0.0
        for i in range(len(path) - 1):
            total += instance[path[i]][path[i + 1]]
        return {"distance": total, "path": path}

    def best_path(self, solutions):
        """Return the solution dict with the smallest distance."""
        return min(solutions, key=lambda s: s["distance"])

    def solve(self, instance: np.ndarray) -> dict:

        MAX_ITERATION = 1000

        # Generate initial population ONCE before the loop
        solutions = []
        for _ in range(500):
            nondeterministic_greedy = NonDeterministicGreedyStrategy()
            solution = nondeterministic_greedy.solve(instance)
            solutions.append(solution)

        prev_best    = {"distance": np.inf, "path": None}
        current_best = {"distance": np.inf, "path": None}
        best = current_best
        # Evolve the population across iterations
        for i in range(MAX_ITERATION):

            # Selection (keep 50% of the population using Tounrnament strategy)
            selected = self.selectOperator(solutions)

            # Crossover
            child_paths = self.crossover(selected)

            # Perturb ~5% of children
            child_paths = self.mutate(child_paths)

            # Convert child paths to solution dictionaries
            children = [self._path_to_solution(p, instance) for p in child_paths]

            # Merge selected parents + children, cap at 1000 (keep the fittest)
            combined = selected + children
            combined.sort(key=lambda s: s["distance"])
            solutions = combined[:1000]

            current_best = self.best_path(solutions)

            if current_best['distance'] < best['distance']:
                best = current_best

        return {"distance": best["distance"], "path": best["path"]}