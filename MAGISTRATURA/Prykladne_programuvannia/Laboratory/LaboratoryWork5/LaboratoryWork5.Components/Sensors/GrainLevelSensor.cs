using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Sensors
{
    public class GrainLevelSensor
    {
        public double Level { get; private set; }

        public double MinLevel { get; } = 0;
        public double MaxLevel { get; } = 100;

        public void SetLevel(double value)
        {
            if (value >= MinLevel && value <= MaxLevel)
            {
                Level = value;
            }
        }

        public bool IsFull()
        {
            return Level >= 100;
        }

        public bool IsEmpty()
        {
            return Level <= 0;
        }
    }
}
