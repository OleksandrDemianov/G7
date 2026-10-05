namespace LaboratoryWork4.Mqtt;

public class SensorConfiguration
{
    public string Name { get; }
    public string Topic { get; }
    public string Unit { get; }
    public Func<double> GetValue { get; }

    public SensorConfiguration(
        string name,
        string topic,
        string unit,
        Func<double> getValue)
    {
        Name = name;
        Topic = topic;
        Unit = unit;
        GetValue = getValue;
    }
}
