"""
Hamiltonian Path Finder using Backtracking

Definição de Caminho Hamiltoniano:
Um caminho Hamiltoniano é um caminho em um grafo que visita cada vértice exatamente
uma vez. Diferente de um ciclo Hamiltoniano, o caminho não precisa fechar em um ciclo.
Em grafos orientados, as arestas têm direção; em grafos não orientados, as arestas
são bidirecionais.

Ideia do Backtracking:
O algoritmo tenta construir o caminho vértice por vértice. Em cada passo, escolhe
um vértice adjacente não visitado, adiciona ao caminho, e recursivamente tenta
completar o caminho. Se não conseguir completar com essa escolha, faz backtrack
(remove o vértice do caminho) e tenta a próxima opção. O processo continua até
encontrar um caminho válido ou esgotar todas as possibilidades.

Complexidade Temporal:
No pior caso, o algoritmo pode explorar todos os possíveis caminhos, resultando
em uma complexidade de O(n!) onde n é o número de vértices. Isso ocorre porque,
após escolher o primeiro vértice, há até n-1 escolhas para o segundo, n-2 para o
terceiro, e assim por diante.

Por que o Teorema Mestre não se aplica:
O Teorema Mestre é usado para resolver relações de recorrência da forma T(n) = aT(n/b) + f(n).
No backtracking do caminho Hamiltoniano, a árvore de recursão não divide o problema
de forma equilibrada (não é T(n) = aT(n/b) + f(n)). Cada chamada recursiva explora
diferentes ramificações do espaço de busca, e o número de subproblemas pode variar
grandemente dependendo da estrutura do grafo. A relação de recorrência seria algo
mais complexo como T(n) ≤ n! em vez de uma forma que o Teorema Mestre pode resolver.
"""

from typing import Optional
import argparse
import sys


class Graph:
    """
    Representa um grafo orientado ou não orientado com n vértices.
    
    Usa sets de adjacências (list[set[int]]) para verificação O(1) e evitar duplicatas.
    """
    
    def __init__(self, n: int, directed: bool) -> None:
        """
        Inicializa grafo com n vértices.
        
        Args:
            n: Número de vértices (0-indexed: 0 a n-1)
            directed: Se True, grafo é orientado; caso contrário, não orientado
        """
        self.n = n
        self.directed = directed
        # Sets de adjacências: adj[u] contém set de vértices adjacentes a u
        self.adj: list[set[int]] = [set() for _ in range(n)]
    
    def add_edge(self, u: int, v: int) -> None:
        """
        Adiciona aresta de u para v.
        
        Args:
            u: Vértice origem
            v: Vértice destino
        
        Invariante: u e v estão no intervalo [0, n-1], e u != v (ignora laços).
                    Sets garantem O(1) para checagem e eliminação automática de duplicatas.
        """
        # Ignora laços
        if u == v:
            return
        
        # Valida índices
        if not (0 <= u < self.n and 0 <= v < self.n):
            return
        
        # Adiciona aresta (set adiciona sem duplicatas automaticamente)
        self.adj[u].add(v)
        
        # Se não orientado, adiciona aresta reversa
        if not self.directed:
            self.adj[v].add(u)
    
    def neighbors(self, u: int) -> list[int]:
        """
        Retorna lista de vizinhos do vértice u, ordenada por grau crescente.
        
        Heurística: ordena vizinhos por grau (graus menores primeiro) para reduzir
        o branching factor no backtracking, explorando primeiro vértices com menos
        opções, o que tende a podar mais cedo subárvores infrutíferas.
        
        Args:
            u: Vértice
        
        Returns:
            Lista de vértices adjacentes a u ordenada por grau ascendente
        
        Invariante: u está no intervalo [0, n-1]
        """
        if not (0 <= u < self.n):
            return []
        # Ordena por grau crescente do vizinho (heurística de poda)
        return sorted(self.adj[u], key=lambda x: len(self.adj[x]))


