import numpy as np

# ------------------------------------------------------------------------------

# Extraindo a Matriz de 'mtz_exemplo.txt'
def mtz_ex():
    matriz_adj = np.zeros((4, 5), dtype=int) # Inicializando a matriz com zeros

    # Supondo que o arquivo 'mtz_exemplo.txt' tenha 4 linhas e 5 colunas de números:
    with open('mtz_exemplo.txt', 'r') as arquivo:
        linhas = arquivo.readlines() # Lendo todas as linhas do arquivo
        for l in range(4):
            numeros = linhas[l].strip().split() # Dividindo a linha em números
            for c in range(5):  # Lendo todas as colunas do arquivo
                matriz_adj[l][c] = int(numeros[c]) # Convertendo string para int e atribuindo à matriz

    return matriz_adj # Retorna o resultado

# ------------------------------------------------------------------------------

def matriz_incidencia():
    matriz_adj = mtz_ex()

    # Determinando o número de vértices e arestas (numpy.shape encontra a dimensão de um array):
    num_vertices, num_arestas = matriz_adj.shape[0], matriz_adj.shape[1]

    # Inicializando a matriz de incidência com apenas zeros:
    matriz_inc = np.zeros((num_vertices, num_arestas), dtype=int)

    for aresta in range(num_arestas):
        for vertice in range(num_vertices):
            if matriz_adj[vertice, aresta] == 1:
                matriz_inc[vertice, aresta] = 1

    return matriz_inc

# ------------------------------------------------------------------------------

def matriz_similaridade():
    # Matriz incidência
    matriz_inc = mtz_ex()

    # Número de linhas e colunas na matriz incidência:
    num_linhas, num_colunas = matriz_inc.shape[0], matriz_inc.shape[1]

    # Dando inicío a matriz de similaridade:
    matriz_similaridade = np.zeros((num_linhas, num_linhas), dtype=int)

    # Preenchendo a matriz de similaridade:
    for i in range(num_linhas):
        for j in range(num_linhas):
            # Contando o número de colunas, onde ambas as linhas i e j têm o valor 1:
            similaridade = sum(matriz_inc[i][k] == 1 and matriz_inc[j][k] == 1 for k in range(num_colunas))
            matriz_similaridade[i][j] = similaridade

    return matriz_similaridade

# ------------------------------------------------------------------------------

def matriz_coocorrencia():

    # Chamando a função e imprimindo a matriz de incidência:
    matriz_inc = mtz_ex()

    # Nomes das colunas
    colunas = ["x", "y", "z", "w", "k"]
    tamanho_coluna = len(colunas)

    # Iniciando a matriz de coocorrência:
    matriz_coo = np.zeros((tamanho_coluna, tamanho_coluna), dtype=int)

    # Loop para preencher a matriz de coocorrência:
    for linha in matriz_inc:  # Itera sobre cada linha da matriz de incidência
        for i in range(tamanho_coluna):  # Itera sobre cada coluna "i"
            for j in range(i, tamanho_coluna):  # Itera sobre cada coluna "j" a partir de "i"
                # Verifica se ambos os elementos na linha atual são 1
                if linha[i] == 1 and linha[j] == 1:
                    # Incrementa a contagem na matriz de coocorrência
                    matriz_coo[i][j] += 1
                    if i != j:
                        # Se "i" e "j" são diferentes, incrementa também a posição simétrica
                        matriz_coo[j][i] += 1
    
    return matriz_coo
