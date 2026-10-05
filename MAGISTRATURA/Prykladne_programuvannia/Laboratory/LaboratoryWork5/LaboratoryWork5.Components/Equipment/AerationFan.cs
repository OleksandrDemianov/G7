using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Equipment
{
    public class AerationFan
    {
        public bool IsOn { get; private set; }

        public void TurnOn()
        {
            IsOn = true;
        }

        public void TurnOff()
        {
            IsOn = false;
        }

        public string GetState()
        {
            return IsOn ? "Увімкнено" : "Вимкнено";
        }
    }
}   

