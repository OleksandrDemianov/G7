namespace GrainStorageScada.Web.Services;

public class SchemeConfigService
{
    private readonly Dictionary<string, int> _thresholds = new()
    {
        ["grainstorage/1/sensors/temperature"] = 28,
        ["grainstorage/1/sensors/humidity"] = 14,
        ["grainstorage/1/sensors/level"] = 80
    };

    public Dictionary<string, int> GetThresholds()
    {
        return new Dictionary<string, int>(_thresholds);
    }

    public bool UpdateMax(string topic, int max)
    {
        if (!_thresholds.ContainsKey(topic))
        {
            return false;
        }

        _thresholds[topic] = max;
        return true;
    }
}
