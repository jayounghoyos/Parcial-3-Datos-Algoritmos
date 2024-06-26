import threading
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

def build_graph(data):
    G = nx.Graph()
    movies = defaultdict(deque)  # Listas enlazadas para almacenar los actores y directores por película

    for _, row in data.iterrows():
        title = row['Series_Title']
        director = row['Director']
        stars = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]

        for star in stars:
            G.add_edge(director, star, title=title)
            movies[title].append(star)
        movies[title].appendleft(director)  # Añadir el director al frente de la lista enlazada

    return G, movies

def visualize_graph(graph):
    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='k', node_size=700, font_size=8)

    # Añadir etiquetas a las aristas con los nombres de las películas
    edge_labels = {(u, v): d['title'] for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Collaboration Graph")
    plt.show()

def listen_for_exit():
    input_text = input("Press 'q' to exit the program: ")
    if input_text.lower() == 'q':
        print("Exiting the program...")
        exit()

# Main execution
file_path = 'formated.csv'
data = load_data(file_path)
graph, movies = build_graph(data)

# Visualizing the graph
visualize_graph(graph)

# Start listening for exit command in a separate thread
exit_thread = threading.Thread(target=listen_for_exit)
exit_thread.start()
