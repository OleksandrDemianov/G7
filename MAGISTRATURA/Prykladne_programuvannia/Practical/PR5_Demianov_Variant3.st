
(* PR5 - Humidity Control *)

(* 1. Analog signal simulation *)
IF simDirection THEN
    rawHumidityValue := rawHumidityValue + simStep;

    IF rawHumidityValue >= 32767 THEN
        rawHumidityValue := 32767;
        simDirection := FALSE;
    END_IF;
ELSE
    rawHumidityValue := rawHumidityValue - simStep;

    IF rawHumidityValue <= 0 THEN
        rawHumidityValue := 0;
        simDirection := TRUE;
    END_IF;
END_IF;

(* 2. Analog signal scaling *)
scaledHumidity :=
    ANY_TO_REAL(rawHumidityValue) * 100.0 / 32767.0;

(* 3. Hysteresis thresholds *)
lowerThreshold := setPoint - hysteresis / 2.0;
upperThreshold := setPoint + hysteresis / 2.0;

(* 4. Humidifier control *)
IF scaledHumidity < lowerThreshold THEN
    humidifierOutput := TRUE;
ELSIF scaledHumidity > upperThreshold THEN
    humidifierOutput := FALSE;
END_IF;
