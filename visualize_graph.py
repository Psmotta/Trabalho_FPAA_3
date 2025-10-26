"""
Módulo de Visualização para Caminho Hamiltoniano

Este módulo fornece funcionalidades para visualizar grafos e destacar
caminhos Hamiltonianos encontrados usando NetworkX e Matplotlib.

Requisitos externos:
    - networkx: para estrutura de grafo
    - matplotlib: para plotagem

Uso:
    python visualize_graph.py  # executa exemplo
    ou
    from visualize_graph import visualize_graph
    visualize_graph(grafo, caminho, "assets/grafo.png")
"""

import os
from typing import Optional, List
import networkx as nx
import matplotlib.pyplot as plt
from main import Graph, find_hamiltonian_path


def visualize_graph(g: Graph, path: Optional[List[int]], output_path: str = "assets/graph.png") -> str:
    """
    Visualiza um grafo e destaca o caminho Hamiltoniano encontrado.
    
    Converte o grafo da classe Graph para NetworkX, plotando com destaque
    para arestas e vértices que fazem parte do caminho Hamiltoniano.
    
    Args:
        g: Grafo (orientado ou não orientado) a ser visualizado
        path: Caminho Hamiltoniano encontrado (pode ser None se não existir)
        output_path: Caminho onde a imagem será salva (default: "assets/graph.png")
    
    Returns:
        str: Caminho absoluto do arquivo salvo
    
    Raises:
        OSError: Se não conseguir criar diretório ou salvar arquivo
    
    Exemplo:
        >>> g = Graph(5, directed=False)
        >>> g.add_edge(0, 1)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(3, 4)
        >>> path = [0, 1, 2, 3, 4]
        >>> visualize_graph(g, path, "assets/exemplo.png")
        'C:/projeto/assets/exemplo.png'
    """
    # Cria diretório assets se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Cria grafo NetworkX apropriado para orientado/não orientado
    if g.directed:
        nx_graph = nx.DiGraph()
    else:
        nx_graph = nx.Graph()
    
    # Adiciona todos os vértices ao grafo NetworkX
    nx_graph.add_nodes_from(range(g.n))
    
    # Adiciona todas as arestas ao grafo NetworkX
    for u in range(g.n):
        for v in g.neighbors(u):
            if g.directed or u < v:  # Evita duplicatas em grafo não orientado
                nx_graph.add_edge(u, v)
    
    # Calcula layout do grafo (posicionamento dos nós)
    pos = nx.spring_layout(nx_graph, seed=42, k=1, iterations=50)
    
    # Cria figura para plotagem
    plt.figure(figsize=(12, 8))
    plt.title("Caminho Hamiltoniano no Grafo", fontsize=16, fontweight='bold')
    
    # Se existir caminho, extrai arestas que fazem parte do caminho
    path_edges = []
    if path and len(path) > 1:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    
    # Separa arestas do caminho das demais
    normal_edges = [e for e in nx_graph.edges() if e not in path_edges and (e[1], e[0]) not in path_edges]
    
    # Desenha arestas normais (não fazem parte do caminho)
    nx.draw_networkx_edges(
        nx_graph, pos, 
        edgelist=normal_edges,
        edge_color='lightgray',
        width=1,
        alpha=0.5,
        arrows=True if g.directed else False,
        arrowsize=20,
        arrowstyle='->',
        connectionstyle='arc3,rad=0.1'
    )
    
    # Desenha arestas que fazem parte do caminho Hamiltoniano (se existir)
    if path and len(path) > 1:
        nx.draw_networkx_edges(
            nx_graph, pos,
            edgelist=path_edges,
            edge_color='red',
            width=3,
            alpha=0.8,
            arrows=True if g.directed else False,
            arrowsize=25,
            arrowstyle='->',
            connectionstyle='arc3,rad=0.1',
            style='solid'
        )
    
    # Desenha todos os nós
    nx.draw_networkx_nodes(
        nx_graph, pos,
        node_color='lightblue',
        node_size=800,
        alpha=0.7,
        edgecolors='black',
        linewidths=1
    )
    
    # Destaca nós que fazem parte do caminho Hamiltoniano (se existir)
    if path:
        nx.draw_networkx_nodes(
            nx_graph, pos,
            nodelist=path,
            node_color='lightgreen',
            node_size=1000,
            alpha=0.9,
            edgecolors='darkgreen',
            linewidths=2
        )
    
    # Adiciona labels aos nós (números)
    nx.draw_networkx_labels(nx_graph, pos, font_size=10, font_weight='bold')
    
    # Ajusta layout e remove eixos
    plt.axis('off')
    plt.tight_layout()
    
    # Salva a imagem
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Retorna caminho absoluto do arquivo salvo
    abs_path = os.path.abspath(output_path)
    
    # Se não existe caminho, imprime alerta
    if path is None or len(path) == 0:
        print(f"[VISUALIZAÇÃO] Grafo salvo sem caminho Hamiltoniano em: {abs_path}")
    else:
        print(f"[VISUALIZAÇÃO] Caminho Hamiltoniano visualizado e salvo em: {abs_path}")
    
    return abs_path


