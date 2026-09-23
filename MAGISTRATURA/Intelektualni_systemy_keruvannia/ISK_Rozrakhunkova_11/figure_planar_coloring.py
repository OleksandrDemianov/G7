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

# Двокольорове розфарбування
color_classes = {
    1: "tomato",
    3: "tomato",
    6: "tomato",
    2: "steelblue",
    4: "steelblue",
    5: "steelblue"
}

# Перевірка планарності
is_planar, embedding = nx.check_planarity(G)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---------------------------------
# 1. Розфарбування графа
# ---------------------------------
ax1 = axes[0]

pos1 = nx.spring_layout(G, seed=42)

node_colors = [color_classes[v] for v in G.nodes()]

nx.draw(
    G,
    pos1,
    ax=ax1,
    with_labels=True,
    node_color=node_colors,
    node_size=900,
    font_size=12,
    edge_color="black"
)

ax1.set_title("Розфарбування: χ(G) = 2 кольори")

c1_patch = mpatches.Patch(
    color="tomato",
    label="Колір 1: {1, 3, 6}"
)

c2_patch = mpatches.Patch(
    color="steelblue",
    label="Колір 2: {2, 4, 5}"
)

ax1.legend(
    handles=[c1_patch, c2_patch],
    loc="upper left"
)

# ---------------------------------
# 2. Планарне зображення
# ---------------------------------
ax2 = axes[1]

if is_planar:
    pos2 = nx.planar_layout(G)

    nx.draw(
        G,
        pos2,
        ax=ax2,
        with_labels=True,
        node_color="mediumseagreen",
        node_size=900,
        font_size=12,
        edge_color="black"
    )

    ax2.set_title("Граф планарний ✓ — планарне зображення")
else:
    ax2.set_title("Граф непланарний")

plt.tight_layout()

plt.savefig(
    "figure_planar_coloring.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()