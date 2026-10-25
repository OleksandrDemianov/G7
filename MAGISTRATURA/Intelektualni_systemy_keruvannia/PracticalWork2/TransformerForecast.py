import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

time = np.arange(1000)

temperature = (
    20
    + 4 * np.sin(2 * np.pi * time / 24)
    + 0.002 * time
)

humidity = (
    14
    - 0.15 * (temperature - 20)
    + 0.5 * np.sin(2 * np.pi * time / 72)
)

level = (
    80
    - 0.02 * time
    + 2 * np.sin(2 * np.pi * time / 168)
)

# Нормалізований часовий індекс
time_feature = time / (len(time) - 1)

# Формування багатовимірного часового ряду
data = np.column_stack((
    temperature,
    humidity,
    level,
    time_feature
))

print("Розмірність масиву:", data.shape)
print("Перші 5 спостережень:")
print(data[:5])

fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

axes[0].plot(time, temperature)
axes[0].set_ylabel("Температура, °C")
axes[0].set_title("Температура зерна")
axes[0].grid(True)

axes[1].plot(time, humidity)
axes[1].set_ylabel("Вологість, %")
axes[1].set_title("Вологість зерна")
axes[1].grid(True)

axes[2].plot(time, level)
axes[2].set_xlabel("Час, год")
axes[2].set_ylabel("Заповнення, %")
axes[2].set_title("Рівень заповнення зерносховища")
axes[2].grid(True)

plt.tight_layout()
plt.show()

from sklearn.preprocessing import StandardScaler

# Формування вхідних послідовностей
sequence_length = 168

X = []
y = []

for i in range(len(data) - sequence_length):
    X.append(data[i:i + sequence_length])
    y.append(data[i + sequence_length, :3])

X = np.array(X)
y = np.array(y)

print("Форма вхідних даних X:", X.shape)
print("Форма вихідних даних y:", y.shape)

# Хронологічний розподіл вибірки
train_size = int(len(X) * 0.8)

X_train = X[:train_size]
X_test = X[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]

# Окремі нормалізатори для входів і виходів
scaler_X = StandardScaler()
scaler_y = StandardScaler()

scaler_X.fit(X_train.reshape(-1, 4))
scaler_y.fit(y_train)

X_train = scaler_X.transform(
    X_train.reshape(-1, 4)
).reshape(X_train.shape)

X_test = scaler_X.transform(
    X_test.reshape(-1, 4)
).reshape(X_test.shape)

y_train = scaler_y.transform(y_train)
y_test = scaler_y.transform(y_test)

print("Навчальні дані X:", X_train.shape)
print("Тестові дані X:", X_test.shape)
print("Навчальні дані y:", y_train.shape)
print("Тестові дані y:", y_test.shape)

# Модель Transformer для прогнозування часового ряду
class TransformerForecast(nn.Module):
    def __init__(self, input_size=4, d_model=32, nhead=4):
        super().__init__()

        # Проєкція чотирьох вхідних ознак
        self.input_layer = nn.Linear(input_size, d_model)

        # Позиційне кодування часових кроків
        positions = torch.arange(168).unsqueeze(1)
        dimensions = torch.arange(0, d_model, 2)

        angles = positions / (
            10000 ** (dimensions / d_model)
        )

        pe = torch.zeros(168, d_model)
        pe[:, 0::2] = torch.sin(angles)
        pe[:, 1::2] = torch.cos(angles)

        self.register_buffer("positional_encoding", pe)

        # Шар Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=64,
            dropout=0.1,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=2
        )

        # Прогнозування трьох параметрів
        self.output_layer = nn.Linear(d_model, 3)

    def forward(self, x):
        x = self.input_layer(x)
        x = x + self.positional_encoding[:x.size(1)]

        x = self.transformer(x)

        return self.output_layer(x[:, -1, :])

    # Створення моделі Transformer
torch.manual_seed(42)

model = TransformerForecast()

# Перевірка моделі на одному прикладі
sample = torch.tensor(
    X_train[:1],
    dtype=torch.float32
)

model.eval()

with torch.no_grad():
    prediction = model(sample)

print("Розмірність входу моделі:", sample.shape)
print("Розмірність виходу моделі:", prediction.shape)
print("Прогноз до навчання:", prediction.numpy())

# Підготовка даних для навчання
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

# Функція втрат та алгоритм оптимізації
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Навчання Transformer-моделі
epochs = 50

model.train()

for epoch in range(epochs):
    optimizer.zero_grad()

    predictions = model(X_train_tensor)
    loss = criterion(predictions, y_train_tensor)

    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(
            f"Епоха {epoch + 1}/{epochs}, "
            f"помилка MSE: {loss.item():.6f}"
        )

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Перевірка Transformer-моделі на тестових даних
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)

model.eval()

with torch.no_grad():
    test_predictions = model(X_test_tensor).cpu().numpy()

# Повернення до початкових одиниць вимірювання
y_test_original = scaler_y.inverse_transform(y_test)
predictions_original = scaler_y.inverse_transform(test_predictions)

# Оцінювання точності прогнозування
parameter_names = [
    "Температура зерна",
    "Вологість зерна",
    "Рівень заповнення"
]

for i, name in enumerate(parameter_names):
    mse = mean_squared_error(
        y_test_original[:, i],
        predictions_original[:, i]
    )
    mae = mean_absolute_error(
        y_test_original[:, i],
        predictions_original[:, i]
    )
    r2 = r2_score(
        y_test_original[:, i],
        predictions_original[:, i]
    )

    print(f"\n{name}:")
    print(f"  MSE: {mse:.6f}")
    print(f"  MAE: {mae:.6f}")
    print(f"  R²:  {r2:.6f}")

# Порівняння прогнозованих і фактичних значень
fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

test_time = np.arange(len(y_test_original))

units = ["°C", "%", "%"]

for i, name in enumerate(parameter_names):
    axes[i].plot(
        test_time,
        y_test_original[:, i],
        label="Фактичне значення"
    )

    axes[i].plot(
        test_time,
        predictions_original[:, i],
        label="Прогноз Transformer",
        linestyle="--"
    )

    axes[i].set_title(name)
    axes[i].set_ylabel(units[i])
    axes[i].grid(True)
    axes[i].legend()

axes[2].set_xlabel("Крок тестової вибірки")

plt.tight_layout()
plt.show()
