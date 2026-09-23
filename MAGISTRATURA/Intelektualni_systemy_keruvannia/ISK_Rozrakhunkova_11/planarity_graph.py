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

# ── Перевірка планарності ──────────────────────────────

n = G.number_of_nodes()
m = G.number_of_edges()

is_planar, embedding = nx.check_planarity(G)

print(f"Кількість вершин n = {n}")
print(f"Кількість ребер m = {m}")

print(f"\nПеревірка умови m ≤ 3n - 6:")
print(f"{m} ≤ {3 * n - 6}")

print(f"\nГраф планарний: {is_planar}")

if is_planar:
    F = 2 - n + m
    print(f"Кількість граней F = {F}")