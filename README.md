# Caminho Hamiltoniano via Backtracking (Python)

Projeto desenvolvido para determinar se existe um Caminho Hamiltoniano em um grafo orientado ou não orientado, utilizando a técnica de **backtracking** com **heurística por grau** para reduzir o espaço de busca.

Este README contém:
✅ Descrição detalhada da implementação  
✅ Instruções para execução do projeto  
✅ Relatório técnico conforme solicitado pelo professor  

**Versão do Python utilizada:** Python 3.10+

---

## 📌 Descrição do Projeto

### O que é Caminho Hamiltoniano?
Um **Caminho Hamiltoniano** é um caminho que passa por **todos os vértices do grafo exatamente uma vez**.  
Não precisa retornar ao vértice inicial (diferente do ciclo Hamiltoniano).

### A Estratégia de Backtracking
A busca tenta construir o caminho incrementalmente:

1. Escolhe um vértice inicial
2. Marca como visitado
3. Escolhe um vizinho ainda não visitado
4. Adiciona ao caminho e continua a recursão
5. Caso fique sem opções, desfaz a escolha (**backtrack**)
6. Repete até encontrar um caminho completo ou esgotar opções

Heurística aplicada:
> Vizinhos são explorados em **ordem crescente de grau**, para podar subárvores mais cedo.

---

## 🧠 Implementação Explicada (linha a linha das principais funções)

### `class Graph`
Representa o grafo como lista de adjacências com sets:

```python
self.adj: list[set[int]] = [set() for _ in range(n)]
```

Sets ajudam a garantir:
✔ Checagem O(1)  
✔ Sem duplicatas de arestas  
*(Laços são ignorados explicitamente no código)*

Principais métodos:
- `add_edge(u, v)`  
  - Ignora laços  
  - Valida limites  
  - Se não orientado, cria aresta bidirecional
- `neighbors(u)`  
  - Retorna vizinhos **ordenados por grau crescente**

---

### `find_hamiltonian_path(g)`
1. Trata casos especiais: n=0 → `[]`; n=1 → `[0]`
2. Tenta iniciar o caminho de cada vértice
3. Cria lista `visited` para controle de visitados
4. Insere vértice no caminho
5. Chama `_backtrack(...)`
6. Se encontrar solução → retorna
7. Se não → tenta outro início

Complexidade: **O(n!)** no pior caso

---

### `_backtrack(g, current, path, visited)`
Lógica completa do backtracking:

```python
if len(path) == g.n:
    return path.copy()

for neighbor in g.neighbors(current):
    if not visited[neighbor]:
        visited[neighbor] = True
        path.append(neighbor)

        result = _backtrack(g, neighbor, path, visited)
        if result is not None:
            return result

        path.pop()
        visited[neighbor] = False
```

Explicando:
- ✅ Base: encontrou caminho completo
- 🔄 Explora vizinhos ordenados por grau
- 🔁 Marca → recursa → verifica sucesso
- ❌ Não funcionou? desfaz e tenta o próximo

---

### `is_hamiltonian_path(g, path)`
Validação completa:
✅ Tamanho correto  
✅ Todo vértice aparece exatamente 1 vez  
✅ Existe aresta entre consecutivos (respeitando orientação)

---

### CLI (`main.py`)
Argumentos suportados:

| Argumento | Descrição |
|----------|-----------|
| `--file` | usa entrada via arquivo |
| `--directed` | define grafo orientado |
| `--undirected` | define grafo não orientado |
| `--self-test` | executa testes automáticos |

Validações:
⚠️ **Não permite** usar `--directed` e `--undirected` juntos  
⚠️ Obrigatório definir um deles ao usar `--file`

---

## ▶️ Como Executar

### 1) Criar ambiente virtual (Recomendado)

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2) Instalar dependências (para módulo de visualização)

O módulo principal (`main.py`) **não requer dependências externas**! 🎉

Para usar o módulo de visualização (`visualize_graph.py`), instale as dependências:

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:
```bash
pip install networkx matplotlib
```

---

### 3) Rodar o programa

**Modo demonstração:**
```bash
python main.py
```

**Rodar auto testes:**
```bash
python main.py --self-test
```

**Com arquivo (grafo não orientado):**
```bash
python main.py --undirected --file input.txt
```

**Com arquivo (grafo orientado):**
```bash
python main.py --directed --file input.txt
```

---

## 📄 Formato do arquivo de entrada

Exemplo (`input.txt`):
```
5 6
0 1
1 2
2 3
3 4
0 4
1 3
```

