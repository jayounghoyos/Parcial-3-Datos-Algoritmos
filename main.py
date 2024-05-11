import tkinter as tk
from tkinter import messagebox
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

def build_graph(data):
    G = nx.Graph()
    movies = defaultdict(deque)  # Usar deque para almacenar listas enlazadas de actores/directores
    
    for _, row in data.iterrows():
        title = row['Series_Title']
        director = row['Director']
        stars = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]
        
        for star in stars:
            G.add_edge(director, star, title=title)
            movies[title].append(star)
        movies[title].appendleft(director)

    return G, movies

def bfs_shortest_path(graph, start, goal):
    explored = set()
    queue = deque([[start]])
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == goal:
            return path
        
        elif node not in explored:
            explored.add(node)
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

    return None

def dfs_paths(graph, start, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)
    paths = [path.copy()]  # Crear una copia para evitar referencias cruzadas

    for neighbor in graph[start]:
        if neighbor not in visited:
            paths.extend(dfs_paths(graph, neighbor, visited.copy(), path.copy()))

    path.pop()  # Quitar el nodo actual al retroceder
    return paths

def salir():
    if messagebox.askokcancel("Salir", "¿Quieres salir del programa?"):
        root.destroy()

def visualize_graph(graph):
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=700, font_size=8)
    plt.title("Collaboration Graph")
    plt.show()

# Main execution
file_path = 'formated.csv'
data = load_data(file_path)
graph, movies = build_graph(data)

visualize_graph(graph)  # Visualize the graph

# Example usage of BFS and DFS
start_actor = 'Actor1'
end_actor = 'Actor2'
print("BFS shortest path:", bfs_shortest_path(graph, start_actor, end_actor))
print("DFS paths:", dfs_paths(graph, start_actor))

root = tk.Tk()
root.title("Salir del Programa")

exit_button = tk.Button(root, text="Salir", command=salir, height=2, width=10)
exit_button.pack(pady=20)

root.mainloop()