import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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

# Створення графа
G = nx.Graph()
G.add_edges_from(edges)

# Впорядкований список вершин
nodes = sorted(G.nodes())
node_index = {node: i for i, node in enumerate(nodes)}

# Матриця суміжності вершин A(G)
A = nx.to_numpy_array(
    G,
    nodelist=nodes,
    dtype=int
)

print("Матриця суміжності A(G):")
print(A)

# Порядок ребер з умови завдання
edge_list = edges

# Матриця інцидентності B(G)
B = np.zeros((len(nodes), len(edge_list)), dtype=int)

for j, (u, v) in enumerate(edge_list):
    B[node_index[u], j] = 1
    B[node_index[v], j] = 1

print("\nМатриця інцидентності B(G):")
print(B)

# Матриця суміжності ребер Aₑ(G)
Ae = B.T @ B
np.fill_diagonal(Ae, 0)

print("\nМатриця суміжності ребер Aₑ(G):")
print(Ae)
# Вектор та множина степенів вершин
deg_vec = [G.degree(v) for v in nodes]
deg_set = sorted(set(deg_vec))

print("\nВектор степенів вершин:")
print(deg_vec)

print("\nМножина степенів:")
print(deg_set)

print(f"\nМінімальний степінь δ(G) = {min(deg_vec)}")
print(f"Максимальний степінь Δ(G) = {max(deg_vec)}")

print(
    f"\nПеревірка леми про рукостискання: "
    f"Σdeg = {sum(deg_vec)}, 2|E| = {2 * G.number_of_edges()}"
)
# Максимальна незалежна множина
complement = nx.complement(G)
cliques_complement = list(nx.find_cliques(complement))
max_independent_set = max(cliques_complement, key=len)

alpha = len(max_independent_set)

print("\nМаксимальна незалежна множина:")
print(sorted(max_independent_set))

print(f"Число незалежності α(G) = {alpha}")
# Радіус, діаметр, центр та периферія графа
ecc = nx.eccentricity(G)
radius = nx.radius(G)
diameter = nx.diameter(G)
center = nx.center(G)
periphery = nx.periphery(G)

print("\nЕксцентриситети вершин:")
print(ecc)

print(f"\nРадіус r(G) = {radius}")
print(f"Діаметр d(G) = {diameter}")
print(f"Центр графа = {center}")
print(f"Периферія графа = {periphery}")
# Мости та точки зчленування
bridges = list(nx.bridges(G))
articulation_points = list(nx.articulation_points(G))

print("\nМости:")
print(bridges if bridges else "Відсутні")

print("\nТочки зчленування:")
print(articulation_points if articulation_points else "Відсутні")
# Вершинна та реберна зв'язність
kappa = nx.node_connectivity(G)
lambda_edge = nx.edge_connectivity(G)

print(f"\nВершинна зв'язність κ(G) = {kappa}")
print(f"Реберна зв'язність λ(G) = {lambda_edge}")

print(
    f"Перевірка нерівності Уітні: "
    f"κ(G) ≤ λ(G) ≤ δ(G) → "
    f"{kappa} ≤ {lambda_edge} ≤ {min(deg_vec)}"
)
# Максимальна кліка
cliques = list(nx.find_cliques(G))
max_clique = max(cliques, key=len)

omega = len(max_clique)

print("\nМаксимальна кліка:")
print(sorted(max_clique))

print(f"Клікове число ω(G) = {omega}")
# Планарність графа
is_planar, _ = nx.check_planarity(G)

print("\nПланарність графа:")
print("Граф планарний" if is_planar else "Граф непланарний")

V = G.number_of_nodes()
E = G.number_of_edges()

print(
    f"Перевірка необхідної умови: "
    f"E ≤ 3V - 6 → {E} ≤ {3 * V - 6}"
)
# Хроматичне число та правильне розфарбування
coloring = nx.coloring.greedy_color(
    G,
    strategy="largest_first"
)

chi = max(coloring.values()) + 1

print("\nРозфарбування вершин:")
print(coloring)

print(f"Хроматичне число χ(G) = {chi}")
# Графічне зображення графа
nx.draw(
    G,
    with_labels=True,
    node_size=1000,
    font_size=12
)

plt.show()