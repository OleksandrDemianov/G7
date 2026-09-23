import networkx as nx

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

# ── Хроматичне число ───────────────────────────────────

coloring = nx.coloring.greedy_color(
    G,
    strategy="largest_first"
)

chromatic_number = max(coloring.values()) + 1

print("Розфарбування вершин:")
for vertex in sorted(coloring):
    print(
        f"Вершина {vertex} -> "
        f"колір {coloring[vertex] + 1}"
    )

print(f"\nХроматичне число χ(G) = {chromatic_number}")

# Перевірка правильності розфарбування
correct = all(
    coloring[u] != coloring[v]
    for u, v in G.edges()
)

print(f"Розфарбування правильне: {correct}")