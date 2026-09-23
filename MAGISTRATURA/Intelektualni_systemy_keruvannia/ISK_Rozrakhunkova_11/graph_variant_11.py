import networkx as nx
import matplotlib.pyplot as plt

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

G = nx.Graph()
G.add_edges_from(edges)

pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1000,
    font_size=12
)

plt.savefig(
    "graph_variant_11.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()