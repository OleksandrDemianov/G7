using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Sensors
{
    public class GrainTemperatureSensor
    {
        public double Temperature { get; private set; }

        public double MinTemperature { get; } = -30;
        public double MaxTemperature { get; } = 80;

        public void SetTemperature(double value)
        {
            if (value >= MinTemperature && value <= MaxTemperature)
            {
                Temperature = value;
            }
        }

        public bool IsTemperatureNormal()
        {
            return Temperature >= 5 && Temperature <= 30;
        }
    }
}