Se houver caminho:
```
0 1 2 3 4
```

Caso contrário:
```
NO HAMILTONIAN PATH
```

---

## 📘 Relatório Técnico

### ✅ Classificação do Problema
| Classe | Descrição |
|--------|-----------|
| **P** | problemas com solução polinomial |
| **NP** | soluções verificáveis em polinomial |
| **NP-Completo** | os mais difíceis dentro de NP |
| **NP-Difícil** | tão difíceis quanto NP-Completo, mas não necessariamente verificáveis em NP |

O **problema de determinar um caminho Hamiltoniano é NP-Completo**.

Ligação com TSP:
- TSP (decisão) reduz para Hamiltoniano e vice-versa
- Resolver um implica resolver o outro polinomialmente

---

### ✅ Complexidade de Tempo do Algoritmo

| Cenário | Complexidade | Observação |
|--------|--------------|------------|
| Melhor caso | O(n) | Caminho direto |
| Caso médio | Entre O(n²) e O(cⁿ) | Varia com densidade e heurística |
| Pior caso | **O(n!)** | Explora permutações de vertices |

**Por quê?**  
Após escolher o primeiro vértice, há:
```
(n-1) * (n-2) * ... * 1 = n!
```

O Teorema Mestre **não se aplica** pois:
- não há divisão balanceada em subproblemas
- branching variável
- dependência do estado global (visited)

### ✅ Complexidade de Espaço
- Grafo: O(n + m)
- Estruturas auxiliares: O(n)
- Pilha de recursão: O(n)

---

## 🧪 Exemplos Reais de Execução

Todos presentes no programa via `--self-test`, incluindo:
- grafos orientados ✅/❌
- grafos não orientados ✅/❌
- casos triviais
- componentes desconexos

> Resultado: **todos os testes passaram** ✅

---

## 📂 Estrutura do Projeto

```
.
├── main.py              # Implementação principal do algoritmo
├── visualize_graph.py   # (Extra) Módulo de visualização com NetworkX
├── requirements.txt      # Dependências do módulo de visualização
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Este arquivo
└── assets/              # Imagens geradas pela visualização
    └── *.png
```

> Você pode adicionar uma pasta `samples/` com arquivos prontos para teste  
> O `.venv/` e `__pycache__/` são ignorados pelo `.gitignore`

---

## 🎨 Módulo de Visualização (Extra)

O arquivo `visualize_graph.py` oferece visualização gráfica do grafo e do caminho Hamiltoniano encontrado.

### Instalação de Dependências

```bash
pip install networkx matplotlib
```

### Como Usar

**Opção 1: Rodar exemplos embutidos**
```bash
python visualize_graph.py
```

Isso gera 3 imagens na pasta `assets/`:
- `exemplo_hamiltoniano.png` - Grafo com caminho encontrado
- `exemplo_sem_caminho.png` - Grafo sem caminho
- `exemplo_completo.png` - Grafo completo

**Opção 2: Importar no seu código**
```python
from main import Graph, find_hamiltonian_path
from visualize_graph import visualize_graph

# Cria grafo
g = Graph(5, directed=False)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)

# Busca caminho
path = find_hamiltonian_path(g)

# Visualiza
visualize_graph(g, path, "assets/meu_grafo.png")
```

### Características da Visualização

- **Arestas do caminho**: Vermelhas e espessas (linewidth=3)
- **Vértices do caminho**: Verdes e maiores
- **Demais elementos**: Cinza claro e discretos
- **Layout automático**: spring_layout do NetworkX
- **Imagem salva automaticamente** na pasta `assets/`

### Requisitos

- Python 3.10+
- networkx: estrutura de grafo
- matplotlib: plotagem

---

## 🔍 Troubleshooting

| Erro | Possível causa | Solução |
|-----|----------------|---------|
| Arquivo não encontrado | Caminho errado | Use caminho absoluto ou `./` |
| Formato inválido | Primeira linha não tem `n m` | Verifique arquivo |
| Flags conflitantes | `--directed` + `--undirected` juntos | Use apenas uma |
| Falta flag de direção | Usou `--file` sem tipo do grafo | Informar tipo |
| ImportError (visualize) | Faltam dependências | `pip install networkx matplotlib` |

---

## 📚 Referências

- Sipser. *Introduction to the Theory of Computation*
- CLRS. *Introduction to Algorithms*
- Garey & Johnson. *Computers and Intractability*
- Knuth. *The Art of Computer Programming*
- Materiais da disciplina (P, NP, TSP)

---

## ✅ Licença
MIT — uso acadêmico liberado ✅