def is_hamiltonian_path(g: Graph, path: list[int]) -> bool:
    """
    Valida se o caminho é um caminho Hamiltoniano válido.
    
    Args:
        g: Grafo
        path: Lista de vértices representando o caminho
    
    Returns:
        True se path é um caminho Hamiltoniano válido, False caso contrário
    
    Invariante: path contém apenas índices válidos [0, n-1]
    """
    n = g.n
    
    # Verifica comprimento
    if len(path) != n:
        return False
    
    # Verifica que cada vértice aparece exatamente uma vez
    if set(path) != set(range(n)):
        return False
    
    # Verifica que arestas consecutivas existem no grafo
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        
        # Para grafos orientados, verifica direção
        if g.directed:
            if v not in g.neighbors(u):
                return False
        else:
            # Para grafos não orientados, verifica adjacência em qualquer direção
            if v not in g.neighbors(u):
                return False
    
    return True


def _backtrack(
    g: Graph,
    current: int,
    path: list[int],
    visited: list[bool]
) -> Optional[list[int]]:
    """
    Função auxiliar recursiva para busca de caminho Hamiltoniano via backtracking.
    
    Usa heurística de ordenação por grau (via neighbors()) para explorar primeiro
    vértices com menos vizinhos, o que tende a podar mais cedo subárvores infrutíferas.
    
    Args:
        g: Grafo
        current: Vértice atual no caminho
        path: Caminho atual (lista mutável)
        visited: Lista de booleanos indicando vértices visitados
    
    Returns:
        Lista de vértices representando caminho Hamiltoniano, ou None se não existe
    
    Invariante: len(path) = número de vértices visitados
    """
    # Base: caminho completo encontrado
    if len(path) == g.n:
        return path.copy()
    
    # Explora vizinhos não visitados ordenados por grau crescente (heurística)
    for neighbor in g.neighbors(current):
        if not visited[neighbor]:
            # Tenta incluir neighbor no caminho
            visited[neighbor] = True
            path.append(neighbor)
            
            # Recursão
            result = _backtrack(g, neighbor, path, visited)
            
            # Se encontrou solução, retorna
            if result is not None:
                return result
            
            # Backtrack: remove neighbor e tenta próxima opção
            path.pop()
            visited[neighbor] = False
    
    # Nenhuma solução encontrada com caminho atual
    return None


def find_hamiltonian_path(g: Graph) -> Optional[list[int]]:
    """
    Encontra um caminho Hamiltoniano no grafo usando backtracking.
    
    Tenta começar em cada vértice para garantir robustez. Usa heurística de
    ordenação por grau (via neighbors()) para reduzir branching no backtracking.
    
    Args:
        g: Grafo (orientado ou não)
    
    Returns:
        Lista de vértices representando caminho Hamiltoniano, ou None se não existe
    
    Complexidade: O(n!) no pior caso. Heurística por grau melhora casos práticos.
    """
    n = g.n
    
    # Casos especiais
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    # Tenta começar em cada vértice
    for start in range(n):
        visited = [False] * n
        path = []
        
        # Marca vértice inicial como visitado
        visited[start] = True
        path.append(start)
        
        # Busca recursiva com heurística de ordenação por grau
        result = _backtrack(g, start, path, visited)
        
        if result is not None:
            return result
    
    return None


