
document.addEventListener("DOMContentLoaded", () => {
    const sensors = {
        "grainstorage/1/sensors/temperature": "temperature-value",
        "grainstorage/1/sensors/humidity": "humidity-value",
        "grainstorage/1/sensors/level": "level-value"
    };

    async function updateReadings() {
        try {
            const response = await fetch("/Scheme/Readings");

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const readings = await response.json();

            for (const reading of readings) {
                const elementId = sensors[reading.topic];

                if (!elementId) continue;

                const element = document.getElementById(elementId);

                if (element) {
                    element.textContent =
                        `${reading.value.toFixed(2)} ${reading.unit}`;
                }
            }
        } catch (error) {
            console.error("Помилка отримання показань:", error);
        }
    }

    updateReadings();
    setInterval(updateReadings, 2000);
});

