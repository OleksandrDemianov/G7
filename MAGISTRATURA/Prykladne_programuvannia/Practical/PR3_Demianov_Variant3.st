(* Stop cycle or start on rising edge *)
IF stopButton THEN
    cycleActive := FALSE;
    pumpPhase := FALSE;
ELSIF StartButton AND NOT startButtonPrev AND NOT cycleActive THEN
    cycleActive := TRUE;
    pumpPhase := TRUE;
END_IF;

(* Save previous Start state *)
startButtonPrev := StartButton;

(* Pump runs for 5 seconds *)
pumpTimer(cycleActive AND pumpPhase, 5);

(* Pump pauses for 3 seconds *)
pauseTimer(cycleActive AND NOT pumpPhase, 3);

(* Automatic phase switching *)
IF cycleActive THEN
    IF pumpPhase AND pumpTimer.Q THEN
        pumpPhase := FALSE;
    ELSIF NOT pumpPhase AND pauseTimer.Q THEN
        pumpPhase := TRUE;
    END_IF;
END_IF;

(* Pump output *)
pumpRunning := cycleActive AND pumpPhase AND NOT stopButton;

(* Fan overrun for 30 seconds *)
fanOffDelay(pumpRunning, 30);
fanRunning := fanOffDelay.Q;
