import numpy as np
from knapsack.knapsack_strategy import Strategy


class NonDeterministicGreedyStrategy(Strategy):

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

        n = sorted_indices.shape[0]
        while w <= W and n > 0:

            if n >= 3:
                # Choose between 0, 1, or 2
                choice = np.random.randint(0, 3) 
            elif n == 2:
                # Choose between 0 or 1
                choice = np.random.randint(0, 2)
            else:
                # Handle the case where size is 1
                choice = 0
            
            if w + weights[sorted_indices[choice]] <= W:

                decision_array[sorted_indices[choice]] = 1
                w += weights[sorted_indices[choice]]
            
            sorted_indices = np.delete(sorted_indices, choice)
            n -= 1

        # Final profit calculation using the decision mask
        max_profit = np.dot(profits, decision_array)

        return {
            "profit": max_profit,
            "weight": w,
            "decision": decision_array
        }