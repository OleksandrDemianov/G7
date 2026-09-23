using System;
using System.Collections.Generic;
using System.Text;

namespace LaboratoryWork3
{
    public class LoadingGate
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

