import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

# Фіксація випадкових значень для відтворюваності
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

# Середовище навчання GridWorld 6×6
class GridWorld:
    def __init__(self, size=6):
        self.size = size
        self.start = (0, 0)
        self.goal = (5, 5)
        self.walls = {(1, 1), (3, 1)}

        self.n_states = size * size
        self.n_actions = 4

        self.reset()

    def reset(self):
        # Повернення агента до початкового стану
        self.position = self.start
        return self.get_state()

    def get_state(self):
        # Перетворення координат на номер стану
        row, col = self.position
        return row * self.size + col

    def step(self, action):
        # Дії: вгору, вниз, вліво, вправо
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        dr, dc = directions[action]
        row, col = self.position

        new_row = max(0, min(self.size - 1, row + dr))
        new_col = max(0, min(self.size - 1, col + dc))

        # Перешкоди блокують переміщення
        if (new_row, new_col) not in self.walls:
            self.position = (new_row, new_col)

        done = self.position == self.goal

        # Винагорода за досягнення цілі та штраф за крок
        reward = 10.0 if done else -0.1

        return self.get_state(), reward, done

# Перевірка роботи середовища GridWorld
env = GridWorld()

state = env.reset()

print("Кількість станів:", env.n_states)
print("Кількість дій:", env.n_actions)
print("Початковий стан:", state)

# Перевірка переміщення агента вправо
next_state, reward, done = env.step(3)

print("Стан після переміщення:", next_state)
print("Винагорода:", reward)
print("Досягнуто цілі:", done)

# Нейронна мережа для оцінювання Q-значень
class QNetwork(nn.Module):
    def __init__(self, n_states=36, n_actions=4):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(n_states, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, n_actions)
        )

    def forward(self, x):
        return self.network(x)


# Перетворення номера стану на вхідний вектор
def encode_state(state, n_states=36):
    state_vector = np.zeros(n_states, dtype=np.float32)
    state_vector[state] = 1.0
    return torch.tensor(state_vector)


# Перевірка роботи нейронної мережі
q_network = QNetwork()

state_vector = encode_state(0)

with torch.no_grad():
    q_values = q_network(state_vector)

print("Розмірність вхідного вектора:", state_vector.shape)
print("Розмірність вихідного вектора:", q_values.shape)
print("Початкові Q-значення:", q_values.numpy())

