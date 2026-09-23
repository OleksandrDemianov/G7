# Початкові факти для чіткої логіки
temperature_high = True
vibration_high = True
noise_present = True

# Чітка логіка
if temperature_high and vibration_high and noise_present:
    clear_result = "Несправність обладнання виявлена"
else:
    clear_result = "Несправність обладнання не виявлена"

# Коефіцієнти впевненості Certainty Factor
temperature_cf = 0.9
vibration_cf = 0.8
noise_cf = 0.7

# Коефіцієнт впевненості правила
rule_cf = 0.85

# Розрахунок підсумкового CF
facts_cf = min(temperature_cf, vibration_cf, noise_cf)
result_cf = facts_cf * rule_cf

# Виведення результатів
print("Чітка логіка:")
print(clear_result)

print()

print("Certainty Factor:")
print("Коефіцієнт впевненості =", round(result_cf, 3))
