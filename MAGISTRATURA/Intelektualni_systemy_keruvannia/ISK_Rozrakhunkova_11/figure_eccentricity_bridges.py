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

# Побудова графа
G = nx.Graph()
G.add_edges_from(edges)

nodes = sorted(G.nodes())

# Ексцентриситети
ecc = nx.eccentricity(G)
ecc_values = [ecc[v] for v in nodes]

radius = nx.radius(G)
diameter = nx.diameter(G)
center = nx.center(G)

# Мости та точки зчленування
bridges = list(nx.bridges(G))
articulation_points = list(nx.articulation_points(G))

# Полотно з двох частин
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---------------------------------
# 1. Діаграма ексцентриситетів
# ---------------------------------
ax1 = axes[0]

bar_colors = ["tomato" if v in center else "steelblue" for v in nodes]
bars = ax1.bar(nodes, ecc_values, color=bar_colors)

ax1.set_title(
    f"Ексцентриситети, r={radius}, d={diameter}, center={center}"
)
ax1.set_xlabel("Вершина")
ax1.set_ylabel("Ексцентриситет ε(v)")
ax1.set_xticks(nodes)
ax1.set_ylim(0, max(ecc_values) + 1)

for bar, value in zip(bars, ecc_values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        str(value),
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

center_patch = mpatches.Patch(color="tomato", label=f"Центр r={radius}")
diameter_patch = mpatches.Patch(color="steelblue", label=f"Діаметр d={diameter}")
ax1.legend(handles=[center_patch, diameter_patch])

# ---------------------------------
# 2. Граф: мости та точки зчленування
# ---------------------------------
ax2 = axes[1]

pos = nx.spring_layout(G, seed=42)

# Цвет вершин
node_colors = []
for v in nodes:
    if v in articulation_points:
        node_colors.append("tomato")
    else:
        node_colors.append("steelblue")

# Цвет рёбер
edge_colors = []
for e in G.edges():
    if e in bridges or (e[1], e[0]) in bridges:
        edge_colors.append("orange")
    else:
        edge_colors.append("black")

nx.draw(
    G,
    pos,
    ax=ax2,
    with_labels=True,
    node_color=node_colors,
    edge_color=edge_colors,
    node_size=900,
    font_size=12,
    width=2
)

ax2.set_title(
    f"Мости: {bridges if bridges else '[]'}\n"
    f"Точки зчленування: {articulation_points if articulation_points else '[]'}"
)

art_patch = mpatches.Patch(color="tomato", label="Точки зчленування")
bridge_patch = mpatches.Patch(color="orange", label="Мости")
normal_patch = mpatches.Patch(color="steelblue", label="Звичайні вершини")
ax2.legend(handles=[art_patch, bridge_patch, normal_patch], loc="upper left")

plt.tight_layout()
plt.savefig("figure_eccentricity_bridges.png", dpi=300, bbox_inches="tight")
plt.show()