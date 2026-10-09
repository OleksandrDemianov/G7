using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Sensors
{
    public class GrainHumiditySensor
    {
        public double Humidity { get; private set; }

        public double MinHumidity { get; } = 0;
        public double MaxHumidity { get; } = 30;

        public void SetHumidity(double value)
        {
            if (value >= MinHumidity && value <= MaxHumidity)
            {
                Humidity = value;
            }
        }

        public bool IsHumidityNormal()
        {
            return Humidity >= 10 && Humidity <= 16;
        }
    }
}
