import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Carregando o arquivo
corpus = pd.read_excel('ArquivoRespostas.xlsx', header=None)

# Removendo células vazias e substituindo por NA
corpus.replace("", np.nan, inplace=True)

# Transformando o corpus em uma lista de listas
corpus = corpus.values.tolist()

# Ordenando usuários
usuarios = sorted(set([item for sublist in corpus for item in sublist if pd.notna(item)]))
indice_usuario = {usuario: i for i, usuario in enumerate(usuarios)}

# Matriz de incidência
mtx_inc = np.zeros((len(usuarios), len(corpus)), dtype=int)
for col, sublist in enumerate(corpus):
    for usuario in sublist:
        if pd.notna(usuario):
            mtx_inc[indice_usuario[usuario], col] = 1

# Matriz de similaridade
mtx_sim = np.dot(mtx_inc, mtx_inc.T)
np.fill_diagonal(mtx_sim, 0)

# Matriz de co-ocorrência
mtx_co = np.zeros((len(usuarios), len(usuarios)), dtype=int)
for sublist in corpus:
    sublist_usuarios = [indice_usuario[usuario] for usuario in sublist if pd.notna(usuario)]
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
eventos = list(range(len(corpus)))
for evento in eventos:
    G_incidencia.add_node(f'Evento_{evento}', bipartite=1)

# Adicionando arestas entre usuários e eventos
for col, sublist in enumerate(corpus):
    for usuario in sublist:
        if pd.notna(usuario):
            G_incidencia.add_edge(usuario, f'Evento_{col}')

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
pesos = [G_similaridade[u][v]['weight'] for u, v in G_similaridade.edges()]
nx.draw(G_similaridade, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', width=pesos)
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
pesos = [G_coocorrencia[u][v]['weight'] for u, v in G_coocorrencia.edges()]
nx.draw(G_coocorrencia, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', width=pesos)
plt.title('Grafo de Coocorrência')
plt.show()

# Métricas topológicas
def metricas_grafo(grafo, nome_grafo):
    print(f"Métricas do grafo {nome_grafo}:")
    print("Número de vértices:", grafo.number_of_nodes())
    print("Número de arestas:", grafo.number_of_edges())
    graus = dict(grafo.degree())
    print("Graus de vértice:", graus)
    grau_medio = np.mean(list(graus.values()))
    print("Grau médio:", grau_medio)
    if nx.is_weighted(grafo):
        pesos = nx.get_edge_attributes(grafo, 'weight')
        peso_medio = np.mean(list(pesos.values()))
        print("Força de conectividade média:", peso_medio)
    densidade = nx.density(grafo)
    print("Densidade da rede:", densidade)

metricas_grafo(G_incidencia, "de incidência")
metricas_grafo(G_similaridade, "de similaridade")
metricas_grafo(G_coocorrencia, "de co-ocorrência")
