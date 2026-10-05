using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork3
{
    public class UnloadingConveyor
    {
        public bool IsRunning { get; private set; }

        public void Start()
        {
            IsRunning = true;
        }

        public void Stop()
        {
            IsRunning = false;
        }

        public string GetState()
        {
            return IsRunning ? "Працює" : "Зупинено";
        }
    }
}

