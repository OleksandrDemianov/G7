clear;
close all;
clc;

% ЛР №3. Варіант 2
T1 = 100;
T2 = 250;
K_obj = 1;
K_sens = 3.9;
T_sens = 20;
K_mech = 1;

% Контрольні значення K_I
KI_values = [0.0001:0.0001:0.0009, 0.001:0.001:0.01];

% Час моделювання
T = 12000;
t = 0:1:T;

% Передатні функції
s = tf('s');
W_obj = K_obj / ((T1*s+1)*(T2*s+1));
W_sens = K_sens / (T_sens*s+1);

% Масиви результатів
I_values = zeros(size(KI_values));
sigma_values = zeros(size(KI_values));
treg_values = zeros(size(KI_values));

for k = 1:length(KI_values)

    KI = KI_values(k);

    % І-регулятор та виконавчий механізм
    G = (KI/s)*K_mech*W_obj;

    % Замкнута система від Set_value до Object
    W_closed = feedback(G,W_sens);

    % Показники перехідного процесу
    info = stepinfo(W_closed, ...
        'SettlingTimeThreshold',0.05);

    sigma_values(k) = info.Overshoot;
    treg_values(k) = info.SettlingTime;

    % Сигнал помилки після Comparison
    W_error = feedback(1,G*W_sens);
    e = K_sens*step(W_error,t);

    % Середньоквадратичний критерій CRMS
    I_values(k) = sqrt(trapz(t,e.^2)/T);

end

% Таблиця результатів
Results = table(KI_values',I_values', ...
    sigma_values',treg_values', ...
    'VariableNames', ...
    {'K_I','I','Sigma_percent','t_reg_s'});
% Перевірка стійкості замкнутої САР
stable_values = false(size(KI_values));

for k = 1:length(KI_values)
    KI = KI_values(k);
    G = (KI/s)*K_mech*W_obj;
    W_closed = feedback(G,W_sens);
    stable_values(k) = isstable(W_closed);
end

Results.Stable = stable_values';

disp(Results);


% Графік залежності I від K_I
figure;
plot(KI_values(stable_values), ...
    I_values(stable_values), '-o');

grid on;
xlabel('K_I');
ylabel('I');
title('Залежність інтегрального критерію якості від K_I');

% Графік залежності перерегулювання sigma від K_I
figure;
plot(KI_values(stable_values), ...
    sigma_values(stable_values), '-o');

grid on;
xlabel('K_I');
ylabel('\sigma, %');
title('Залежність перерегулювання від K_I');

% Графік залежності часу регулювання від K_I
figure;
plot(KI_values(stable_values), ...
    treg_values(stable_values), '-o');

grid on;
xlabel('K_I');
ylabel('t_{рег}, c');
title('Залежність часу регулювання від K_I');