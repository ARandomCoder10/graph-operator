from copy import deepcopy

#Data from the June 2022 Question 3
graph = {
    'A': {'B': 4.0, 'C': 12.0, 'D': 10.0},
    'B': {'A': 4.0, 'C': 7.0, 'E': 13.0, 'F': 15.0},
    'C': {'A': 12.0, 'B': 7.0, 'F': 3.0},
    'D': {'A': 10.0, 'F': 8.0, 'G': 11.0},
    'E': {'B': 13.0, 'F': 4.0, 'H': 5.0},
    'F': {'B': 15.0, 'C': 3.0, 'D': 8.0, 'E': 4.0, 'G': 6.0, 'H': 10.0},
    'G': {'D': 11.0, 'F': 6.0, 'H': 12.0},
    'H': {'E': 5.0, 'F': 10.0, 'G': 12.0}
}
directed = False
principal = 'A'

#My own graph - multiple shortest pathways
graph = {
    'A': {'B': 2.0, 'C': 4.0},
    'B': {'A': 2.0, 'C': 2.0},
    'C': {'A': 4.0, 'B': 2.0, 'D': 7.0, 'E': 3.0, 'F': 16.0},
    'D': {'C': 7.0, 'F': 9.0},
    'E': {'C': 3.0, 'F': 13.0},
    'F': {'C': 16.0, 'D': 9.0, 'E': 13.0}
}
directed = False
principal = 'A'

#Data from the June 2024 Question 3
graph = {
    'A': {'B': 25.0, 'C': 18.0, 'D': 47.0},
    'B': {'A': 25.0, 'C': 5.0, 'D': 17.0},
    'C': {'A': 18.0, 'B': 5.0, 'D': 24.0},
    'D': {'A': 47.0, 'B': 17.0, 'C': 24.0, 'E': 20.0, 'F': 34.0, 'G': 26.0},
    'E': {'D': 20.0, 'F': 12.0, 'J': 41.0, 'K': 37.0},
    'F': {'D': 34.0, 'E': 12.0, 'G': 4.0, 'H': 15.0, 'J': 27.0, 'K': 25.0},
    'G': {'D': 26.0, 'F': 4.0, 'H': 21.0},
    'H': {'F': 15.0, 'G': 21.0, 'J': 9.0, 'K': 6.0},
    'J': {'E': 41.0, 'F': 27.0, 'H': 9.0},
    'K': {'E': 37.0, 'F': 25.0, 'H': 6.0}
}
directed = False
principal = 'A'

#January 2014 Q5
graph = {
    'S': {'A': 24.0, 'B': 38.0, 'C': 75.0, 'D': 82.0},
    'A': {'S': 24.0, 'C': 43.0, 'E': 22.0},
    'B': {'S': 38.0, 'D': 39.0},
    'C': {'S': 75.0, 'A': 43.0, 'D': 10.0, 'T': 48.0},
    'D': {'S': 82.0, 'B': 39.0, 'C': 10.0, 'T': 32.0},
    'E': {'A': 22.0, 'T': 73.0},
    'T': {'C': 48.0, 'D': 32.0, 'E': 73.0},
}
directed = False
principal = 'S'

#Creating the dictionary of results
results = {}

visiting_vertex = principal #For me to better follow within code
graph_dijk = deepcopy(graph) #Dijk-stra

working_values = [[], []]
work_vertices = working_values[0]
work_values = working_values[1]

INFINITY = float('inf') #A universal constant

#Constructing the working_values record & the results dictionary
for vertex in graph_dijk:
    #Skipping the principal vertex because it is the start
    if vertex != principal:
        work_vertices.append(vertex)
        work_values.append(INFINITY)
        results[vertex] = [[], INFINITY] #Placeholders
    else:
        #Setting the principal to be a base for all results
        results[vertex] = [[principal], 0.0]
pass

#To find all shortest pathways

path_branches = [[results, working_values, graph_dijk, principal]]
incomplete = True

#Finding every path_branch
while incomplete:

    #For each path_branch, the algorithm
    while working_values != [[], []]:
        arcs = graph_dijk[visiting_vertex]

        new_branches = [] #A temporary space to store the branches to be finalised

        #Retrieving the adjacent arcs
        for arc_vertex, arc_weight in arcs.items():

            #Removing the arc's repeated instance in the adjacency list
            if not directed or (directed and visiting_vertex in graph_dijk[arc_vertex]):
                # if the graph is fully undirected or if there is a directed arc and the current arc is undirected
                graph_dijk[arc_vertex].pop(visiting_vertex)

            #Create a new branch for an identical total_weight
            if results[visiting_vertex][1] + arc_weight == results[arc_vertex][1]:
                new_branches.append([deepcopy(results), [], deepcopy(graph_dijk), ''])
                #The [1] and [3] are placeholders for the working_values & visiting_vertex

            #If the path up to the visiting_vertex + the adjacent arc is less than (or equal to)
            #the one set for the arc_vertex
            if results[visiting_vertex][1] + arc_weight <= results[arc_vertex][1]:

                #Copy the pathway up to the visiting vertex...
                results[arc_vertex] = deepcopy(results[visiting_vertex])
                #...add the arc_vertex to the pathway...
                results[arc_vertex][0].append(arc_vertex)
                #...and update the total weight with the arc_weight
                results[arc_vertex][1] += arc_weight

                #Add it to the working values
                work_values[work_vertices.index(arc_vertex)] = results[arc_vertex][1]

        #Finding the minimum
        min_value = min(work_values)
        min_vertex = work_vertices[work_values.index(min_value)]
        work_vertices.remove(min_vertex)
        work_values.remove(min_value)

        #Removing the adjacent arcs
        visiting_vertex = min_vertex #The next visiting_vertex

        #If completed but not exited
        # The next vertex to visit when starting each branch
        for branch in new_branches:
            branch[1], branch[3] = deepcopy(working_values), visiting_vertex
            path_branches.append(branch)

    #Determining full completion
    for branch in path_branches:
        if branch[1] != [[], []]:
            results, working_values, graph_dijk, visiting_vertex = branch[0], branch[1], branch[2], branch[3]
            work_vertices, work_values = working_values[0], working_values[1]
            break
        elif branch == path_branches[-1]:
            incomplete = False

#Removing the algorithm data
path_branches_temp = []
for branch in path_branches:
    branch[0].pop(principal)
    path_branches_temp.append(branch[0])
path_branches = deepcopy(path_branches_temp)

#Redefining the final results
results = deepcopy(path_branches[0])
for pathway in results.values():
    #Make then 2D to append multiple pathways
    pathway[0] = [pathway[0]]

#In each branch
for branch in path_branches[1:]:
    #In each vertex pathway
    for leaf in branch:
        #If the total_weight in the algorithm is less, replace it
        if branch[leaf][1] < results[leaf][1]:
            results[leaf] = deepcopy(branch[leaf])
        #If the total_weight is the same as another, add the pathway
        elif branch[leaf][1] == results[leaf][1] and branch[leaf][0] not in results[leaf][0]:
            results[leaf][0].append(branch[leaf][0])

print('It worked?')
pass