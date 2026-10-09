
using System.Collections.Concurrent;
using GrainStorageScada.Web.Models;

namespace GrainStorageScada.Web.Services
{
    public class LiveValuesCache
    {
        private readonly ConcurrentDictionary<string, SensorReading>
            _readings = new();

        public void Update(SensorReading reading)
        {
            _readings[reading.Topic] = reading;
        }

        public SensorReading? Get(string topic)
        {
            return _readings.TryGetValue(topic, out var reading)
                ? reading
                : null;
        }

        public IReadOnlyList<SensorReading> GetAll()
        {
            return _readings.Values.ToList();
        }
    }
}

