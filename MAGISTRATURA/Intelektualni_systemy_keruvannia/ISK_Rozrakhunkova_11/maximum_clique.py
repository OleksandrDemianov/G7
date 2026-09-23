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

# ── Колода (максимальна кліка) ─────────────────────────

cliques = list(nx.find_cliques(G))

max_clique = max(
    cliques,
    key=len
)

omega = len(max_clique)

print("Максимальна кліка:")
print(sorted(max_clique))

print(f"Клікове число ω(G) = {omega}")