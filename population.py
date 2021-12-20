from chromosome import Chromosome


class Population(object):
    # initializing the population by adding (size) chromosomes with (gene_length) genes and contents from 0 to (
    # contents_range)
    def __init__(self, size=10, gene_length=36, contents_range=36):
        self.population_size = size
        self.chromosomes = []
        for i in range(0, self.population_size):
            self.chromosomes.append(Chromosome(gene_length=gene_length, contents_range=contents_range))

    # Sorting the population according to every chromosome's fitness
    def sort_population(self, fitness):
        n = len(fitness)

        for i in range(0, n - 1):
            for j in range(0, n - i - 1):
                total_1 = (fitness[j][1] * 1000) + (fitness[j][2] * 50) + (fitness[j][3])
                total_2 = (fitness[j+1][1] * 1000) + (fitness[j+1][2] * 50) + (fitness[j+1][3])
                if fitness[j][0] < fitness[j + 1][0] or (fitness[j][0] == fitness[j + 1][0] and total_1 < total_2):
                    fitness[j], fitness[j + 1] = fitness[j + 1], fitness[j]
                    self.chromosomes[j], self.chromosomes[j + 1] = self.chromosomes[j + 1], self.chromosomes[j]
