(* PR4 - Conveyor Control - Variant 3 *)
(* Two-stage conveyor with quality control *)

(* 1. Start and Stop *)

IF startConveyor AND NOT stopConveyor
   AND NOT shiftComplete AND NOT defectAlarm THEN
    conveyorActive := TRUE;
END_IF;

IF stopConveyor THEN
    conveyorActive := FALSE;
END_IF;

(* 2. Detect one product *)

productPulse := sensorPulse AND NOT sensorPulsePrev
                AND motorRunning;

sensorPulsePrev := sensorPulse;

(* 3. Reset parts counter after pause *)

resetParts := pauseTimer.Q;

(* 4. Count good products *)

counter1(
    CU := productPulse AND NOT defectSensor,
    RESET := resetCounter OR resetParts,
    PV := 5
);

currentCount := counter1.CV;
containerFull := counter1.Q;

(* 5. Count consecutive defects *)

defectCounter(
    CU := productPulse AND defectSensor,
    RESET := resetCounter OR
             (productPulse AND NOT defectSensor),
    PV := 3
);

defectCount := defectCounter.CV;
defectAlarm := defectCounter.Q;

(* 6. Count completed containers *)

counter2(
    CU := containerFull AND NOT containerPulse,
    RESET := resetCounter,
    PV := 3
);

containerPulse := containerFull;

containerCount := counter2.CV;
shiftComplete := counter2.Q;

(* 7. Pause for 3 seconds *)

pauseTimer(
    containerFull AND NOT shiftComplete
    AND NOT defectAlarm AND conveyorActive,
    3
);

(* 8. Stop cycle on alarm or shift completion *)

IF defectAlarm OR shiftComplete OR stopConveyor THEN
    conveyorActive := FALSE;
END_IF;

(* 9. Final motor control *)

motorRunning := conveyorActive
                AND NOT containerFull
                AND NOT shiftComplete
                AND NOT defectAlarm
                AND NOT stopConveyor;
