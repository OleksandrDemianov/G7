using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork3
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

