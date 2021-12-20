import random


class Chromosome:
    # initializing a chromosome with (gene_length) genes and contents from 0 to (contents_range)
    def __init__(self, num=1, gene_length=36, contents_range=36):
        self.gene_length = gene_length
        self.genes = []
        self.optimized = []
        self.contents = range(1, contents_range + 1)
        # set random genes to chromosome
        if num == 1:
            self.genes = random.sample(list(self.contents), self.gene_length)

    def calculate_fitness(self, selection_1: [], selection_2: [], selection_3: [], topic: []):
        # calculating fitness and optimized genes of current chromosome
        count1 = 0
        count2 = 0
        count3 = 0
        self.optimized = []
        for i in range(0, self.gene_length):
            if int(self.genes[i]) == int(selection_1[i]):
                count1 += 1
                self.optimized.append(1)
            elif int(self.genes[i]) == int(selection_2[i]):
                count2 += 1
                self.optimized.append(1)
            elif int(self.genes[i]) == int(selection_3[i]):
                count3 += 1
                self.optimized.append(1)
            elif topic[int(selection_1[i]) - 1] == topic[i] or topic[int(selection_2[i]) - 1] == topic[i] or \
                    topic[int(selection_3[i]) - 1] == topic[i]:
                self.optimized.append(1)
            else:
                self.optimized.append(0)
        total = count1 + count2 + count3

        # return the total fitness with a count for every selection of the current chromosome
        return [total, count1, count2, count3]
