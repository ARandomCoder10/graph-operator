# Data from the June 2022 Question 3
#graph = {
#    'A': {'B': 12.0, 'C': 24.0, 'D': 20.0, 'E': 23.0, 'F': 11.0},
#    'B': {'A': 12.0, 'C': 12.0, 'D': 8.0, 'E': 24.0, 'F': 21.0},
#    'C': {'A': 28.0, 'B': 2.0, 'D': 4.0, 'E': 12.0, 'F': 2.0},
#    'D': {'A': 24.0, 'B': 21.0, 'C': 4.0, 'E': 16.0, 'F': 13.0},
#    'E': {'A': 23.0, 'B': 29.0, 'C': 12.0, 'D': 16.0, 'F': 12.0},
#    'F': {'A': 11.0, 'B': 23.0, 'C': 17.0, 'D': 13.0, 'E': 12.0},
#}
#directed = True

# Data from the June 2024 Question 2
#graph = {
#    'A': {'B': 50.0, 'C': 59.0, 'D': 26.0, 'E': 50.0, 'F': 40.0, 'G': 87.0, 'H': 63.0, 'J': 59.0},
#    'B': {'A': 50.0, 'C': 28.0, 'D': 61.0, 'E': 79.0, 'F': 63.0, 'G': 45.0, 'H': 64.0, 'J': 48.0},
#    'C': {'A': 59.0, 'B': 28.0, 'D': 33.0, 'E': 57.0, 'F': 35.0, 'G': 70.0, 'H': 36.0, 'J': 45.0},
#    'D': {'A': 26.0, 'B': 61.0, 'C': 33.0, 'E': 24.0, 'F': 64.0, 'G': 71.0, 'H': 37.0, 'J': 33.0},
#    'E': {'A': 50.0, 'B': 79.0, 'C': 57.0, 'D': 24.0, 'F': 40.0, 'G': 64.0, 'H': 30.0, 'J': 31.0},
#    'F': {'A': 40.0, 'B': 63.0, 'C': 35.0, 'D': 64.0, 'E': 40.0, 'G': 47.0, 'H': 70.0, 'J': 71.0},
#    'G': {'A': 87.0, 'B': 45.0, 'C': 70.0, 'D': 71.0, 'E': 64.0, 'F': 47.0, 'H': 34.0, 'J': 67.0},
#    'H': {'A': 63.0, 'B': 64.0, 'C': 36.0, 'D': 37.0, 'E': 30.0, 'F': 70.0, 'G': 34.0, 'J': 33.0},
#    'J': {'A': 59.0, 'B': 48.0, 'C': 45.0, 'D': 33.0, 'E': 31.0, 'F': 71.0, 'G': 67.0, 'H': 33.0}
#}
#directed = False

#the second test data - fully undirected
#graph = {
#    'S': {'V': 75.0, 'W': 30.0, 'X': 55.0, 'Y': 70.0, 'Z': 70.0},
#    'V': {'S': 75.0, 'W': 55.0, 'X': 30.0, 'Y': 40.0, 'Z': 15.0},
#    'W': {'S': 30.0, 'V': 55.0, 'X': 65.0, 'Y': 45.0, 'Z': 55.0},
#    'X': {'S': 55.0, 'V': 30.0, 'W': 65.0, 'Y': 15.0, 'Z': 10.0},
#    'Y': {'S': 70.0, 'V': 40.0, 'W': 45.0, 'X': 15.0, 'Z': 20.0},
#    'Z': {'S': 70.0, 'V': 15.0, 'W': 55.0, 'X': 10.0, 'Y': 20.0},
#}
#directed = False

#The third test data - extreme boundary producing n! tours
#graph = {
#    'A': {'B': 1.0, 'C': 1.0, 'D': 1.0, 'E': 1.0, 'F': 1.0},
#    'B': {'A': 1.0, 'C': 1.0, 'D': 1.0, 'E': 1.0, 'F': 1.0},
#    'C': {'A': 1.0, 'B': 1.0, 'D': 1.0, 'E': 1.0, 'F': 1.0},
#   'D': {'A': 1.0, 'B': 1.0, 'C': 1.0, 'E': 1.0, 'F': 1.0},
#    'E': {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0, 'F': 1.0},
#    'F': {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0, 'E': 1.0},
#}
#directed = False

#The third test data - extreme boundary producing (n-1)! tours
#letters = 'ABCDEGHIJKLMNOPQRSTUVWXYZ'
#graph = {}
#n = 5

#for key in letters[:n]:
    #graph[key] = {}
    #for vertex in letters[:n]:
        #if vertex != key:
            #graph[key][vertex] = 1.0
#directed = False

