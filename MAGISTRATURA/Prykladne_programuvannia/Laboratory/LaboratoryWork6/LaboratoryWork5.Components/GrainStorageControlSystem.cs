using LaboratoryWork5.Components.Sensors;
using LaboratoryWork5.Components.Equipment;
using LaboratoryWork5.Components.Systems;

namespace LaboratoryWork5.Components
{
    public class GrainStorageControlSystem
    {
        public GrainTemperatureSensor TemperatureSensor { get; }
        public GrainHumiditySensor HumiditySensor { get; }
        public GrainLevelSensor LevelSensor { get; }

        public AerationFan AerationFan { get; }
        public LoadingConveyor LoadingConveyor { get; }
        public UnloadingConveyor UnloadingConveyor { get; }
        public BucketElevator BucketElevator { get; }

        public LoadingGate LoadingGate { get; }
        public UnloadingGate UnloadingGate { get; }

        public AspirationSystem AspirationSystem { get; }
        public VentilationSystem VentilationSystem { get; }
        public LightingSystem LightingSystem { get; }

        public PowerSystem PowerSystem { get; }
        public FireAlarmSystem FireAlarmSystem { get; }

        public GrainStorageControlSystem()
        {
            TemperatureSensor = new GrainTemperatureSensor();
            HumiditySensor = new GrainHumiditySensor();
            LevelSensor = new GrainLevelSensor();

            AerationFan = new AerationFan();
            LoadingConveyor = new LoadingConveyor();
            UnloadingConveyor = new UnloadingConveyor();
            BucketElevator = new BucketElevator();

            LoadingGate = new LoadingGate();
            UnloadingGate = new UnloadingGate();

            AspirationSystem = new AspirationSystem();
            VentilationSystem = new VentilationSystem();
            LightingSystem = new LightingSystem();

            PowerSystem = new PowerSystem();
            FireAlarmSystem = new FireAlarmSystem();
        }

        public void AutomaticControl()
        {
            if (!TemperatureSensor.IsTemperatureNormal() ||
                !HumiditySensor.IsHumidityNormal())
            {
                AerationFan.TurnOn();
            }
            else
            {
                AerationFan.TurnOff();
            }

            if (FireAlarmSystem.IsAlarmActive)
            {
                LoadingConveyor.Stop();
                UnloadingConveyor.Stop();
                BucketElevator.Stop();
                AerationFan.TurnOff();
            }
        }
    }
}
