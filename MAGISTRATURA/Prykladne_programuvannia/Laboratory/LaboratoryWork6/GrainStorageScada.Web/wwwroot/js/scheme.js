
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
                    const unit = reading.topic === "grainstorage/1/sensors/temperature"
                        ? "°C"
                        : reading.unit;

                    element.textContent =
                        `${reading.value.toFixed(2)} ${unit}`;

                    if (reading.topic === "grainstorage/1/sensors/temperature") {
                        element.style.color = reading.value > 28 ? "red" : "white";
                    }

                    if (reading.topic === "grainstorage/1/sensors/humidity") {
                        element.style.color = reading.value > 14 ? "red" : "white";
                    }

                    if (reading.topic === "grainstorage/1/sensors/level") {
                        element.style.color = reading.value > 80 ? "red" : "white";
                    }
                }
            }
        } catch (error) {
            console.error("Помилка отримання показань:", error);
        }
    }

    updateReadings();
    setInterval(updateReadings, 2000);
});

