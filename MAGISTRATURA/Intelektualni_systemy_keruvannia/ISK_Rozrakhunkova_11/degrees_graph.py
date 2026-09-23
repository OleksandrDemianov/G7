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

nodes = sorted(G.nodes())

# ── Вектор та множина степенів ──────────────────────────

deg_vec = [G.degree(v) for v in nodes]
deg_set = sorted(set(deg_vec))

print("Вектор степенів вершин:")
print(deg_vec)

print("\nМножина степенів:")
print(deg_set)

print(f"\nМінімальний степінь δ(G) = {min(deg_vec)}")
print(f"Максимальний степінь Δ(G) = {max(deg_vec)}")

print(
    f"\nПеревірка леми про рукостискання: "
    f"Σdeg = {sum(deg_vec)}, "
    f"2|E| = {2 * G.number_of_edges()}"
)