def _self_test() -> None:
    """
    Executa testes automáticos para validar implementação.
    
    Testa múltiplos cenários:
    - Caminho trivial (1 vértice)
    - Grafo pequeno com caminho (orientado e não orientado)
    - Grafo sem caminho
    - Grafo desconexo
    - Grafo não orientado sem caminho (componente isolado)
    - Grafo orientado com caminho de tamanho n
    """
    
    # Teste 1: Grafo trivial com 1 vértice
    print("Teste 1: Grafo com 1 vértice...")
    g1 = Graph(1, directed=True)
    path1 = find_hamiltonian_path(g1)
    assert path1 == [0], f"Esperado [0], obtido {path1}"
    assert is_hamiltonian_path(g1, path1), "Validação falhou para path1"
    print("Passou")
    
    # Teste 2: Grafo pequeno 3 vértices, orientado, com caminho
    print("Teste 2: Grafo 3 vértices orientado com caminho...")
    g2 = Graph(3, directed=True)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    path2 = find_hamiltonian_path(g2)
    assert path2 == [0, 1, 2], f"Esperado [0, 1, 2], obtido {path2}"
    assert is_hamiltonian_path(g2, path2), "Validação falhou para path2"
    print("Passou")
    
    # Teste 3: Grafo 3 vértices, não orientado, com caminho
    print("Teste 3: Grafo 3 vértices não orientado com caminho...")
    g3 = Graph(3, directed=False)
    g3.add_edge(0, 1)
    g3.add_edge(1, 2)
    path3 = find_hamiltonian_path(g3)
    assert path3 == [0, 1, 2] or path3 == [2, 1, 0], \
        f"Esperado [0, 1, 2] ou [2, 1, 0], obtido {path3}"
    assert is_hamiltonian_path(g3, path3), "Validação falhou para path3"
    print("Passou")
    
    # Teste 4: Grafo sem caminho Hamiltoniano (isolado)
    print("Teste 4: Grafo orientado sem caminho Hamiltoniano...")
    g4 = Graph(3, directed=True)
    g4.add_edge(0, 1)
    # Vértice 2 isolado
    path4 = find_hamiltonian_path(g4)
    assert path4 is None, f"Esperado None, obtido {path4}"
    print("Passou")
    
    # Teste 5: Grafo completo (deve ter caminho)
    print("Teste 5: Grafo completo 4 vértices...")
    g5 = Graph(4, directed=False)
    for u in range(4):
        for v in range(u + 1, 4):
            g5.add_edge(u, v)
    path5 = find_hamiltonian_path(g5)
    assert path5 is not None and len(path5) == 4, \
        f"Caminho deve existir, obtido {path5}"
    assert is_hamiltonian_path(g5, path5), "Validação falhou para path5"
    print("Passou")
    
    # Teste 6: Validar is_hamiltonian_path com caminho inválido
    print("Teste 6: Validação de caminho inválido...")
    g6 = Graph(4, directed=False)
    g6.add_edge(0, 1)
    g6.add_edge(1, 2)
    g6.add_edge(2, 3)
    # Caminho com gap (0 -> 2 não é aresta)
    assert not is_hamiltonian_path(g6, [0, 2, 1, 3]), \
        "Deve falhar: aresta 0-2 não existe"
    print("Passou")
    
    # Teste 7: Grafo não orientado SEM caminho (componente isolado)
    print("Teste 7: Grafo não orientado sem caminho (componente isolado)...")
    g7 = Graph(4, directed=False)
    g7.add_edge(0, 1)  # Componente 0-1
    g7.add_edge(2, 3)  # Componente 2-3 (isolado)
    path7 = find_hamiltonian_path(g7)
    assert path7 is None, f"Esperado None (desconexo), obtido {path7}"
    print("Passou")
    
    # Teste 8: Grafo orientado COM caminho de tamanho n
    print("Teste 8: Grafo orientado com caminho de tamanho n...")
    g8 = Graph(5, directed=True)
    g8.add_edge(0, 1)
    g8.add_edge(1, 2)
    g8.add_edge(2, 3)
    g8.add_edge(3, 4)
    path8 = find_hamiltonian_path(g8)
    assert path8 is not None and len(path8) == 5, \
        f"Caminho deve existir, obtido {path8}"
    assert path8 == [0, 1, 2, 3, 4], f"Esperado [0,1,2,3,4], obtido {path8}"
    assert is_hamiltonian_path(g8, path8), "Validação falhou para path8"
    print("Passou")
    
    print("\nTodos os testes passaram!")


