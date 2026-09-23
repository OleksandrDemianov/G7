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

# ── Максимальна незалежна множина ───────────────────────

complement = nx.complement(G)

cliques_complement = list(nx.find_cliques(complement))

max_independent_set = max(
    cliques_complement,
    key=len
)

alpha = len(max_independent_set)

print("Максимальна незалежна множина:")
print(sorted(max_independent_set))

print(f"Число незалежності α(G) = {alpha}")