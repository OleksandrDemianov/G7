document.addEventListener("DOMContentLoaded", () => {
    const sensors = {
        "grainstorage/1/sensors/temperature": "temperature-value",
        "grainstorage/1/sensors/humidity": "humidity-value",
        "grainstorage/1/sensors/level": "level-value"
    };

    async function updateReadings() {
        try {
            const response = await fetch("/Scheme/Readings");
            const thresholdResponse = await fetch("/Scheme/Thresholds");

            if (response.redirected || thresholdResponse.redirected) {
                window.location.reload();
                return;
            }

            if (!response.ok || !thresholdResponse.ok) {
                throw new Error("Помилка HTTP-запиту");
            }

            const readings = await response.json();
            const thresholds = await thresholdResponse.json();

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

                    const max = thresholds[reading.topic];

                    element.style.color =
                        max !== undefined && reading.value > max
                            ? "red"
                            : "white";
                }
            }
        } catch (error) {
            console.error("Помилка отримання показань:", error);
        }
    }

    updateReadings();
    setInterval(updateReadings, 2000);
});
