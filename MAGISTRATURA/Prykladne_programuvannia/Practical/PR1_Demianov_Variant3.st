(* Input values for Variant 3 *)
operandA := 77;
operandB := 9;

(* Basic arithmetic operations *)
sumResult := operandA + operandB;
diffResult := operandA - operandB;
prodResult := operandA * operandB;
divResult := operandA / operandB;

(* Arithmetic mean *)
avgValue := ANY_TO_REAL(operandA + operandB) / 2.0;

(* Additional operations *)
modResult := operandA MOD operandB;
squareA := operandA * operandA;
absResult := ABS(operandA - operandB);
