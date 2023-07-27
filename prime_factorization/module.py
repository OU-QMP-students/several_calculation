import itertools

import numpy as np
import pandas as pd


class Combination:
    def __init__(self, char_sort: pd.DataFrame, target: list or np.ndarray) -> None:
        self.val = char_sort["E"].values.flatten()
        self.e = target[0]
        self.char_sort = char_sort

    def selection(self):
        selection = []
        min_s = min(self.val)
        for i, v in enumerate(self.val):
            array = self.val[: i + 1]
            total = sum(array)

            if total == self.e:
                selection.append(array)
                if np.all(array == min_s):
                    break

            elif total > self.e:
                for j in range(i):
                    if np.all(array == min_s):
                        break
                    array = self.val[j : i + 1]
                    total = sum(array)
                    if total == self.e:
                        selection.append(array)
                        break

                    elif total < self.e:
                        break
        return selection

    def combination(self):
        # main
        combinations = []
        for sel in self.selection():
            uni, count = np.unique(sel, return_counts=True)
            uni = dict(zip(uni, count))
            res = []
            for u, c in uni.items():
                ind = self.char_sort.loc[u].index.tolist()
                comb = list(itertools.combinations(ind, c))
                res.append(np.array(comb))
                if len(res) == 2:
                    gr1, gr2 = res
                    _gr1 = np.tile(gr1, (len(gr2), 1))
                    _gr2 = np.tile(gr2, len(gr1)).reshape(-1, gr2.shape[1])
                    k = np.hstack([_gr1, _gr2]).tolist()
                else:
                    k = res[0].tolist()
            combinations += k
        return combinations
