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

nodes = sorted(G.nodes())
degrees = [G.degree(v) for v in nodes]

# Максимальна незалежна множина
independent_set = {2, 4, 5}
alpha = len(independent_set)

# Створюємо полотно з двох частин
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---------------------------------
# 1. Стовпчикова діаграма степенів
# ---------------------------------
ax1 = axes[0]
colors_bar = ["tomato" if v in [1, 2] else "steelblue" for v in nodes]

bars = ax1.bar(nodes, degrees, color=colors_bar)
ax1.set_title("Вектор степенів вершин")
ax1.set_xlabel("Вершина")
ax1.set_ylabel("Степінь deg(v)")
ax1.set_xticks(nodes)
ax1.set_ylim(0, max(degrees) + 1)

avg_deg = sum(degrees) / len(degrees)
ax1.axhline(avg_deg, linestyle="--", color="green", label=f"Середній deg={avg_deg:.1f}")
ax1.legend()

for bar, deg in zip(bars, degrees):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        str(deg),
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold"
    )

# ---------------------------------
# 2. Граф з незалежною множиною
# ---------------------------------
ax2 = axes[1]

pos = nx.spring_layout(G, seed=42)

node_colors = ["tomato" if v in independent_set else "steelblue" for v in nodes]

nx.draw(
    G,
    pos,
    ax=ax2,
    with_labels=True,
    node_color=node_colors,
    node_size=900,
    font_size=12
)

ax2.set_title(f"Максимальна незалежна множина: {tuple(sorted(independent_set))}, α(G)={alpha}")

# Легенда
import matplotlib.patches as mpatches
red_patch = mpatches.Patch(color="tomato", label="Незалежна множина")
blue_patch = mpatches.Patch(color="steelblue", label="Інші вершини")
ax2.legend(handles=[red_patch, blue_patch], loc="upper left")

plt.tight_layout()
plt.savefig("figure_degrees_independent.png", dpi=300, bbox_inches="tight")
plt.show()