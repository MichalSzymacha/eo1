from typing import Tuple
import numpy as np
import numpy.typing as npt


"""
TODO:

-dodanie strategii elitarnej
algorytm genetyczny - zaimpelmentować samo wykonanie 
"""

class Individual:
    def __init__(self, size : int, vars_number : int, genes : npt.NDArray[np.int32] = None):
        self.size = size
        self.vars_number = vars_number
        self.genes_size = size * vars_number
        self.fitness = None
        if genes is not None:
            self.genes = genes
            if len(genes) != self.genes_size:
                raise ValueError(f"Genes size should be {self.genes_size}, but got {len(genes)}")
        else:
            self.genes = np.random.choice([0, 1], size=self.genes_size)

    def mutate_one_point(self):
            """
            Mutacja pojedynczego bitu
            """
            i = np.random.randint(self.genes_size)
            self.genes[i] = self.genes[i] ^ 1
    
    def mutate_two_point(self):
        """
        Mutacja dwóch punktów
        """
        i, j = np.random.choice(self.genes_size, 2, replace=False)
        self.genes[i] = self.genes[i] ^ 1
        self.genes[j] = self.genes[j] ^ 1

    def mutate_boundary(self):
        """
        Mutacja brzegowa
        """
        i = np.random.randint(self.genes_size)
        if i < self.size:
            self.genes[0] = self.genes[0] ^ 1
        else:
            self.genes[-1] = self.genes[-1] ^ 1
    
    def inversion(self):
        """
        Inwersja
        """
        i, j = np.random.choice(self.genes_size, 2, replace=False)
        if i > j:
            i, j = j, i
        for k in range((j-i)//2):
            self.genes[i+k], self.genes[j-k-1] = self.genes[j-k-1], self.genes[i+k]    

    def decode(self, var_bounds):
        genes = np.split(self.genes, self.vars_number)
        return [self.decode_gene(gene, var_bounds) for gene in genes]
        
    def decode_gene(self, gene, var_bounds):
        return var_bounds[0] + int("".join(map(str, gene)), 2) * (var_bounds[1] - var_bounds[0]) / (2**self.size - 1)

    def evaluate(self, objective_function, var_bounds):
        self.objective_value = objective_function(self.decode(var_bounds))
        self.fitness = self.objective_value



def func(x):
    return x[0] + x[1]

if __name__ == "__main__":
    ind = Individual(3, 2)

    print(ind.genes)
    ind.inversion()
    print(ind.genes)