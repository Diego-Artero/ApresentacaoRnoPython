# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Carregando o arquivo
corpus = pd.read_excel('ArquivoRespostas.xlsx', header=None)

# Remover vazios/espaços e substituir por NA
corpus.replace("", np.nan, inplace=True)

# Transformando o corpus em uma lista de listas
corpus = corpus.values.tolist()

# Ordenando usuários
usuarios = sorted(set([item for sublist in corpus for item in sublist if pd.notna(item)]))
usuario_indice = {usuario: i for i, usuario in enumerate(usuarios)}

# Matriz de incidência
mtx_inc = np.zeros((len(usuarios), len(corpus)), dtype=int)
for col, sublist in enumerate(corpus):
    for usuario in sublist:
        if pd.notna(usuario):
            mtx_inc[usuario_indice[usuario], col] = 1

# Matriz de similaridade
mtx_sim = np.dot(mtx_inc, mtx_inc.T)
np.fill_diagonal(mtx_sim, 0)

# Matriz de co-ocorrência
mtx_co = np.zeros((len(usuarios), len(usuarios)), dtype=int)
for sublist in corpus:
    sublist_usuarios = [usuario_indice[usuario] for usuario in sublist if pd.notna(usuario)]
    for i in range(len(sublist_usuarios)):
        for j in range(i + 1, len(sublist_usuarios)):
            mtx_co[sublist_usuarios[i], sublist_usuarios[j]] += 1
            mtx_co[sublist_usuarios[j], sublist_usuarios[i]] += 1
np.fill_diagonal(mtx_co, 0)

# Criando grafos usando NetworkX
# Construindo o grafo de incidência
G_incidencia = nx.Graph()

# Adicionando nós para usuários
for usuario in usuarios:
    G_incidencia.add_node(usuario, bipartite=0)

# Adicionando nós para eventos
events = list(range(len(corpus)))
for event in events:
    G_incidencia.add_node(f'Event_{event}', bipartite=1)

# Adicionando arestas entre usuários e eventos
for col, sublist in enumerate(corpus):
    for usuario in sublist:
        if pd.notna(usuario):
            G_incidencia.add_edge(usuario, f'Event_{col}')

# Desenhando o grafo de incidência
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G_incidencia)  # Layout do grafo
nx.draw(G_incidencia, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
plt.title('Grafo de Incidência')
plt.show()

# Construindo o grafo de similaridade
G_similaridade = nx.Graph()
for i in range(len(usuarios)):
    for j in range(i + 1, len(usuarios)):
        if mtx_sim[i, j] > 0:
            G_similaridade.add_edge(usuarios[i], usuarios[j], weight=mtx_sim[i, j])

# Desenhando o grafo de similaridade
plt.figure(figsize=(12, 8))
weights = [G_similaridade[u][v]['weight'] for u, v in G_similaridade.edges()]
nx.draw(G_similaridade, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', width=weights)
plt.title('Grafo de Similaridade')
plt.show()

# Construindo o grafo de coocorrência
G_coocorrencia = nx.Graph()
for i in range(len(usuarios)):
    for j in range(i + 1, len(usuarios)):
        if mtx_co[i, j] > 0:
            G_coocorrencia.add_edge(usuarios[i], usuarios[j], weight=mtx_co[i, j])

# Desenhando o grafo de coocorrência
plt.figure(figsize=(12, 8))
weights = [G_coocorrencia[u][v]['weight'] for u, v in G_coocorrencia.edges()]
nx.draw(G_coocorrencia, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', width=weights)
plt.title('Grafo de Coocorrência')
plt.show()

# Métricas topológicas
def graph_metrics(graph, graph_name):
    print(f"Métricas do grafo {graph_name}:")
    print("Número de vértices:", graph.number_of_nodes())
    print("Número de arestas:", graph.number_of_edges())
    degrees = dict(graph.degree())
    print("Graus de vértice:", degrees)
    mean_degree = np.mean(list(degrees.values()))
    print("Grau médio:", mean_degree)
    if nx.is_weighted(graph):
        weights = nx.get_edge_attributes(graph, 'weight')
        mean_weight = np.mean(list(weights.values()))
        print("Força de conectividade média:", mean_weight)
    density = nx.density(graph)
    print("Densidade da rede:", density)
graph_metrics(G_incidencia, "de incidência")
graph_metrics(G_similaridade, "de similaridade")
graph_metrics(G_coocorrencia, "de co-ocorrência")

