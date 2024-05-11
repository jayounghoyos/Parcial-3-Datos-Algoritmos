import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

def build_graph(data):
    G = nx.Graph()
    movies = defaultdict(deque)
    
    for _, row in data.iterrows():
        title = row['Series_Title']
        director = row['Director']
        stars = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]
        
        # Añadir el director y los actores al grafo
        for star in stars:
            G.add_edge(director, star, title=title)
            movies[title].append(star)
        movies[title].appendleft(director)  # Agregar el director al principio

    return G, movies

def visualize_graph(graph):
    pos = nx.circular_layout(graph)  # Usar una disposición circular simple
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=700, font_size=8)
    plt.title("Collaboration Graph")
    plt.show()

# Main execution
file_path = 'formated.csv'  # Asegúrate de que el nombre y ruta del archivo sean correctos
data = load_data(file_path)
graph, movies = build_graph(data)

visualize_graph(graph)  # Llamada para visualizar el grafo
