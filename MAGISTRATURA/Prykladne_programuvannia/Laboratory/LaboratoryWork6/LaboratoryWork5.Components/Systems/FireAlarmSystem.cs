using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Systems
{
    public class FireAlarmSystem
    {
        public bool IsAlarmActive { get; private set; }

        public void ActivateAlarm()
        {
            IsAlarmActive = true;
        }

        public void ResetAlarm()
        {
            IsAlarmActive = false;
        }

        public string GetState()
        {
            return IsAlarmActive ? "Пожежна тривога" : "Нормальний стан";
        }
    }
}