#The fourth test data - checking an incomplete graph
#graph = {
#    'A': {'B': 1.0, 'D': 1.0},
#    'B': {'A': 1.0, 'C': 1.0},
#    'C': {'A': 1.0, 'B': 1.0},
#    'D': {'A': 1.0, 'B': 1.0},
#}
#directed = True

#graph = {
#    'A': {'B': 1, 'C': 1},
#    'B': {'A': 1, 'C': 1, 'D': 1},
#    'C': {'A': 1, 'B': 1, 'D': 1},
#    'D': {},
#    'E': {'F': 1},
#    'F': {'E': 1}
#}
#directed = True

from copy import deepcopy
def solve(graph, directed, principal):
    # -----------------------------------------------------
    # Measuring the runtime manually (for testing purposes)
    from time import perf_counter
    start = perf_counter()
    # -----------------------------------------------------

    final_tours = []
    graphs = [deepcopy(graph)]
    
    # Getting the other graph representation
    if directed:
        graph_b = {}
    
        #Making a key for every vertex
        for graph_vertex in graph:
            graph_b[graph_vertex] = {}
    
        #Adding the arc weights
        for graph_vertex in graph:
            for arc_vertex, arc_weight in graph[graph_vertex].items():
                if graph_vertex in graph[arc_vertex]: #Checking against one-way directed arcs
                    graph_b[arc_vertex][graph_vertex] = arc_weight
    
        graphs.append(graph_b)
    
    #Operating on each transposition
    #the state to know which transposition
    for state, graph in enumerate(graphs):

        total_weight, incompatible = 0.0, False

        visiting_vertex = principal
        pathway = [principal]
        graph_principal = deepcopy(graph)
        incomplete = True

        for vertex in graph_principal:
            if principal in graph_principal[vertex]:
                graph_principal[vertex].pop(principal)

        graph_neigh = deepcopy(graph_principal)
        final_tours.append([[principal], 0.0, graph_neigh, state])

        while incomplete:
            adj_arcs = deepcopy(graph_neigh[visiting_vertex])

            if adj_arcs != {}:

                weights = list(adj_arcs.values())
                minimum = min(weights)

                # Iterating through to find the connected vertex to the minimum arc weight
                for arc_vertex, arc_weight in adj_arcs.items():
                    #if arc_weight == minimum:

                    #Retrieving the graph_neigh for the already
                    #determined part of the pathway
                    for tour in final_tours:
                        if tour[0] == pathway:
                            #Copying the graph at such stage
                            graph_neigh = deepcopy(tour[2])
                            break

                    #Correcting the graph_neigh to this pathway by
                    #removing each arc connected to the arc_vertex
                    graph_neigh_temp = deepcopy(graph_neigh)
                    for graph_vertex in graph_neigh_temp:
                        if arc_vertex in graph_neigh_temp[graph_vertex]:
                            graph_neigh_temp[graph_vertex].pop(arc_vertex)

                    #Updating the final tours
                    final_tours.append(
                        [pathway + [arc_vertex], (total_weight + arc_weight).__round__(4),
                         graph_neigh_temp, state])
                    #Adding the graph's index is for a marker for if this was from the transposed graph

                final_tours.remove([pathway, total_weight, graph_neigh, state])

            else:
                # If there are no adjacent arcs left...
                incompatible = True

            # To determine if there are anymore incomplete tours
            if final_tours != []:
                for tour in final_tours:
                    if len(tour[0]) < len(graph):
                        #To prevent re-accessing the same tour that was incompatible
                        if incompatible:
                            incompatible = False
                            incompatible_tour = deepcopy(tour)
                            continue
                        else:
                            # Resetting all the values of the variables for the next run
                            pathway, total_weight, graph_neigh = tour[0], tour[1], deepcopy(tour[2])
                            visiting_vertex = pathway[-1]
                            break
                    elif tour == final_tours[-1]:
                        incomplete = False
            else:
                incomplete = False

            # If there is an incompatible tour...
            try:
                if incompatible_tour in final_tours:
                    final_tours.remove(incompatible_tour)
            except NameError:
                pass

    final_tours_compatible = []
    for tour in final_tours:
        #Removing the graph_neigh from each tour
        if len(tour) == 4:
            pathway = tour[0]
            final_stop = pathway[-1]

            #The final check for incompatibility - can it return?
            if principal in graph[final_stop]:
                pathway.append(principal)
                tour[1] = (tour[1] + graph[final_stop][principal]).__round__(4)
                tour.remove(tour[2])

                # Reversing the pathway for each transposed tour
                if tour[-1] == 1:
                    tour[0] = tour[0][::-1]

                final_tours_compatible.append(tour)

    final_tours = deepcopy(final_tours_compatible)
    pass

    #try:
    #    if incompatible_tour in final_tours:
    #        final_tours.remove(incompatible_tour)
    #except NameError:
    #    pass

    #Only one run for one vertex
    #if principal_specified:
        #break

    if final_tours != []:
        #Removing the no-longer-needed state
        for tour in final_tours:
           tour.pop()


        #Isolating the shortest tours
        tour_weights = []
        final_tours_abstracted = []

        for tour in final_tours:
            if tour[1] not in tour_weights:
                tour_weights.append(tour[1])
        minimum_tour_weight = min(tour_weights)

        for tour in final_tours:
            if tour[1] == minimum_tour_weight:
                final_tours_abstracted.append(tour)
        final_tours = deepcopy(final_tours_abstracted)

        # Removing any identical tours (caused by tours with no directed arcs)
        if directed:
            for tour in final_tours:
                # If there is an identical
                if final_tours.count(tour) == 2:
                    # Iterate backwards to prevent dynamic index skipping
                    for i, backward_tour in enumerate(final_tours[::-1]):
                        if tour == backward_tour:
                            final_tours.pop(len(final_tours) - i - 1)
                            break
        else:
            # Reversing all undirected tours and adding them
            final_tours_full = deepcopy(final_tours)
            for tour in final_tours:
                # Can replicate an already-stored tour if the tour was found from identical arc weights
                if [tour[0][::-1], tour[1]] not in final_tours:
                    final_tours_full.append([tour[0][::-1], tour[1]])
            final_tours = deepcopy(final_tours_full)

        pass
        #Data storage optimisation
        final_tours_optimised = [[], minimum_tour_weight]
        for tour in final_tours:
            final_tours_optimised[0].append(tour[0])
        final_tours = deepcopy(final_tours_optimised)

    # -----------------------------------------------------
    # Measuring the runtime manually (for testing purposes)
    end = perf_counter()
    runtime = end - start
    #print(f'K{n}: {runtime}s')
    # -----------------------------------------------------

    return final_tours

