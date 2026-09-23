import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

# Вершинна та реберна зв'язність
kappa = nx.node_connectivity(G)
lambda_edge = nx.edge_connectivity(G)

# Один мінімальний вершинний розріз
vertex_cut = nx.minimum_node_cut(G)

# Один мінімальний реберний розріз
edge_cut = nx.minimum_edge_cut(G)

# Максимальна кліка
cliques = list(nx.find_cliques(G))
max_clique = max(cliques, key=len)
omega = len(max_clique)

# Фіксоване розташування графа
pos = nx.spring_layout(G, seed=42)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# -----------------------------
# 1. Числа зв'язності
# -----------------------------
ax1 = axes[0]

node_colors = [
    "tomato" if v in vertex_cut else "steelblue"
    for v in G.nodes()
]

edge_colors = []
edge_widths = []

for u, v in G.edges():
    if (u, v) in edge_cut or (v, u) in edge_cut:
        edge_colors.append("orange")
        edge_widths.append(3)
    else:
        edge_colors.append("gray")
        edge_widths.append(1.5)

nx.draw(
    G,
    pos,
    ax=ax1,
    with_labels=True,
    node_color=node_colors,
    edge_color=edge_colors,
    width=edge_widths,
    node_size=900,
    font_size=12
)

ax1.set_title(
    f"Вершинна зв'язність κ(G) = {kappa}\n"
    f"Реберна зв'язність λ(G) = {lambda_edge}"
)

vertex_patch = mpatches.Patch(
    color="tomato",
    label=f"Min вершинний розріз: {sorted(vertex_cut)}"
)

edge_patch = mpatches.Patch(
    color="orange",
    label=f"Min реберний розріз: {sorted(edge_cut)}"
)

normal_patch = mpatches.Patch(
    color="steelblue",
    label="Інші вершини"
)

ax1.legend(
    handles=[vertex_patch, edge_patch, normal_patch],
    loc="upper left"
)

# -----------------------------
# 2. Максимальна кліка
# -----------------------------
ax2 = axes[1]

clique_set = set(max_clique)

node_colors_clique = [
    "orange" if v in clique_set else "steelblue"
    for v in G.nodes()
]

edge_colors_clique = []

for u, v in G.edges():
    if u in clique_set and v in clique_set:
        edge_colors_clique.append("tomato")
    else:
        edge_colors_clique.append("lightgray")

nx.draw(
    G,
    pos,
    ax=ax2,
    with_labels=True,
    node_color=node_colors_clique,
    edge_color=edge_colors_clique,
    width=2,
    node_size=900,
    font_size=12
)

ax2.set_title(
    f"Максимальна кліка (колода): {sorted(max_clique)}, ω(G)={omega}"
)

clique_patch = mpatches.Patch(
    color="orange",
    label=f"Колода: {sorted(max_clique)}"
)

other_patch = mpatches.Patch(
    color="steelblue",
    label="Інші вершини"
)

ax2.legend(
    handles=[clique_patch, other_patch],
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    "figure_connectivity_clique.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()