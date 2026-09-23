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
deg_vec = [G.degree(v) for v in nodes]

# ── Вершинна та реберна зв'язність ────────────────────

kappa = nx.node_connectivity(G)
lambda_edge = nx.edge_connectivity(G)

min_vertex_cut = nx.minimum_node_cut(G)
min_edge_cut = nx.minimum_edge_cut(G)

print(f"Вершинна зв'язність κ(G) = {kappa}")
print(f"Мінімальний вершинний розріз: {min_vertex_cut}")

print(f"\nРеберна зв'язність λ(G) = {lambda_edge}")
print(f"Мінімальний реберний розріз: {min_edge_cut}")

print(
    f"\nПеревірка нерівності Уітні: "
    f"{kappa} ≤ {lambda_edge} ≤ {min(deg_vec)}"
)