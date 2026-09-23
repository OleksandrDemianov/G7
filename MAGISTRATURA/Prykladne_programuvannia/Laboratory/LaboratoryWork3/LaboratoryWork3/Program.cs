using LaboratoryWork3;
using System.Text;

Console.OutputEncoding = Encoding.UTF8;

GrainStorageControlSystem system = new GrainStorageControlSystem();

Console.WriteLine("=== АВТОМАТИЗОВАНА СИСТЕМА ЗБЕРІГАННЯ ЗЕРНА ===");
Console.WriteLine();

// Задаємо поточні значення датчиків
system.TemperatureSensor.SetTemperature(32);
system.HumiditySensor.SetHumidity(17);
system.LevelSensor.SetLevel(75);

// Запускаємо автоматичне керування
system.AutomaticControl();

// Виведення параметрів
Console.WriteLine($"Температура зерна: {system.TemperatureSensor.Temperature} °C");
Console.WriteLine($"Вологість зерна: {system.HumiditySensor.Humidity} %");
Console.WriteLine($"Рівень зерна: {system.LevelSensor.Level} %");

Console.WriteLine();

Console.WriteLine($"Вентилятор аерації: {system.AerationFan.GetState()}");
Console.WriteLine($"Завантажувальний транспортер: {system.LoadingConveyor.GetState()}");
Console.WriteLine($"Розвантажувальний транспортер: {system.UnloadingConveyor.GetState()}");
Console.WriteLine($"Норія: {system.BucketElevator.GetState()}");

Console.WriteLine();

Console.WriteLine($"Завантажувальна засувка: {system.LoadingGate.GetState()}");
Console.WriteLine($"Розвантажувальна засувка: {system.UnloadingGate.GetState()}");
Console.WriteLine($"Система аспірації: {system.AspirationSystem.GetState()}");
Console.WriteLine($"Система вентиляції: {system.VentilationSystem.GetState()}");
Console.WriteLine($"Освітлення: {system.LightingSystem.GetState()}");

Console.WriteLine();

Console.WriteLine($"Електроживлення: {system.PowerSystem.GetState()}");
Console.WriteLine($"Пожежна сигналізація: {system.FireAlarmSystem.GetState()}");