#Algorithm fully works!
pass

#

#The third test data - extreme boundary producing (n-1)! tours




graph = {
    'A': {'B': 2, 'C': 14, 'D': 21, 'E': 22},
    'B': {'A': 2, 'C': 12, 'D': 19, 'F': 23},
    'C': {'A': 14, 'B': 12, 'D': 7, 'E': 8, 'F': 11},
    'D': {'A': 21, 'B': 19, 'C': 7, 'E': 1, 'F': 4},
    'E': {'A': 22, 'C': 8, 'D': 1, 'F': 3},
    'F': {'B': 23, 'C': 11, 'D': 4, 'E': 3}
}
directed = False

#graph = {
#    'A': {'B': 1, 'C': 1, 'D': 1, 'E': 1},
#    'B': {},
#    'C': {},
#    'D': {},
#    'E': {}
#}

#graph = {
#    'A': {'B': 12.0, 'C': 24.0, 'D': 20.0, 'E': 23.0, 'F': 11.0},
#    'B': {'A': 12.0, 'C': 12.0, 'D': 8.0, 'E': 24.0, 'F': 21.0},
#    'C': {'A': 28.0, 'B': 2.0, 'D': 4.0, 'E': 12.0, 'F': 2.0},
#    'D': {'A': 24.0, 'B': 21.0, 'C': 4.0, 'E': 16.0, 'F': 13.0},
#    'E': {'A': 23.0, 'B': 29.0, 'C': 12.0, 'D': 16.0, 'F': 12.0},
#    'F': {'A': 11.0, 'B': 23.0, 'C': 17.0, 'D': 13.0, 'E': 12.0},
#}
#directed = True

import random
letters = 'ABCDEGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"£$%^&*()-=[]:;@<>?+_.,{}~'
graph = {}
n = 2

for i in range(78):
    directed = False
    n += 1

    for key in letters[:n]:
        graph[key] = {}

    for key in letters[:n-1]:
        index = letters.index(key) + 1

        for vertex in letters[index:n]:
            #75% chance of there being an arc
            if random.random() <= 0.75:

                #85% chance it is undirected
                if random.random() <= 0.85:
                    a = random.randint(1, 1000)
                    graph[key][vertex] = a
                    graph[vertex][key] = a

                #15% chance it is directed
                else:
                    #40% chance it goes one direction
                    if random.random() <= 0.4:
                        graph[key][vertex] = random.randint(1, 1000)
                    elif 0.4 < random.random() <= 0.8:
                        graph[vertex][key] = random.randint(1, 1000)

                    #20% chance it goes both directions
                    else:
                        graph[key][vertex] = random.randint(1, 1000)
                        graph[vertex][key] = random.randint(1, 1000)

                    directed = True

    a = solve(graph, directed, 'A', n)

#10: 0.015617900062352419s
#15: 0.028577700024470687s
#20: 0.039780500112101436s
#25: 0.07210410002153367s
#30: 0.143935