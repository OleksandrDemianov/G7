(* Emergency stop and alarm activation *)
IF emergencyStop THEN
    motorRunning := FALSE;
    alarmActive := TRUE;
END_IF;

(* Alarm reset *)
IF resetAlarm AND NOT emergencyStop THEN
    alarmActive := FALSE;
END_IF;

(* Manual reset of the start counter *)
IF resetStartCount THEN
    startCount := 0;
END_IF;

(* Motor control *)
IF stopButton OR alarmActive THEN
    motorRunning := FALSE;

ELSIF manual THEN
    (* Manual mode *)
    IF startButton AND motorReady AND (startCount < 5) THEN
        motorRunning := TRUE;
    END_IF;

ELSE
    (* Automatic mode *)
    IF autoStart AND motorReady AND
       (motorRunning OR (startCount < 5)) THEN
        motorRunning := TRUE;
    ELSE
        motorRunning := FALSE;
    END_IF;
END_IF;

(* Count each new motor start *)
IF motorRunning AND NOT prevMotorRunning THEN
    startCount := startCount + 1;
END_IF;

(* Save previous motor state *)
prevMotorRunning := motorRunning;
