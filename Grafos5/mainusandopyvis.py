import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network

# Carregando o arquivo
corpus = pd.read_excel('ArquivoRespostas.xlsx', header=None)

# Remover vazios/espaços e substituir por NA
corpus.replace("", np.nan, inplace=True)

# Transformando o corpus em uma lista de listas
corpus = corpus.values.tolist()

# Obtendo a lista de todos os usuários
usuarios = sorted(set([item for sublist in corpus for item in sublist if pd.notna(item)]))
usuario_indice = {usuario: i for i, usuario in enumerate(usuarios)}

# Criando a matriz de incidência
mtx_inc = np.zeros((len(usuarios), len(corpus)), dtype=int)
for col, sublist in enumerate(corpus):
    for usuario in sublist:
        if pd.notna(usuario):
            mtx_inc[usuario_indice[usuario], col] = 1

# Criando a matriz de similaridade
mtx_sim = np.dot(mtx_inc, mtx_inc.T)
np.fill_diagonal(mtx_sim, 0)

# Convertendo a matriz de similaridade para tipo nativo do Python
mtx_sim = mtx_sim.astype(int)

# Criando a matriz de coocorrência
mtx_co = np.zeros((len(usuarios), len(usuarios)), dtype=int)
for sublist in corpus:
    sublist_usuarios = [usuario_indice[usuario] for usuario in sublist if pd.notna(usuario)]
    for i in range(len(sublist_usuarios)):
        for j in range(i + 1, len(sublist_usuarios)):
            mtx_co[sublist_usuarios[i], sublist_usuarios[j]] += 1
            mtx_co[sublist_usuarios[j], sublist_usuarios[i]] += 1
np.fill_diagonal(mtx_co, 0)

# Convertendo a matriz de coocorrência para tipo nativo do Python
mtx_co = mtx_co.astype(int)

# Função para criar e visualizar o grafo de incidência
def draw_incidencia_graph(corpus, usuarios):
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
    nt = Network(notebook=True)
    nt.from_nx(G_incidencia)
    nt.show("grafo_incidencia.html")

# Função para criar e visualizar o grafo de similaridade
def draw_similarity_graph(mtx_sim, usuarios):
    G_similaridade = nx.Graph()
    for i in range(len(usuarios)):
        for j in range(i + 1, len(usuarios)):
            if mtx_sim[i, j] > 0:
                G_similaridade.add_edge(usuarios[i], usuarios[j], weight=int(mtx_sim[i, j]))

    # Desenhando o grafo de similaridade
    nt = Network(notebook=True)
    nt.from_nx(G_similaridade)
    nt.show("grafo_similaridade.html")

# Função para criar e visualizar o grafo de coocorrência
def draw_cooccurrence_graph(mtx_co, usuarios):
    G_coocorrencia = nx.Graph()
    for i in range(len(usuarios)):
        for j in range(i + 1, len(usuarios)):
            if mtx_co[i, j] > 0:
                G_coocorrencia.add_edge(usuarios[i], usuarios[j], weight=int(mtx_co[i, j]))

    # Desenhando o grafo de coocorrência
    nt = Network(notebook=True)
    nt.from_nx(G_coocorrencia)
    nt.show("grafo_coocorrencia.html")

# Função para calcular e exibir as métricas dos grafos
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

# Desenhando os grafos
draw_incidencia_graph(corpus, usuarios)
draw_similarity_graph(mtx_sim, usuarios)
draw_cooccurrence_graph(mtx_co, usuarios)

# Calculando e exibindo as métricas dos grafos
G_similaridade = nx.Graph()
for i in range(len(usuarios)):
    for j in range(i + 1, len(usuarios)):
        if mtx_sim[i, j] > 0:
            G_similaridade.add_edge(usuarios[i], usuarios[j], weight=int(mtx_sim[i, j]))

G_coocorrencia = nx.Graph()
for i in range(len(usuarios)):
    for j in range(i + 1, len(usuarios)):
        if mtx_co[i, j] > 0:
            G_coocorrencia.add_edge(usuarios[i], usuarios[j], weight=int(mtx_co[i, j]))

graph_metrics(G_similaridade, "de similaridade")
graph_metrics(G_coocorrencia, "de co-ocorrência")
graph_metrics(G_incidencia, "de incidência")
