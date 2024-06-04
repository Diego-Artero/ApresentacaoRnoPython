import networkx as nx

influenciadores = nx.Graph()
qtd_vert = int(input("Quantas pessoas você quer adicionar? "))
for nmr in range(qtd_vert):
    nome_pessoa = input("Qual o nome da pessoa? ").capitalize()
    vertice = int(input(f"Quantos influenciadores o(a) {nome_pessoa} segue? "))

    influenciadores.add_node(nome_pessoa)

    for vertices in range(vertice):
        if vertice >= 0:
            contador = vertices + 1
            nome = input(f"Nome do influenciador N°{contador} que o(a) {nome_pessoa} segue: ").capitalize()
            influenciadores.add_node(nome)
            influenciadores.add_edge(nome_pessoa, nome, weight=1)

numero_vertice = influenciadores.number_of_nodes()
numero_arestas = influenciadores.number_of_edges()
ligacoes = list(influenciadores.edges(data=True))
nomes_vertices = list(influenciadores.nodes)
graus = influenciadores.degree()
acumuladora = sum(dict(graus).values())

print(f"Os graus dos vértices são: {dict(graus)}")
print(f"O grau médio é {acumuladora / influenciadores.number_of_nodes():.2f}")
print(f"Os vértices são: {nomes_vertices}")
print(f"O Grafo possui {numero_vertice} vertices, {numero_arestas} arestas e suas ligações são: {ligacoes}.")
print("Os pesos das arestas são:")
for u, v, wt in influenciadores.edges(data='weight'):
    print(f"({u} -> {v}, peso: {wt})")
contapeso = 0
for p in influenciadores.edges():
  contapeso += wt
print(f"A força de conectividade média é: {contapeso / numero_arestas}")
densidade = (2 * len(ligacoes)) / (numero_vertice * (numero_vertice - 1)) if numero_vertice > 1 else 0
print(f"O grafo possui densidade = {densidade:.2f}")