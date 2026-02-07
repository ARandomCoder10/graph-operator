from copy import deepcopy

# Data from the June 2022 Question 3
graph = {
    'A': {'B': 12.0, 'C': 24.0, 'D': 20.0, 'E': 23.0, 'F': 11.0},
    'B': {'A': 12.0, 'C': 12.0, 'D': 8.0, 'E': 24.0, 'F': 21.0},
    'C': {'A': 28.0, 'B': 2.0, 'D': 4.0, 'E': 12.0, 'F': 2.0},
    'D': {'A': 24.0, 'B': 21.0, 'C': 4.0, 'E': 16.0, 'F': 13.0},
    'E': {'A': 23.0, 'B': 29.0, 'C': 12.0, 'D': 16.0, 'F': 12.0},
    'F': {'A': 11.0, 'B': 23.0, 'C': 17.0, 'D': 13.0, 'E': 12.0},
}
directed = True

# Data from the June 2024 Question 2
graph = {
    'A': {'B': 50.0, 'C': 59.0, 'D': 26.0, 'E': 50.0, 'F': 40.0, 'G': 87.0, 'H': 63.0, 'J': 59.0},
    'B': {'A': 50.0, 'C': 28.0, 'D': 61.0, 'E': 79.0, 'F': 63.0, 'G': 45.0, 'H': 64.0, 'J': 48.0},
    'C': {'A': 59.0, 'B': 28.0, 'D': 33.0, 'E': 57.0, 'F': 35.0, 'G': 70.0, 'H': 36.0, 'J': 45.0},
    'D': {'A': 26.0, 'B': 61.0, 'C': 33.0, 'E': 24.0, 'F': 64.0, 'G': 71.0, 'H': 37.0, 'J': 33.0},
    'E': {'A': 50.0, 'B': 79.0, 'C': 57.0, 'D': 24.0, 'F': 40.0, 'G': 64.0, 'H': 30.0, 'J': 31.0},
    'F': {'A': 40.0, 'B': 63.0, 'C': 35.0, 'D': 64.0, 'E': 40.0, 'G': 47.0, 'H': 70.0, 'J': 71.0},
    'G': {'A': 87.0, 'B': 45.0, 'C': 70.0, 'D': 71.0, 'E': 64.0, 'F': 47.0, 'H': 34.0, 'J': 67.0},
    'H': {'A': 63.0, 'B': 64.0, 'C': 36.0, 'D': 37.0, 'E': 30.0, 'F': 70.0, 'G': 34.0, 'J': 33.0},
    'J': {'A': 59.0, 'B': 48.0, 'C': 45.0, 'D': 33.0, 'E': 31.0, 'F': 71.0, 'G': 67.0, 'H': 33.0}
}
directed = False

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
#    graph[key] = {}
#    for vertex in letters[:n]:
#        if vertex != key:
#            graph[key][vertex] = 1.0
#directed = False

#The fourth test data - checking an incomplete graph
#graph = {
#    'A': {'B': 1.0, 'D': 1.0},
#    'B': {'A': 1.0, 'C': 1.0},
#    'C': {'A': 1.0, 'B': 1.0},
#    'D': {'A': 1.0, 'B': 1.0},
#}
#directed = True

#-----------------------------------------------------
#Measuring the runtime manually (for testing purposes)
from time import perf_counter
start = perf_counter()
#-----------------------------------------------------

final_tours = []
graphs = [deepcopy(graph)]

principal_specified = False
principal = ''

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

#Starting at each vertex
for start_vertex in graph:

    #If they chose to explore all possibilities...
    if not principal_specified:
        principal = start_vertex
    #If they chose to specify the start & return, continue until found
    elif start_vertex != principal:
        continue

    pass

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
                    if arc_weight == minimum:

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
                            [pathway + [arc_vertex], total_weight + minimum,
                             graph_neigh_temp, state])
                        #Adding the graph's index is for a marker for if this was from the transposed graph

                final_tours.remove([pathway, total_weight, graph_neigh, state])

            else:
                # If there are no adjacent arcs left...
                incompatible = True

            # To determine if there are anymore incomplete tours
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

            # If there is an incompatible tour...
            try:
                if incompatible_tour in final_tours:
                    final_tours.remove(incompatible_tour)
            except NameError:
                pass

        for tour in final_tours:
            #Removing the graph_neigh from each tour
            if len(tour) == 4:
                pathway = tour[0]
                final_stop = pathway[-1]

                #The final check for incompatibility - can it return?
                if principal in graph[final_stop]:
                    pathway.append(principal)
                    tour[1] += graph[final_stop][principal]
                    tour.remove(tour[2])

                    # Reversing the pathway for each transposed tour
                    if tour[-1] == 1:
                        tour[0] = tour[0][::-1]
                else:
                    incompatible_tour = deepcopy(tour)

        try:
            if incompatible_tour in final_tours:
                final_tours.remove(incompatible_tour)
        except NameError:
            pass

    #Only one run for one vertex
    if principal_specified:
        break

#Removing the no-longer-needed state
for tour in final_tours:
   tour.pop()

# Checking for & removing repeated tours that are backwards
if directed:
    for tour in final_tours:
        #If there is an identical
        if final_tours.count(tour) == 2:
            #Remove the identicals to eventually retain one of it
            final_tours.remove(tour)
        else:
            tour.append(False)
        #This will label all the false ones...

    #...so this one can catch the True ones, which are currently unmarked
    for tour in final_tours:
        if len(tour) == 2:
            tour.append(True)

#-----------------------------------------------------
end = perf_counter()
print(f'RUNTIME: {end - start}s')
#-----------------------------------------------------

#If no tours, unsolvable
#If 1 tour, already sorted and abstracted
if len(final_tours) >= 2:

    # Removing the extra unnecessary tour branches

    #A temporary dictionary to store the weights of each tour
    tour_weights = {}

    vertices = [principal] if principal_specified else graph.keys()
    for vertex in vertices:

        tour_weights[vertex] = []

    for tour in final_tours:
        tour_weights[tour[0][0]].append(tour[1])

    #final_tours without the extra tours
    final_tours_abstracted = []

    for vertex, collection in tour_weights.items():
        try:
            minimum = min(collection)
        except ValueError:
            #In the event that no tour was possible from such vertex
            continue

        for tour in final_tours:
            if tour[0][0] == vertex and tour[1] == minimum:
                final_tours_abstracted.append(deepcopy(tour))

    final_tours = deepcopy(final_tours_abstracted)

    #Sorting the tours

    #Gathering the total_weights
    total_weights = []
    for tour in final_tours:
        total_weights.append(tour[1])

    #Then finding the tour associated with the minimum
    final_tours_ordered = []

    while total_weights != []:
        #Searching...
        minimum_total = min(total_weights)
        for tour in final_tours:
            if tour[1] == minimum_total and tour not in final_tours_ordered:
                final_tours_ordered.append(deepcopy(tour))
                #Set it up for the next minimum
                total_weights.remove(minimum_total)
                break

    final_tours = deepcopy(final_tours_ordered)

#Algorithm fully works!
pass