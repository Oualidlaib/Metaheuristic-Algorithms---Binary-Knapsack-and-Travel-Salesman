import numpy as np
from knapsack.knapsack_strategy import Strategy


class DeterministicGreedyStrategy(Strategy):

    def solve(self, instance: dict) -> dict:
        
        n_items = instance["profits"].shape[0]
        
        profits = instance["profits"]
        weights = instance["weights"]
        W = instance["capacity"]
        
        # Calculate ratios and sort indices descending
        ratios = profits / weights
        sorted_indices = np.argsort(-ratios)

        w = 0
        decision_array = np.zeros(n_items)

        for idx in sorted_indices:
            if w + weights[idx] <= W:
                decision_array[idx] = 1
                w += weights[idx]

        # Final profit calculation using the decision mask
        max_profit = np.dot(profits, decision_array)

        return {
            "profit": max_profit,
            "weight": w,
            "decision": decision_array
        }







        

