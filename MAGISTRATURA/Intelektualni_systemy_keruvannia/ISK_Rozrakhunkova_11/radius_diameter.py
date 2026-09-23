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

# ── Радіус, діаметр, центр та периферія ────────────────

ecc = nx.eccentricity(G)
radius = nx.radius(G)
diameter = nx.diameter(G)
center = nx.center(G)
periphery = nx.periphery(G)

print("Ексцентриситети вершин:")
print(ecc)

print(f"\nРадіус r(G) = {radius}")
print(f"Діаметр d(G) = {diameter}")
print(f"Центр графа = {center}")
print(f"Периферія графа = {periphery}")