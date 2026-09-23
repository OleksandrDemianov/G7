import networkx as nx
import numpy as np

# Ребра графа
edges = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 1),
    (1, 5),
    (2, 6),
    (5, 6)
]

# Створення графа
G = nx.Graph()
G.add_edges_from(edges)

# Впорядкований список вершин
nodes = sorted(G.nodes())
node_index = {node: i for i, node in enumerate(nodes)}

# ── Матриця суміжності вершин A(G) ─────────────────────

A = nx.to_numpy_array(
    G,
    nodelist=nodes,
    dtype=int
)

print("Матриця суміжності A(G):")
print(A)

# ── Матриця інцидентності B(G) ─────────────────────────

edge_list = edges

B = np.zeros(
    (len(nodes), len(edge_list)),
    dtype=int
)

for j, (u, v) in enumerate(edge_list):
    B[node_index[u], j] = 1
    B[node_index[v], j] = 1

print("\nМатриця інцидентності B(G):")
print(B)

# ── Матриця суміжності ребер Aₑ(G) ─────────────────────

Ae = B.T @ B
np.fill_diagonal(Ae, 0)

print("\nМатриця суміжності ребер Aₑ(G):")
print(Ae)