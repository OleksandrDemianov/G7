
updateTimer(NOT updateTimer.Q, 2);

IF updateTimer.Q THEN
    speedStr := ANY_TO_STRING(speedValue);
    torqueStr := ANY_TO_STRING(torqueValue);

    outMessage := CONCAT(CONCAT(CONCAT(CONCAT(
        'SPEED=', speedStr),
        ';TORQUE='),
        torqueStr),
        '$R$N');
END_IF;
