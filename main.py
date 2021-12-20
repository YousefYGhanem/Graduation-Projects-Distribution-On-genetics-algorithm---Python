import csv
import random
import threading

from chromosome import Chromosome
from population import Population
import PySimpleGUI as sg

print("Starting Program...")

# Global Variables
iterations_count: int
generation_count: int
opti_count: int
best_iteration: Chromosome(0)
best_fitness: [int]
kill = False
browse_groups = sg.FileBrowse('Browse Groups File')
browse_projects = sg.FileBrowse('Browse Projects File')

Stud_names: list
selection_1: list
selection_2: list
selection_3: list

doctors: list
proj_title: list
topic: list


#######################
# Logs file Write
def write_log(log: str):
    with open(r"Logs.txt", "a") as logs_file:
        logs_file.write(log + '\n')
    logs_file.close()


###############################################

# crossover function (Takes the current population and adds the children to best_fit list)
def crossover(population, best_fit):
    n = 2

    while n < population.population_size:
        crossover_point = random.randint(1, population.chromosomes[n].gene_length - 1)
        child1 = Chromosome(0, len(selection_1), len(doctors))
        child2 = Chromosome(0, len(selection_1), len(doctors))
        # parents index
        c1_index = random.randint(1, int(population.population_size / 2))
        c2_index = random.randint(1, int(population.population_size / 2))

        child1.genes[0:crossover_point] = population.chromosomes[c1_index].genes[0:crossover_point]
        child2.genes[0:crossover_point] = population.chromosomes[c2_index].genes[0:crossover_point]

        for i in range(crossover_point, child2.gene_length):
            if population.chromosomes[c1_index].genes[i] not in child2.genes:
                child2.genes.append(population.chromosomes[c1_index].genes[i])
            else:
                for m in child2.contents:
                    if m not in child2.genes:
                        child2.genes.append(m)
                        break
            if population.chromosomes[c2_index].genes[i] not in child1.genes:
                child1.genes.append(population.chromosomes[c2_index].genes[i])
            else:
                for m in child1.contents:
                    if m not in child1.genes:
                        child1.genes.append(m)
                        break

        child1 = mutate(child1)
        child2 = mutate(child2)

        best_fit.append(child1)
        best_fit.append(child2)

        n += 2
    for k in range(0, population.population_size):
        population.chromosomes[k] = best_fit[k]


################################################################

# mutation function
def mutate(ch: Chromosome):
    ch.calculate_fitness(selection_1, selection_2, selection_3, topic)
    while True:
        a = random.randint(1, ch.gene_length - 1)
        b = random.randint(1, ch.gene_length - 1)
        if ch.optimized[a] == 0 or ch.optimized[b] == 0:
            ch.genes[a], ch.genes[b] = ch.genes[b], ch.genes[a]
            break

    # first implementation:
    # a = random.randint(1, ch.gene_length - 1)
    # b = random.randint(1, ch.gene_length - 1)
    # ch.genes[a], ch.genes[b] = ch.genes[b], ch.genes[a]
    return ch


################################################################

# function to optimize the solution (assign the best topics for groups that didn't get desired projects)
def optimize():
    global opti_count
    opti_count = 0
    best_iteration.calculate_fitness(selection_1, selection_2, selection_3, topic)
    for i in range(0, best_iteration.gene_length):
        if best_iteration.optimized[i] == 1:
            continue
        if best_iteration.optimized[i] == 0:
            for j in range(0, best_iteration.gene_length):
                if best_iteration.optimized[j] == 1:
                    continue
                elif topic[int(selection_1[i]) - 1] == topic[j] or topic[int(selection_2[i]) - 1] == topic[j] or \
                        topic[int(selection_3[i]) - 1] == topic[j]:
                    if i == j:
                        best_iteration.optimized[i] = 1
                    else:
                        best_iteration.genes[i], best_iteration.genes[j] = best_iteration.genes[j], \
                                                                           best_iteration.genes[i]
                        best_iteration.optimized[i] = 1
                        opti_count += 1


