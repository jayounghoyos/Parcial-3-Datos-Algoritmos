import pandas as pd
import networkx as nx
from collections import defaultdict
import plotly.graph_objects as go

def load_data(file_path, num_rows):
    df = pd.read_csv(file_path, nrows=num_rows)
    return df[['Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']]

def build_graph(data):
    G = nx.Graph()
    movies = defaultdict(set)
    
    for row in data.itertuples(index=False):
        title = row.Series_Title
        director = row.Director
        stars = {row.Star1, row.Star2, row.Star3, row.Star4} - {None}
        
        for star in stars:
            G.add_edge(director, star, title=title)
            movies[title].add(star)
        movies[title].add(director)

    return G, movies

def visualize_graph_3d(graph):
    pos = nx.spring_layout(graph, dim=3, seed=42)
    edge_x, edge_y, edge_z, hover_text = [], [], [], []
    for edge in graph.edges(data=True):
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
        # Añadiendo el título de la película como información en hover
        hover_text.extend([edge[2]['title'], edge[2]['title'], None])

    edge_trace = go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, line=dict(width=2, color='grey'), hoverinfo='text', hovertext=hover_text, mode='lines')

    node_x, node_y, node_z, text = [], [], [], []
    for node, (x, y, z) in pos.items():
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        text.append(node)

    node_trace = go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=text, marker=dict(showscale=True, colorscale='Viridis', size=10, colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right'), line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(title='<br>Network graph made with Python', titlefont_size=16, showlegend=False, hovermode='closest', margin=dict(b=20,l=5,r=5,t=40), annotations=[dict(text="Plotly 3D visualization", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002)], xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    fig.show()

# Main execution
#numero de filas usadas
num_rows = 20
file_path = 'formated.csv'
data = load_data(file_path, num_rows)
graph, movies = build_graph(data)
visualize_graph_3d(graph)  # Visualize the graph in 3D
