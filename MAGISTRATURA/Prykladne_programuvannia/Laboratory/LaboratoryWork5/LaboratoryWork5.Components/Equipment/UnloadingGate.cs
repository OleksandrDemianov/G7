using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Equipment
{
    public class UnloadingGate
    {
        public bool IsOpen { get; private set; }

        public void Open()
        {
            IsOpen = true;
        }

        public void Close()
        {
            IsOpen = false;
        }

        public string GetState()
        {
            return IsOpen ? "Відкрита" : "Закрита";
        }
    }
}