################################################################
# function for generations
def generate(pop: Population):
    for generations in range(0, generation_count):
        fitness = []

        for i in range(0, pop.population_size):
            fitness.append(pop.chromosomes[i].calculate_fitness(selection_1, selection_2, selection_3, topic))

        pop.sort_population(fitness)
        best_fit = [pop.chromosomes[0], pop.chromosomes[1]]
        crossover(pop, best_fit)


################################################################
# Program run
def start():
    print("\n---------------------------------\nCalculating Iterations", end=" ")
    global best_fitness, best_iteration, kill

    best_iteration = Chromosome(0, len(selection_1), len(doctors))
    best_fitness = [0, 0, 0, 0]
    best_total = 0

    # Loop for each iteration
    for iterations in range(0, iterations_count):
        if kill:
            print("\nprogram stopped.")
            break
        print(".", end=" ")
        progress_label.update('%' + str(int(float(iterations / iterations_count) * 100)))
        pop = Population(int(population_length.get()), len(selection_1), len(doctors))
        t1 = threading.Thread(target=generate(pop))
        t1.start()

        fitness = []

        for i in range(0, pop.population_size):
            fitness.append(pop.chromosomes[i].calculate_fitness(selection_1, selection_2, selection_3, topic))

        pop.sort_population(fitness)
        current_iteration = pop.chromosomes[0]
        current_fitness = current_iteration.calculate_fitness(selection_1, selection_2, selection_3, topic)
        iterations_text.print(current_iteration.genes, current_fitness)
        current_total = (current_fitness[1] * 1000) + (current_fitness[2] * 50) + (current_fitness[3])
        if (current_fitness[0] > best_fitness[0]) or (
                current_fitness[0] == best_fitness[0] and current_total > best_total):
            best_fitness = current_fitness
            best_iteration = current_iteration
            best_total = current_total
            solution.update([best_iteration.genes, best_fitness])

    if not kill:
        print("\nAll iteration calculated.")
        progress_label.update('%100')

    # saving the original solution to logs file
    if radio_1.get():
        write_log(str(best_iteration.genes) + str(best_fitness))


# function for representing the best solution so far with an organized table
def open_window():
    header_list = ['Student Groups', 'Project Title', 'Supervisor']
    data = []
    for groups in range(0, best_iteration.gene_length):
        data.append([Stud_names[groups], proj_title[best_iteration.genes[groups] - 1],
                     doctors[best_iteration.genes[groups] - 1]])

    layout1 = [[sg.Table(values=data,
                         headings=header_list,
                         display_row_numbers=True,
                         auto_size_columns=False,
                         num_rows=min(25, len(data)),
                         col_widths=[20, 80, 25],
                         justification='left')],
               [sg.Button('OK', pad=(500, 0), size=(10, 1))]]

    window1 = sg.Window("Result Table", layout1, modal=True, grab_anywhere=True)

    while True:
        event1, values1 = window1.read()
        if event1 == "OK" or event1 == sg.WIN_CLOSED:
            window1.close()
            break


# Building The GUI
sg.theme('DarkGray2')

# Components
browse_groups_label = sg.Text()
browse_projects_label = sg.Text()
population_length = sg.Input(size=(6, 1))
iteration_num = sg.Input(size=(6, 1))
generation_num = sg.Input(size=(6, 1))
radio_1 = sg.Radio("Save Regular output.", "RADIO1", default=True)
radio_2 = sg.Radio("Save Optimized output.", "RADIO1", default=False)
Start_button = sg.Button('Start', size=(10, 1), pad=((380, 0), 0))
Stop_button = sg.Button('Stop', size=(10, 1), pad=((50, 0), 0), visible=False)
iterations_text = sg.Multiline(disabled=True, size=(400, 20))
solution = sg.Input(disabled=True, size=(600, 1))
show_result = sg.Button('Show Result', visible=False, size=(15, 1), pad=((350, 0), (10, 0), 0, 0))
optimize_button = sg.Button('Optimize Solution', visible=False, size=(15, 1), pad=((350, 0), (10, 0), 0, 0))
progress_label = sg.Text()
optimize_label = sg.Text(justification='center', pad=((280, 0), (10, 0), 0, 0))