def exemplo_visualizacao() -> None:
    """
    Exemplo de uso do módulo de visualização.
    
    Cria o mesmo grafo do exemplo da função _demo_examples() do main.py
    (grafo não orientado com caminho Hamiltoniano) e visualiza.
    """
    print("=" * 60)
    print("Exemplo de Visualização: Caminho Hamiltoniano")
    print("=" * 60)
    
    # Cria grafo não orientado (mesmo do exemplo do main.py)
    g = Graph(5, directed=False)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 0)
    
    # Busca caminho Hamiltoniano
    path = find_hamiltonian_path(g)
    
    # Visualiza e salva
    output_file = visualize_graph(g, path, "assets/exemplo_hamiltoniano.png")
    
    print(f"\nGrafo visualizado com {g.n} vértices e {sum(len(g.adj[u]) for u in range(g.n)) // 2 if not g.directed else sum(len(g.adj[u]) for u in range(g.n))} arestas")
    print(f"Imagem salva em: {output_file}")
    
    if path:
        print(f"Caminho encontrado: {' → '.join(map(str, path))}")
    else:
        print("Nenhum caminho Hamiltoniano encontrado.")


def exemplo_sem_caminho() -> None:
    """
    Exemplo visualizando grafo sem caminho Hamiltoniano.
    
    Cria um grafo orientado com vértices isolados para demonstrar
    visualização sem caminho.
    """
    print("\n" + "=" * 60)
    print("Exemplo de Visualização: SEM Caminho Hamiltoniano")
    print("=" * 60)
    
    # Cria grafo orientado sem caminho (mesmo do exemplo 2 do main.py)
    g = Graph(4, directed=True)
    g.add_edge(0, 1)
    g.add_edge(1, 0)  # Apenas ciclo pequeno
    # Vértices 2 e 3 isolados
    
    # Busca caminho Hamiltoniano
    path = find_hamiltonian_path(g)
    
    # Visualiza e salva
    output_file = visualize_graph(g, path, "assets/exemplo_sem_caminho.png")
    
    print(f"\nGrafo visualizado com {g.n} vértices")
    print(f"Imagem salva em: {output_file}")
    
    if path:
        print(f"Caminho encontrado: {' → '.join(map(str, path))}")
    else:
        print("Nenhum caminho Hamiltoniano encontrado.")


def exemplo_grafo_completo() -> None:
    """
    Exemplo com grafo completo de 6 vértices.
    
    Demonstra visualização de grafo denso com caminho Hamiltoniano.
    """
    print("\n" + "=" * 60)
    print("Exemplo de Visualização: Grafo Completo")
    print("=" * 60)
    
    # Cria grafo completo de 6 vértices
    g = Graph(6, directed=False)
    for u in range(6):
        for v in range(u + 1, 6):
            g.add_edge(u, v)
    
    # Busca caminho Hamiltoniano
    path = find_hamiltonian_path(g)
    
    # Visualiza e salva
    output_file = visualize_graph(g, path, "assets/exemplo_completo.png")
    
    print(f"\nGrafo completo com {g.n} vértices")
    print(f"Imagem salva em: {output_file}")
    
    if path:
        print(f"Um dos caminhos possíveis: {' → '.join(map(str, path))}")
    else:
        print("Nenhum caminho Hamiltoniano encontrado.")


if __name__ == "__main__":
    """
    Executa exemplos de visualização quando o arquivo é rodado diretamente.
    
    Roda três exemplos:
    1. Grafo com caminho Hamiltoniano (exemplo do main.py)
    2. Grafo sem caminho Hamiltoniano
    3. Grafo completo com muitos caminhos
    """
    try:
        exemplo_visualizacao()
        exemplo_sem_caminho()
        exemplo_grafo_completo()
        
        print("\n" + "=" * 60)
        print("Todos os exemplos foram gerados com sucesso!")
        print("Arquivos salvos na pasta 'assets/'")
        print("=" * 60)
        
    except ImportError as e:
        print(f"Erro: Dependências não instaladas. Execute: pip install networkx matplotlib")
        print(f"Detalhes: {e}")
    except Exception as e:
        print(f"Erro ao gerar visualizações: {e}")