# Агент для алгоритмів DQN та Double DQN
class DQNAgent:
    def __init__(self, n_states=36, n_actions=4,
                 double_dqn=False):
        self.n_states = n_states
        self.n_actions = n_actions
        self.double_dqn = double_dqn

        # Параметри навчання
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 32

        # Основна та цільова нейронні мережі
        self.policy_net = QNetwork(n_states, n_actions)
        self.target_net = QNetwork(n_states, n_actions)

        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )
        self.target_net.eval()

        # Оптимізатор та функція втрат
        self.optimizer = optim.Adam(
            self.policy_net.parameters(),
            lr=0.001
        )
        self.criterion = nn.MSELoss()

        # Буфер збереження досвіду
        self.memory = deque(maxlen=10000)

    def select_action(self, state):
        # Стратегія вибору дії epsilon-greedy
        if random.random() < self.epsilon:
            return random.randrange(self.n_actions)

        with torch.no_grad():
            state_tensor = encode_state(
                state, self.n_states
            ).unsqueeze(0)

            q_values = self.policy_net(state_tensor)

            return int(torch.argmax(q_values, dim=1).item())

    def remember(self, state, action, reward,
                 next_state, done):
        # Збереження переходу до буфера
        self.memory.append(
            (state, action, reward, next_state, done)
        )

    def update_target_network(self):
        # Синхронізація цільової мережі
        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )

    def decay_epsilon(self):
        # Поступове зменшення дослідження
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return None

        # Випадкова вибірка переходів
        batch = random.sample(
            self.memory, self.batch_size
        )

        states, actions, rewards, next_states, dones = zip(*batch)

        states_tensor = torch.stack([
            encode_state(s, self.n_states) for s in states
        ])
        next_states_tensor = torch.stack([
            encode_state(s, self.n_states) for s in next_states
        ])

        actions_tensor = torch.tensor(
            actions, dtype=torch.long
        ).unsqueeze(1)

        rewards_tensor = torch.tensor(
            rewards, dtype=torch.float32
        )

        dones_tensor = torch.tensor(
            dones, dtype=torch.float32
        )

        # Поточні Q-значення обраних дій
        current_q = self.policy_net(
            states_tensor
        ).gather(1, actions_tensor).squeeze(1)

        with torch.no_grad():
            if self.double_dqn:
                # Double DQN: вибір дії основною мережею
                next_actions = self.policy_net(
                    next_states_tensor
                ).argmax(dim=1, keepdim=True)

                # Оцінювання дії цільовою мережею
                next_q = self.target_net(
                    next_states_tensor
                ).gather(1, next_actions).squeeze(1)
            else:
                # DQN: максимальна оцінка цільової мережі
                next_q = self.target_net(
                    next_states_tensor
                ).max(dim=1).values

            target_q = rewards_tensor + (
                self.gamma * next_q * (1 - dones_tensor)
            )

        # Оновлення основної мережі
        loss = self.criterion(current_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

# Створення агентів DQN та Double DQN
dqn_agent = DQNAgent(
    n_states=36,
    n_actions=4,
    double_dqn=False
)

double_dqn_agent = DQNAgent(
    n_states=36,
    n_actions=4,
    double_dqn=True
)

# Перевірка параметрів агентів
print("\nПеревірка ініціалізації агентів:")
print("Алгоритм DQN:", dqn_agent.double_dqn)
print("Алгоритм Double DQN:", double_dqn_agent.double_dqn)

print("Кількість дій DQN:", dqn_agent.n_actions)
print("Кількість дій Double DQN:", double_dqn_agent.n_actions)

print(
    "Кількість параметрів нейронної мережі:",
    sum(p.numel() for p in dqn_agent.policy_net.parameters())
)

# Навчання агента у середовищі GridWorld
def train_agent(agent, episodes=500, max_steps=100):
    rewards_history = []
    success_history = []
    losses_history = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0.0
        losses = []
        done = False

        for step in range(max_steps):
            action = agent.select_action(state)

            next_state, reward, done = env.step(action)

            agent.remember(
                state, action, reward, next_state, done
            )

            loss = agent.train_step()

            if loss is not None:
                losses.append(loss)

            total_reward += reward
            state = next_state

            if done:
                break

        agent.decay_epsilon()

        # Оновлення цільової мережі кожні 10 епізодів
        if (episode + 1) % 10 == 0:
            agent.update_target_network()

        rewards_history.append(total_reward)
        success_history.append(int(done))

        losses_history.append(
            np.mean(losses) if losses else 0.0
        )

        if (episode + 1) % 100 == 0:
            success_rate = np.mean(success_history[-100:])

            print(
                f"Епізод {episode + 1}/{episodes}, "
                f"винагорода: {total_reward:.2f}, "
                f"успішність: {success_rate:.2%}"
            )

    return rewards_history, success_history, losses_history

# Забезпечення однакових початкових ваг нейронних мереж
double_dqn_agent.policy_net.load_state_dict(
    dqn_agent.policy_net.state_dict()
)

double_dqn_agent.update_target_network()

# Навчання класичного DQN
print("\nНавчання класичного DQN")

np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

dqn_rewards, dqn_success, dqn_losses = train_agent(
    dqn_agent,
    episodes=500,
    max_steps=100
)

# Навчання Double DQN
print("\nНавчання Double DQN")

np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

double_rewards, double_success, double_losses = train_agent(
    double_dqn_agent,
    episodes=500,
    max_steps=100
)

# Підсумкові результати навчання
print("\nПідсумкові результати за останні 100 епізодів:")

print(
    f"DQN — середня винагорода: "
    f"{np.mean(dqn_rewards[-100:]):.3f}, "
    f"успішність: {np.mean(dqn_success[-100:]):.1%}"
)

print(
    f"Double DQN — середня винагорода: "
    f"{np.mean(double_rewards[-100:]):.3f}, "
    f"успішність: {np.mean(double_success[-100:]):.1%}"
)

# Обчислення еталонних Q-значень методом ітерації значень
def calculate_reference_q(env, gamma=0.95, tolerance=1e-10):
    n_states = env.n_states
    n_actions = env.n_actions

    values = np.zeros(n_states)

    # Таблиця переходів середовища
    transitions = []

    for state in range(n_states):
        row = state // env.size
        col = state % env.size

        state_transitions = []

        for action in range(n_actions):
            env.position = (row, col)

            next_state, reward, done = env.step(action)

            state_transitions.append(
                (next_state, reward, done)
            )

        transitions.append(state_transitions)

    # Ітераційний розрахунок оптимальної цінності станів
    for iteration in range(10000):
        new_values = np.zeros(n_states)

        for state in range(n_states):
            action_values = []

            for next_state, reward, done in transitions[state]:
                q = reward

                if not done:
                    q += gamma * values[next_state]

                action_values.append(q)

            new_values[state] = max(action_values)

        difference = np.max(np.abs(new_values - values))
        values = new_values

        if difference < tolerance:
            break

    # Еталонні Q-значення для кожної дії
    reference_q = np.zeros((n_states, n_actions))

    for state in range(n_states):
        for action in range(n_actions):
            next_state, reward, done = transitions[state][action]

            reference_q[state, action] = reward

            if not done:
                reference_q[state, action] += (
                    gamma * values[next_state]
                )

    env.reset()

    return reference_q


reference_q = calculate_reference_q(env)

print("\nПеревірка еталонних Q-значень:")
print("Розмірність Q-таблиці:", reference_q.shape)
print("Q-значення початкового стану:")
print(reference_q[0])

# Порівняння оцінок Q-значень з еталоном
all_states = torch.eye(env.n_states, dtype=torch.float32)

dqn_agent.policy_net.eval()
double_dqn_agent.policy_net.eval()

with torch.no_grad():
    dqn_q = dqn_agent.policy_net(all_states).numpy()
    double_q = double_dqn_agent.policy_net(all_states).numpy()

# Виключення клітинок перешкод і цільового стану
valid_states = [
    s for s in range(env.n_states)
    if (s // env.size, s % env.size)
    not in env.walls | {env.goal}
]

# Похибка оцінювання Q-значень
dqn_error = dqn_q[valid_states] - reference_q[valid_states]
double_error = double_q[valid_states] - reference_q[valid_states]

# Додатна частина похибки відповідає завищенню
dqn_overestimation = np.maximum(dqn_error, 0)
double_overestimation = np.maximum(double_error, 0)

print("\nПорівняння завищення Q-значень:")

print(
    f"DQN — середнє завищення: "
    f"{np.mean(dqn_overestimation):.6f}"
)

print(
    f"Double DQN — середнє завищення: "
    f"{np.mean(double_overestimation):.6f}"
)

print(
    f"DQN — середня абсолютна похибка: "
    f"{np.mean(np.abs(dqn_error)):.6f}"
)

print(
    f"Double DQN — середня абсолютна похибка: "
    f"{np.mean(np.abs(double_error)):.6f}"
)

# Порівняння результатів навчання DQN та Double DQN
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# Ковзне середнє винагороди
window = 20

dqn_avg = np.convolve(
    dqn_rewards, np.ones(window) / window, mode="valid"
)

double_avg = np.convolve(
    double_rewards, np.ones(window) / window, mode="valid"
)

episodes_axis = np.arange(window, len(dqn_rewards) + 1)

axes[0, 0].plot(episodes_axis, dqn_avg, label="DQN")
axes[0, 0].plot(episodes_axis, double_avg, label="Double DQN")
axes[0, 0].set_title("Середня винагорода за 20 епізодів")
axes[0, 0].set_xlabel("Епізод")
axes[0, 0].set_ylabel("Винагорода")
axes[0, 0].legend()
axes[0, 0].grid(True)

# Ковзна успішність
dqn_rate = np.convolve(
    dqn_success, np.ones(window) / window, mode="valid"
)

double_rate = np.convolve(
    double_success, np.ones(window) / window, mode="valid"
)

axes[0, 1].plot(episodes_axis, dqn_rate, label="DQN")
axes[0, 1].plot(episodes_axis, double_rate, label="Double DQN")
axes[0, 1].set_title("Успішність за 20 епізодів")
axes[0, 1].set_xlabel("Епізод")
axes[0, 1].set_ylabel("Частка успішних епізодів")
axes[0, 1].legend()
axes[0, 1].grid(True)

# Середнє завищення Q-значень
axes[1, 0].bar(
    ["DQN", "Double DQN"],
    [
        np.mean(dqn_overestimation),
        np.mean(double_overestimation)
    ]
)
axes[1, 0].set_title("Середнє завищення Q-значень")
axes[1, 0].set_ylabel("Завищення Q")
axes[1, 0].grid(True, axis="y")

# Середня абсолютна похибка Q-значень
axes[1, 1].bar(
    ["DQN", "Double DQN"],
    [
        np.mean(np.abs(dqn_error)),
        np.mean(np.abs(double_error))
    ]
)
axes[1, 1].set_title("Середня абсолютна похибка Q-значень")
axes[1, 1].set_ylabel("Абсолютна похибка")
axes[1, 1].grid(True, axis="y")

plt.tight_layout()
plt.show()

