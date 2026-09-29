import numpy as np
import matplotlib.pyplot as plt

# Трапецеїдальна функція належності
def trapezoidal(x, a, b, c, d):
    return np.maximum(
        0,
        np.minimum(
            np.minimum((x - a) / (b - a + 1e-9), 1),
            (d - x) / (d - c + 1e-9)
        )
    )

# Операції над нечіткими множинами
def fuzzy_intersection(mu_A, mu_B):
    return np.minimum(mu_A, mu_B)

def fuzzy_union(mu_A, mu_B):
    return np.maximum(mu_A, mu_B)

def fuzzy_complement(mu_A):
    return 1 - mu_A

# Діапазон вологості ґрунту
x = np.linspace(0, 100, 500)

# Функції належності
mu_dry = trapezoidal(x, 0, 0, 20, 40)
mu_moist = trapezoidal(x, 25, 40, 60, 75)
mu_wet = trapezoidal(x, 60, 75, 100, 100)

# Графік функцій належності
plt.figure()

plt.plot(x, mu_dry, label="Сухо")
plt.plot(x, mu_moist, label="Вологувато")
plt.plot(x, mu_wet, label="Мокро")

plt.xlabel("Вологість ґрунту, %")
plt.ylabel("Ступінь належності")
plt.title("Функції належності вологості ґрунту")
plt.legend()
plt.grid()

plt.show()

# Операції для множин "Сухо" та "Вологувато"
intersection = fuzzy_intersection(mu_dry, mu_moist)
union = fuzzy_union(mu_dry, mu_moist)
complement = fuzzy_complement(mu_dry)

# Перетин
plt.figure()

plt.plot(x, mu_dry, label="Сухо")
plt.plot(x, mu_moist, label="Вологувато")
plt.plot(x, intersection, label="Перетин")

plt.xlabel("Вологість ґрунту, %")
plt.ylabel("Ступінь належності")
plt.title("Перетин нечітких множин")
plt.legend()
plt.grid()

plt.show()

# Об'єднання
plt.figure()

plt.plot(x, mu_dry, label="Сухо")
plt.plot(x, mu_moist, label="Вологувато")
plt.plot(x, union, label="Об'єднання")

plt.xlabel("Вологість ґрунту, %")
plt.ylabel("Ступінь належності")
plt.title("Об'єднання нечітких множин")
plt.legend()
plt.grid()

plt.show()

# Доповнення
plt.figure()

plt.plot(x, mu_dry, label="Сухо")
plt.plot(x, complement, label="Доповнення множини Сухо")

plt.xlabel("Вологість ґрунту, %")
plt.ylabel("Ступінь належності")
plt.title("Доповнення нечіткої множини")
plt.legend()
plt.grid()

plt.show()

# α-зрізи та дефаззифікація
def alpha_cut(x, mu_A, alpha):
    return x[mu_A >= alpha]

def centroid_defuzz(x, mu):
    return np.sum(x * mu) / np.sum(mu)

# α-зрізи для множини "Вологувато"
alpha_values = [0.3, 0.6, 0.9]

for alpha in alpha_values:
    cut = alpha_cut(x, mu_moist, alpha)

    plt.figure()
    plt.plot(x, mu_moist, label="Вологувато")
    plt.axhline(alpha, linestyle="--", label=f"α = {alpha}")

    if len(cut) > 0:
        plt.fill_between(
            x,
            0,
            mu_moist,
            where=(mu_moist >= alpha),
            alpha=0.3
        )

    plt.xlabel("Вологість ґрунту, %")
    plt.ylabel("Ступінь належності")
    plt.title(f"α-зріз нечіткої множини «Вологувато», α = {alpha}")
    plt.legend()
    plt.grid()

    plt.show()

# Дефаззифікація методом центроїда
centroid = centroid_defuzz(x, mu_moist)

print("Результат дефаззифікації:")
print("Центроїд =", round(centroid, 2), "%")

# Нечітка система Мамдані для керування поливом

# Вихідна змінна — інтенсивність поливу, %
x_watering = np.linspace(0, 100, 500)

# Функції належності для поливу
mu_low = trapezoidal(x_watering, 0, 0, 20, 40)
mu_medium = trapezoidal(x_watering, 25, 40, 60, 75)
mu_high = trapezoidal(x_watering, 60, 75, 100, 100)

# Вхідне значення вологості ґрунту
soil_input = 30

# Фаззифікація вхідного значення
w_dry = np.interp(soil_input, x, mu_dry)
w_moist = np.interp(soil_input, x, mu_moist)
w_wet = np.interp(soil_input, x, mu_wet)

print()
print("Нечітка система Мамдані")
print("Вологість ґрунту =", soil_input, "%")
print("Сухо =", round(w_dry, 3))
print("Вологувато =", round(w_moist, 3))
print("Мокро =", round(w_wet, 3))

# Активація правил Мамдані
rule_dry = np.minimum(w_dry, mu_high)
rule_moist = np.minimum(w_moist, mu_medium)
rule_wet = np.minimum(w_wet, mu_low)

# Агрегація результатів
aggregated = np.maximum(
    rule_dry,
    np.maximum(rule_moist, rule_wet)
)

# Дефаззифікація методом центроїда
watering_result = centroid_defuzz(x_watering, aggregated)

print("Інтенсивність поливу =", round(watering_result, 2), "%")

# Графік результату нечіткого виводу
plt.figure()

plt.plot(x_watering, mu_low, label="Низький")
plt.plot(x_watering, mu_medium, label="Середній")
plt.plot(x_watering, mu_high, label="Високий")

plt.fill_between(
    x_watering,
    0,
    aggregated,
    alpha=0.3,
    label="Агрегований результат"
)

plt.axvline(
    watering_result,
    linestyle="--",
    label=f"Результат = {watering_result:.2f}%"
)

plt.xlabel("Інтенсивність поливу, %")
plt.ylabel("Ступінь належності")
plt.title("Нечіткий висновок системи Мамдані")
plt.legend()
plt.grid()

plt.show()