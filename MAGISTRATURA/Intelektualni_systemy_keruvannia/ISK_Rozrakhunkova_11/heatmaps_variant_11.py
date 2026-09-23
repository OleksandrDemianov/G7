import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Варіант 11
edges = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 1),
    (1, 5),
    (2, 6),
    (5, 6)
]

# Побудова графа
G = nx.Graph()
G.add_edges_from(edges)

# Вершини та ребра
nodes = sorted(G.nodes())
edge_list = edges
edge_names = [f"e{i}" for i in range(1, len(edge_list) + 1)]

# Матриця суміжності вершин A(G)
A = nx.to_numpy_array(G, nodelist=nodes, dtype=int)

# Матриця інцидентності B(G)
B = np.zeros((len(nodes), len(edge_list)), dtype=int)
node_index = {node: i for i, node in enumerate(nodes)}

for j, (u, v) in enumerate(edge_list):
    B[node_index[u], j] = 1
    B[node_index[v], j] = 1

# Створення теплових карт
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---- A(G)
ax = axes[0]
ax.imshow(A, cmap="Blues", vmin=0, vmax=1)
ax.set_title("Матриця суміжності вершин A(G)")
ax.set_xlabel("Вершини")
ax.set_ylabel("Вершини")
ax.set_xticks(range(len(nodes)))
ax.set_yticks(range(len(nodes)))
ax.set_xticklabels(nodes)
ax.set_yticklabels(nodes)

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        ax.text(j, i, str(A[i, j]), ha="center", va="center", color="black")

# ---- B(G)
ax = axes[1]
ax.imshow(B, cmap="Oranges", vmin=0, vmax=1)
ax.set_title("Матриця інцидентності B(G)")
ax.set_xlabel("Ребра")
ax.set_ylabel("Вершини")
ax.set_xticks(range(len(edge_names)))
ax.set_yticks(range(len(nodes)))
ax.set_xticklabels(edge_names)
ax.set_yticklabels(nodes)

for i in range(B.shape[0]):
    for j in range(B.shape[1]):
        ax.text(j, i, str(B[i, j]), ha="center", va="center", color="black")

plt.tight_layout()
plt.savefig("heatmaps_AB_variant_11.png", dpi=300, bbox_inches="tight")
plt.show()