# Gui build layout
layout = [[browse_groups, browse_groups_label],
          [browse_projects, browse_projects_label],
          [sg.Text('Number of Chromosomes in Population: '), population_length, sg.Text('Number of iterations: '),
           iteration_num, sg.Text('Number of Generations: '), generation_num],
          [sg.Text("Iterations:")],
          [iterations_text],
          [sg.Text("Best Solution:")],
          [solution],
          [radio_1, radio_2, sg.Text('Progress: ', pad=((400, 0), 0)), progress_label],
          [Start_button, Stop_button],
          [show_result],
          [optimize_button],
          [optimize_label]]

window = sg.Window('Graduation Projects Distribution', layout, size=(870, 680))
print("Program is Ready.")
while True:
    event, values = window.read()
    if event == 'Start':
        # if any of the brackets is empty
        if population_length.get() == '' or iteration_num.get() == '' or generation_num.get() == '':
            sg.Popup('One or more of the Fields is Empty!', title='Error', keep_on_top=True)
        # if values entered are not numeric (or not positive)
        elif not population_length.get().isnumeric() or not iteration_num.get().isnumeric() or not generation_num.get().isnumeric():
            sg.Popup('Invalid inputs!\nPlease enter Positive integers.', title='Error', keep_on_top=True)
        # if population is less than 1
        elif population_length.get() == '1' or population_length.get() == '0':
            sg.Popup('Chromosomes in population must be more than 1.', title='Error', keep_on_top=True)
        # if iterations or generations num is 0
        elif iteration_num.get() == '0':
            sg.Popup('number of iterations must be over 0.', title='Error', keep_on_top=True)
        elif generation_num.get() == '0':
            sg.Popup('number of generations must be over 0.', title='Error', keep_on_top=True)
        # if files aren't assigned
        elif not browse_groups.get_size() or browse_projects.get_size() is None:
            sg.Popup('Files are not Assigned!', title='Error', keep_on_top=True)
        else:
            kill = False
            # reading files and storing every row variables
            # Groups file
            Stud_names = []
            selection_1 = []
            selection_2 = []
            selection_3 = []

            doctors = []
            proj_title = []
            topic = []

            #######################
            # Groups file
            groups_file = open(values['Browse Groups File'])
            csv_reader = csv.reader(groups_file)

            for row in csv_reader:
                Stud_names.append(row[0])
                selection_1.append(row[1])
                selection_2.append(row[2])
                selection_3.append(row[3])

            #######################
            # Project file
            projects_file = open(values['Browse Projects File'])
            csv_reader2 = csv.reader(projects_file)

            for row in csv_reader2:
                doctors.append(row[0])
                proj_title.append(row[1])
                topic.append(row[2])

            #######################
            iterations_count = int(iteration_num.get())
            generation_count = int(generation_num.get())
            iterations_text.update('')
            solution.update('')
            optimize_label.update('')

            # Creating a Thread
            t2 = threading.Thread(target=start)
            t2.start()
            show_result.update(visible=True)
            optimize_button.update(visible=True)
            Stop_button.update(visible=True)

    if event == 'Show Result':
        open_window()

    if event == 'Optimize Solution':
        optimize()
        best_fitness = best_iteration.calculate_fitness(selection_1, selection_2, selection_3, topic)
        solution.update([best_iteration.genes, best_fitness])
        optimize_label.update(str(opti_count) + ' Groups in the Solution has been optimized!')
        # saves optimized solution to logs file
        if radio_2.get():
            write_log(str(best_iteration.genes) + str(best_fitness))
        print("Solution is optimized.")
    if event == 'Stop':
        kill = True

    if event == sg.WIN_CLOSED:
        print("\nProgram ended.")
        break

window.close()

###############################################