def _read_graph_from_file(filepath: str, directed: bool) -> Graph:
    """
    Lê grafo de arquivo de texto.
    
    Formato:
        Primeira linha: n m
        Próximas m linhas: u v
    
    Args:
        filepath: Caminho do arquivo
        directed: Se grafo é orientado
    
    Returns:
        Grafo lido
    
    Raises:
        FileNotFoundError: Se arquivo não existe
        ValueError: Se formato é inválido
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{filepath}' não encontrado")
    
    if len(lines) < 1:
        raise ValueError("Arquivo vazio")
    
    # Lê n e m
    try:
        n, m = map(int, lines[0].strip().split())
    except ValueError:
        raise ValueError("Formato inválido na primeira linha. Use: n m")
    
    g = Graph(n, directed)
    
    # Lê arestas
    for i in range(1, min(m + 1, len(lines))):
        line = lines[i].strip()
        if not line:
            continue
        try:
            u, v = map(int, line.split())
            g.add_edge(u, v)
        except ValueError:
            raise ValueError(f"Formato inválido na linha {i + 1}. Use: u v")
    
    return g


def _demo_examples() -> None:
    """
    Executa exemplos demonstrativos sem arquivo.
    
    Mostra 2 grafos: um com caminho Hamiltoniano e outro sem.
    """
    
    print("=" * 60)
    print("Exemplo 1: Grafo não orientado COM caminho Hamiltoniano")
    print("=" * 60)
    
    # Exemplo 1: Grafo com caminho
    g1 = Graph(5, directed=False)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)
    g1.add_edge(3, 4)
    g1.add_edge(4, 0)
    
    path1 = find_hamiltonian_path(g1)
    if path1:
        print("Caminho encontrado:", " ".join(map(str, path1)))
    else:
        print("NO HAMILTONIAN PATH")
    
    print("\n" + "=" * 60)
    print("Exemplo 2: Grafo orientado SEM caminho Hamiltoniano")
    print("=" * 60)
    
    # Exemplo 2: Grafo sem caminho (desconexo)
    g2 = Graph(4, directed=True)
    g2.add_edge(0, 1)
    g2.add_edge(1, 0)  # Apenas ciclo pequeno
    # Vértices 2 e 3 isolados
    
    path2 = find_hamiltonian_path(g2)
    if path2:
        print("Caminho encontrado:", " ".join(map(str, path2)))
    else:
        print("NO HAMILTONIAN PATH")


def main() -> None:
    """CLI principal usando argparse."""
    
    parser = argparse.ArgumentParser(
        description="Encontra caminho Hamiltoniano via backtracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos:
  python main.py --undirected --file input.txt
  python main.py --directed --file input.txt
  python main.py  # mostra exemplos
  python main.py --self-test
        """
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Arquivo de entrada com o grafo'
    )
    
    parser.add_argument(
        '--directed',
        action='store_true',
        help='Grafo é orientado'
    )
    
    parser.add_argument(
        '--undirected',
        action='store_true',
        help='Grafo é não orientado'
    )
    
    parser.add_argument(
        '--self-test',
        action='store_true',
        help='Executa testes automáticos'
    )
    
    args = parser.parse_args()
    
    # Modo self-test
    if args.self_test:
        _self_test()
        return
    
    # Modo com arquivo
    if args.file:
        # Valida: não pode passar ambos --directed e --undirected juntos
        if args.directed and args.undirected:
            print("Erro: Não é possível especificar --directed e --undirected simultaneamente", 
                  file=sys.stderr)
            sys.exit(1)
        
        # Valida: deve especificar um dos dois
        if not args.directed and not args.undirected:
            print("Erro: Especifique --directed ou --undirected (não ambos)", file=sys.stderr)
            sys.exit(1)
        
        directed = args.directed
        
        try:
            g = _read_graph_from_file(args.file, directed)
        except (FileNotFoundError, ValueError) as e:
            print(f"Erro: {e}", file=sys.stderr)
            sys.exit(1)
        
        path = find_hamiltonian_path(g)
        
        if path is None:
            print("NO HAMILTONIAN PATH")
        else:
            print(" ".join(map(str, path)))
    
    else:
        # Modo demonstração (sem arquivo)
        _demo_examples()


if __name__ == "__main__":
    main()

