# PSEUDOCODE:

# TODO: Consider dividing each edge into a bunch of sub graphs
# 	to accommodate for multiple people being on 1 road


from collections import defaultdict
import csv
from heap import Heap
import numpy as np
from Graph import Graph
from Person import Person
import time
from plot_graph import plot_graph

def main():
    graph = Graph('graph.txt')

    people = 3

    with open('start_end.txt') as f:
        everyone = [Person(row[0], row[1], row[2]) for row in csv.reader(f)]

    people = everyone.copy()
    time_taken = 0
    reached = []
    tot=0

    while tot<len(people):

        graph.time_taken = defaultdict(lambda: 0)

        for idx in range(len(people)):
            person = people[idx]
            if not person.reached():

                route = dijkstra(graph, person.current_pos, person.end)
                next_pos = route[1][0]

                graph.update_positions(person.current_pos, next_pos, remove=True)
                person.path.append(next_pos)

                if not person.current_pos == person.start:
                    graph.update_cost(person.prev_pos, person.current_pos, value=-1) # reduces cost of the edge the person is no longer on

                graph.update_cost(person.current_pos, next_pos, value=1) # increases cost of the edge on which person travels
                person.prev_pos = person.current_pos

                person.move(next_pos)

                graph.time_taken[(person.prev_pos, person.current_pos)] += 1

                print(person.path[-2:])

            elif person.already_reached:
                pass
            else:
                print(f"PERSON {person.name} REACHED, PATH:", person.path)
                reached.append(person)
                person.already_reached = True
                tot+=1

        try:
            print(graph.time_taken.values())
            time = max(graph.time_taken.values())
            print(f"Time Taken: {time}\n----------")
            time_taken += time
        except:
            pass

            # take max people at an edge and use that for time taken

        # plot_graph(graph)
        # time_taken += max(graph.time_taken.values())

    print(time_taken)
    print([person.path for person in everyone])


class SpecialMinHeap(Heap):
    def greater(self, a, b):
        return a if self.m_heap[a]['distance'] < self.m_heap[b]['distance'] else b


def dijkstra(graph, start, end):
    '''
    This function returns a tuple of least distance and the best path to be taken from start + 1 to end
    TODO: figure out optimum way to recalculate
            dijkstra by only recalculating wrt
            the edge whose cost has changed
    '''

    nodes = {node: {'distance': (0 if node == start else np.inf), 'path_via': None, 'done': False, 'name': node} for node in graph.nodes}

    pq = SpecialMinHeap()
    pq.push(nodes[start])

    while not pq.empty():
        current_master_node = pq.pop()

        if current_master_node['name'] == end:
            route = [end]
            path_via = end

            while path_via != start:
                route.append(nodes[path_via]['path_via'])
                path_via = route[-1]

            return (nodes[end]['distance'], route[-2::-1])

        if current_master_node['done']:
            continue

        for adj_node, distance in graph.edges[current_master_node['name']].items():
            if not nodes[adj_node]['done']:
                distance += current_master_node['distance']

                if nodes[adj_node]['distance'] > distance:
                    nodes[adj_node]['distance'] = distance
                    nodes[adj_node]['path_via'] = current_master_node['name']
                    pq.push(nodes[adj_node])

        current_master_node['done'] = True

    raise RuntimeError('End point not found')


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)

'''
{
'1': {'2': 1, '5': 1, '6': 1}, 
'2': {'1': 1, '3': 1, '4': 1, '7': 1}, 
'3': {'2': 1, '4': 1, '6': 1}, 
'4': {'3': 1, '5': 1, '2': 1, '7': 1}, 
'5': {'4': 1, '1': 1, '6': 1}, 
'6': {'1': 1, '3': 1, '5': 1}, 
'7': {'2': 1, '4': 1}
}
'''

'''
{'1': {'2': 3, '5': 1, '6': 3},
'2': {'1': 3, '3': 1, '4': 1, '7': 1}, 
'3': {'2': 1, '4': 1, '6': 1}, 
'4': {'3': 1, '5': 1, '2': 1, '7': 1}, 
'5': {'4': 1, '1': 1, '6': 1}, 
'6': {'1': 3, '3': 1, '5': 1}, 
'7': {'2': 1, '4': 1}}
'''