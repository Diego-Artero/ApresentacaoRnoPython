Análise de Redes Sociais

Este projeto consiste na análise de redes sociais a partir de dados fornecidos em um arquivo Excel. O objetivo é visualizar e analisar as relações entre os usuários com base em sua interação em eventos específicos.
Como Funciona

    Carregamento de Dados: Os dados são carregados a partir de um arquivo Excel fornecido como entrada.

    Pré-processamento: Os dados são pré-processados para remover valores vazios e transformados em uma representação adequada para a análise de redes.

    Criação de Redes: São criadas redes de incidência, similaridade e co-ocorrência com base nos dados fornecidos.

    Visualização: As redes são visualizadas utilizando a biblioteca Pyvis, permitindo a interação com os elementos do grafo.

    Análise: São calculadas métricas de cada rede, como número de vértices, número de arestas, grau médio, densidade, entre outros.

Como Utilizar

    Instalação das Dependências: Certifique-se de ter instalado as bibliotecas necessárias listadas no arquivo requirements.txt. Você pode instalá-las utilizando o comando:

    pip install pandas numpy networkx pyvis

    Execução do Código: Execute o script main.py em um ambiente Python. Certifique-se de ter o arquivo Excel fornecido no mesmo diretório.

    Visualização dos Resultados: Após a execução do script, serão gerados arquivos HTML contendo as visualizações das redes. Abra esses arquivos em um navegador da web para interagir com as redes.

Estrutura do Projeto

    main.py: Script principal para análise das redes sociais.
    ArquivoRespostas.xlsx: Arquivo Excel contendo os dados de entrada.
