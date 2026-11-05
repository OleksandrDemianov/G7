
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============================================================
# Практична робота №4
# Інтелектуальні системи в робототехніці
# Варіант №11
# Керування дволанковим маніпулятором методом CTC
# ============================================================

# 1. Параметри маніпулятора
L1 = 1.0
L2 = 0.8
m1 = 2.0
m2 = 1.5
g = 9.81

lc1 = L1 / 2
lc2 = L2 / 2

I1 = m1 * L1**2 / 12
I2 = m2 * L2**2 / 12

T = 12.0

# 2. Коефіцієнти CTC-регулятора
Kp = np.diag([50.0, 50.0])
Kd = np.diag([14.0, 14.0])


# 3. Задана траєкторія руху
def desired_trajectory(t):
    qd = np.array([
        0.5 + 0.3 * np.sin(0.6 * t),
        0.4 + 0.25 * np.sin(0.8 * t)
    ])

    dqd = np.array([
        0.18 * np.cos(0.6 * t),
        0.20 * np.cos(0.8 * t)
    ])

    ddqd = np.array([
        -0.108 * np.sin(0.6 * t),
        -0.16 * np.sin(0.8 * t)
    ])

    return qd, dqd, ddqd


# 4. Математична модель маніпулятора
def robot_model(q, dq):
    q1, q2 = q
    dq1, dq2 = dq

    # Матриця інерції
    M11 = (
        I1 + I2 + m1 * lc1**2
        + m2 * (L1**2 + lc2**2
                + 2 * L1 * lc2 * np.cos(q2))
    )

    M12 = I2 + m2 * (
        lc2**2 + L1 * lc2 * np.cos(q2)
    )

    M22 = I2 + m2 * lc2**2

    M = np.array([
        [M11, M12],
        [M12, M22]
    ])

    # Коріолісові та відцентрові складові
    h = m2 * L1 * lc2 * np.sin(q2)

    C = np.array([
        -h * (2 * dq1 * dq2 + dq2**2),
        h * dq1**2
    ])

    # Гравітаційні моменти
    G = np.array([
        (m1 * lc1 + m2 * L1) * g * np.cos(q1)
        + m2 * lc2 * g * np.cos(q1 + q2),

        m2 * lc2 * g * np.cos(q1 + q2)
    ])

    return M, C, G


# 5. Закон керування Computed Torque Control
def ctc_controller(t, q, dq):
    qd, dqd, ddqd = desired_trajectory(t)

    e = qd - q
    de = dqd - dq

    M, C, G = robot_model(q, dq)

    v = ddqd + Kd @ de + Kp @ e

    tau = M @ v + C + G

    return tau


# 6. Рівняння руху замкненої системи
def robot_dynamics(t, state):
    q = state[:2]
    dq = state[2:]

    M, C, G = robot_model(q, dq)

    tau = ctc_controller(t, q, dq)

    ddq = np.linalg.solve(M, tau - C - G)

    return np.concatenate([dq, ddq])


# 7. Початкові умови
qd0, _, _ = desired_trajectory(0)

initial_state = [
    qd0[0] - 0.20,
    qd0[1] + 0.15,
    0.0,
    0.0
]

time = np.linspace(0, T, 1201)

# 8. Комп'ютерне моделювання
solution = solve_ivp(
    robot_dynamics,
    [0, T],
    initial_state,
    t_eval=time,
    rtol=1e-8,
    atol=1e-10
)

if not solution.success:
    raise RuntimeError(solution.message)

q = solution.y[:2].T
dq = solution.y[2:].T

qd = np.array([
    desired_trajectory(t)[0] for t in time
])

error = qd - q

tau = np.array([
    ctc_controller(t, q[i], dq[i])
    for i, t in enumerate(time)
])

# 9. Оцінювання точності керування
rmse = np.sqrt(np.mean(error**2, axis=0))
max_error = np.max(np.abs(error), axis=0)

print("ПРАКТИЧНА РОБОТА №4")
print("Варіант №11 — Computed Torque Control")
print("=" * 50)

for i in range(2):
    print(f"Суглоб {i + 1}:")
    print(f"  RMSE = {rmse[i]:.6f} рад")
    print(f"  Максимальна похибка = {max_error[i]:.6f} рад")
    print(f"  Кінцева похибка = {error[-1, i]:.6f} рад")

print("=" * 50)
print("Моделювання завершено успішно.")

# 10. Графік кутових положень
plt.figure(figsize=(10, 6))

plt.plot(time, qd[:, 0], label="q1 задане")
plt.plot(time, q[:, 0], "--", label="q1 фактичне")
plt.plot(time, qd[:, 1], label="q2 задане")
plt.plot(time, q[:, 1], "--", label="q2 фактичне")

plt.xlabel("Час, с")
plt.ylabel("Кутове положення, рад")
plt.title("Відстеження траєкторії методом CTC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("CTC_01_Trajectory.png", dpi=200)

# 11. Графік похибок керування
plt.figure(figsize=(10, 6))

plt.plot(time, error[:, 0], label="Похибка q1")
plt.plot(time, error[:, 1], label="Похибка q2")

plt.xlabel("Час, с")
plt.ylabel("Похибка, рад")
plt.title("Похибки відстеження траєкторії")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("CTC_02_Errors.png", dpi=200)

# 12. Графік керувальних моментів
plt.figure(figsize=(10, 6))

plt.plot(time, tau[:, 0], label="Момент tau1")
plt.plot(time, tau[:, 1], label="Момент tau2")

plt.xlabel("Час, с")
plt.ylabel("Керувальний момент, Н·м")
plt.title("Керувальні моменти CTC-регулятора")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("CTC_03_Torques.png", dpi=200)

plt.show()

