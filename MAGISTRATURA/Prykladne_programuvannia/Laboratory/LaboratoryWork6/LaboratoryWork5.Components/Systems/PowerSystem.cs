using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork5.Components.Systems
{
    public class PowerSystem
    {
        public bool MainPowerAvailable { get; private set; } = true;
        public bool ReservePowerAvailable { get; private set; }
        public bool IsReservePowerActive { get; private set; }

        public void SetMainPower(bool available)
        {
            MainPowerAvailable = available;
        }

        public void SetReservePower(bool available)
        {
            ReservePowerAvailable = available;
        }

        public void SwitchToReservePower()
        {
            if (!MainPowerAvailable && ReservePowerAvailable)
            {
                IsReservePowerActive = true;
            }
        }

        public string GetState()
        {
            return IsReservePowerActive ? "Резервне живлення" : "Основне живлення";
        }
    }
}

