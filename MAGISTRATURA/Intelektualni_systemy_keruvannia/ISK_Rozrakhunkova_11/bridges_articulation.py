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

# ── Мости та точки зчленування ─────────────────────────

bridges = list(nx.bridges(G))
articulation_points = list(nx.articulation_points(G))

print("Мости:")
print(bridges if bridges else "Відсутні")

print("\nТочки зчленування:")
print(articulation_points if articulation_points else "Відсутні")