
import numpy as np
import matplotlib.pyplot as plt

# Параметры динамического объекта
ambient_temperature = 20.0
heating_coefficient = 0.08
cooling_coefficient = 0.02

# Модель изменения температуры
def plant_model(temperature, control):
    return (
        temperature
        + heating_coefficient * control
        - cooling_coefficient * (temperature - ambient_temperature)
    )

# Начальные условия
temperature = 20.0
control = 5.0
temperatures = [temperature]

# Моделирование объекта
for step in range(100):
    temperature = plant_model(temperature, control)
    temperatures.append(temperature)

# Построение графика
plt.plot(temperatures, label="Object temperature")
plt.xlabel("Time step")
plt.ylabel("Temperature, °C")
plt.title("Dynamic object response")
plt.legend()
plt.grid(True)
plt.show()


# Формування навчальних даних для нейронної мережі
np.random.seed(42)

X = []
y = []

temperature = 20.0

for step in range(2000):
    control = np.random.uniform(0, 10)

    next_temperature = plant_model(temperature, control)

    X.append([temperature, control])
    y.append(next_temperature)

    temperature = next_temperature

X = np.array(X)
y = np.array(y)

print("Training data generated")
print("Number of samples:", len(X))
print("Input shape:", X.shape)
print("Output shape:", y.shape)
print("First sample:", X[0], "->", y[0])


# Навчання нейронної мережі
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Розділення даних
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Нормалізація вхідних даних
scaler_X = StandardScaler()
X_train_scaled = scaler_X.fit_transform(X_train)
X_test_scaled = scaler_X.transform(X_test)

# Нормалізація вихідних даних
scaler_y = StandardScaler()
y_train_scaled = scaler_y.fit_transform(
    y_train.reshape(-1, 1)
).ravel()

# Створення нейронної мережі
model = MLPRegressor(
    hidden_layer_sizes=(16, 8),
    activation="relu",
    solver="adam",
    max_iter=2000,
    random_state=42
)

# Навчання
model.fit(X_train_scaled, y_train_scaled)

# Прогнозування на тестових даних
y_pred_scaled = model.predict(X_test_scaled)
y_pred = scaler_y.inverse_transform(
    y_pred_scaled.reshape(-1, 1)
).ravel()

# Оцінювання точності
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nNeural network training completed")
print("Architecture: 2-16-8-1")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("MSE:", round(mse, 6))
print("R2:", round(r2, 6))

# Графік порівняння
plt.figure(figsize=(9, 5))
plt.plot(y_test[:100], label="Real temperature")
plt.plot(y_pred[:100], "--", label="Neural network prediction")
plt.xlabel("Test sample")
plt.ylabel("Temperature, °C")
plt.title("Neural network prediction accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Нейронне передбачувальне керування (Neural MPC)
from scipy.optimize import minimize

# Параметри регулятора
target_temperature = 35.0
prediction_horizon = 10
control_min = 0.0
control_max = 10.0
control_penalty = 0.01

# Однокроковий прогноз нейронної мережі
def neural_predict(temperature, control):
    inputs = np.array([[temperature, control]])
    inputs_scaled = scaler_X.transform(inputs)

    prediction_scaled = model.predict(inputs_scaled)

    prediction = scaler_y.inverse_transform(
        prediction_scaled.reshape(-1, 1)
    )

    return float(prediction[0, 0])


# Функція вартості MPC
def mpc_cost(control_sequence, current_temperature):
    predicted_temperature = current_temperature
    total_cost = 0.0

    for control in control_sequence:
        predicted_temperature = neural_predict(
            predicted_temperature, control
        )

        error = target_temperature - predicted_temperature

        total_cost += error ** 2 + control_penalty * control ** 2

    return total_cost


# Моделювання замкненої системи керування
temperature = 20.0
mpc_temperatures = [temperature]
mpc_controls = []

initial_guess = np.full(prediction_horizon, 5.0)

for step in range(100):
    result = minimize(
        mpc_cost,
        initial_guess,
        args=(temperature,),
        method="SLSQP",
        bounds=[(control_min, control_max)] * prediction_horizon,
        options={"maxiter": 100, "ftol": 1e-5}
    )

    if not result.success:
        print("Optimization warning at step:", step)
        print(result.message)

    control = float(np.clip(result.x[0], control_min, control_max))

    # Реальний об'єкт керування
    temperature = plant_model(temperature, control)

    mpc_temperatures.append(temperature)
    mpc_controls.append(control)

    # Зсув прогнозованої послідовності
    initial_guess = np.concatenate(
        [result.x[1:], result.x[-1:]]
    )

# Результати керування
print("\nNeural MPC simulation completed")
print("Target temperature:", target_temperature)
print("Final temperature:", round(temperature, 4))
print("Final error:", round(target_temperature - temperature, 4))
print("Minimum control:", round(min(mpc_controls), 4))
print("Maximum control:", round(max(mpc_controls), 4))

# Графік температури
plt.figure(figsize=(9, 5))
plt.plot(mpc_temperatures, label="Actual temperature")
plt.axhline(
    target_temperature,
    color="red",
    linestyle="--",
    label="Target temperature"
)
plt.xlabel("Time step")
plt.ylabel("Temperature, °C")
plt.title("Neural MPC temperature control")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Графік керуючого впливу
plt.figure(figsize=(9, 5))
plt.step(
    range(len(mpc_controls)),
    mpc_controls,
    where="post",
    label="MPC control signal"
)
plt.xlabel("Time step")
plt.ylabel("Control signal")
plt.title("Neural MPC control action")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
