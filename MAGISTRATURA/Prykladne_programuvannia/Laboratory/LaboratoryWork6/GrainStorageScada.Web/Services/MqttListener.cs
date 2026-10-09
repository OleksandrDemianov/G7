
using System.Text.Json;
using GrainStorageScada.Web.Models;
using MQTTnet;

namespace GrainStorageScada.Web.Services
{
    public class MqttListener : BackgroundService
    {
        private static readonly JsonSerializerOptions JsonOptions =
            new() { PropertyNameCaseInsensitive = true };

        private readonly LiveValuesCache _cache;
        private readonly IConfiguration _config;
        private readonly ILogger<MqttListener> _logger;

        public MqttListener(
            LiveValuesCache cache,
            IConfiguration config,
            ILogger<MqttListener> logger)
        {
            _cache = cache;
            _config = config;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(
            CancellationToken stoppingToken)
        {
            var factory = new MqttClientFactory();

            using var client = factory.CreateMqttClient();

            client.ApplicationMessageReceivedAsync += OnMessageReceivedAsync;

            var options = new MqttClientOptionsBuilder()
                .WithTcpServer(
                    _config["Mqtt:Host"],
                    _config.GetValue<int>("Mqtt:Port"))
                .Build();

            var subscribeOptions = factory
                .CreateSubscribeOptionsBuilder()
                .WithTopicFilter(_config["Mqtt:TopicFilter"]!)
                .Build();

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    if (!client.IsConnected)
                    {
                        await client.ConnectAsync(options, stoppingToken);

                        _logger.LogInformation(
                            "Підключено до MQTT-брокера");

                        await client.SubscribeAsync(
                            subscribeOptions, stoppingToken);

                        _logger.LogInformation(
                            "Підписано на {Filter}",
                            _config["Mqtt:TopicFilter"]);
                    }

                    await Task.Delay(
                        TimeSpan.FromSeconds(5), stoppingToken);
                }
                catch (OperationCanceledException)
                    when (stoppingToken.IsCancellationRequested)
                {
                    break;
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(
                        ex,
                        "MQTT-з'єднання недоступне. Повтор через 5 с");

                    await Task.Delay(
                        TimeSpan.FromSeconds(5), stoppingToken);
                }
            }
        }

        private Task OnMessageReceivedAsync(
            MqttApplicationMessageReceivedEventArgs e)
        {
            try
            {
                string topic = e.ApplicationMessage.Topic;
                string json =
                    e.ApplicationMessage.ConvertPayloadToString();

                MqttPayload? payload =
                    JsonSerializer.Deserialize<MqttPayload>(
                        json, JsonOptions);

                if (payload is not null)
                {
                    var reading = new SensorReading
                    {
                        Topic = topic,
                        Value = payload.Value,
                        Unit = payload.Unit,
                        MeasuredAtUtc = payload.MeasuredAtUtc
                    };

                    _cache.Update(reading);
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(
                    ex, "Помилка обробки MQTT-повідомлення");
            }

            return Task.CompletedTask;
        }

        private class MqttPayload
        {
            public double Value { get; set; }

            public string Unit { get; set; } = "";

            public DateTimeOffset MeasuredAtUtc { get; set; }
        }
    }
}
