using LaboratoryWork3;
using LaboratoryWork4.Mqtt;
using MQTTnet;
using System.Text;
using System.Text.Json;

Console.OutputEncoding = Encoding.UTF8;

GrainStorageControlSystem system = new GrainStorageControlSystem();

Console.WriteLine("=== АВТОМАТИЗОВАНА СИСТЕМА ЗБЕРІГАННЯ ЗЕРНА ===");
Console.WriteLine();

// Конфігурація MQTT-тем сенсорів
SensorConfiguration[] sensors =
[
    new SensorConfiguration(
        "Температура зерна",
        "grainstorage/1/sensors/temperature",
        "C",
        () => system.TemperatureSensor.Temperature),

    new SensorConfiguration(
        "Вологість зерна",
        "grainstorage/1/sensors/humidity",
        "%",
        () => system.HumiditySensor.Humidity),

    new SensorConfiguration(
        "Рівень зерна",
        "grainstorage/1/sensors/level",
        "%",
        () => system.LevelSensor.Level)
];

// Створення MQTT-клієнта
var factory = new MqttClientFactory();
using var mqttClient = factory.CreateMqttClient();

var options = new MqttClientOptionsBuilder()
    .WithTcpServer("127.0.0.1", 1883)
    .Build();

await mqttClient.ConnectAsync(options);

Console.WriteLine("Підключено до MQTT-брокера.");
Console.WriteLine();

// Цикл роботи симулятора
for (int iteration = 1; iteration <= 10; iteration++)
{
    Console.WriteLine($"Ітерація {iteration}");

    // Моделювання поточних показань сенсорів
    system.TemperatureSensor.SetTemperature(
        Math.Round(5 + Random.Shared.NextDouble() * 30, 2));

    system.HumiditySensor.SetHumidity(
        Math.Round(10 + Random.Shared.NextDouble() * 10, 2));

    system.LevelSensor.SetLevel(
        Math.Round(Random.Shared.NextDouble() * 100, 2));

    // Автоматичне керування системою
    system.AutomaticControl();

    // Публікація показань усіх сенсорів
    foreach (var sensor in sensors)
    {
        await PublishSensorReadingAsync(mqttClient, sensor);
    }

    Console.WriteLine();

    await Task.Delay(TimeSpan.FromSeconds(2));
}

await mqttClient.DisconnectAsync();

Console.WriteLine("Відключено від MQTT-брокера.");

static async Task PublishSensorReadingAsync(
    IMqttClient mqttClient,
    SensorConfiguration sensor)
{
    string payload = JsonSerializer.Serialize(new
    {
        value = Math.Round(sensor.GetValue(), 2),
        unit = sensor.Unit,
        measuredAtUtc = DateTimeOffset.UtcNow
    });

    var message = new MqttApplicationMessageBuilder()
        .WithTopic(sensor.Topic)
        .WithPayload(payload)
        .Build();

    await mqttClient.PublishAsync(message);

    Console.WriteLine(
        $"Published {sensor.Topic} -> {payload}");
}
