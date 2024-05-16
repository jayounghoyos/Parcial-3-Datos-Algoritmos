import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, value):
        if not self.head:
            self.head = Node(value)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(value)
    
    def prepend(self, value):
        new_head = Node(value)
        new_head.next = self.head
        self.head = new_head 
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

def build_graph(data):
    G = nx.Graph()
    movies = defaultdict(LinkedList)  # Usamos la lista enlazada personalizada

    for _, row in data.iterrows():
        title = row['Series_Title']
        director = row['Director']
        stars = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]

        for star in stars:
            G.add_edge(director, star, title=title)
            movies[title].append(star)
        movies[title].prepend(director)  # Añadir el director al principio de la lista

    return G, movies

def bfs_shortest_path(graph, start, goal):
    explored = set()
    queue = LinkedList()
    queue.append([start])

    while queue.head:
        path = queue.head.value
        queue.head = queue.head.next
        node = path[-1]

        if node == goal:
            return path

        if node not in explored:
            explored.add(node)
            for neighbour in graph[node]:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return None

def dfs_paths(graph, start, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = [start]

    visited.add(start)
    paths = [path[:]]
    for neighbor in graph[start]:
        if neighbor not in visited:
            path.append(neighbor)
            paths.extend(dfs_paths(graph, neighbor, path, visited))
            path.pop()
    return paths

def visualize_graph(graph):
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=700, font_size=8)
    
    # Añadir etiquetas a las aristas con los nombres de las películas
    edge_labels = {(u, v): d['title'] for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    
    #plt.title("Collaboration Graph") #Se puede comentar para no tener que ver el titulo y cargue mas rapido
    plt.show()

if __name__ == '__main__':
    # Main execution
    file_path = 'formated.csv'
    data = load_data(file_path)
    graph, movies = build_graph(data)

    # Visualizing the graph
    visualize_graph(graph)

    # Example of using BFS and DFS
    start_actor = 'Morgan Freeman'  
    end_actor = 'Al Pacino'
    print("BFS shortest path:", bfs_shortest_path(graph, start_actor, end_actor))
    print("DFS paths:", dfs_paths(graph, start_actor))