function LR5_identification
% Експериментальна ідентифікація об'єкта керування
clear; clc; close all;

%% 1. Експериментальні дані
t = [0 0.8 1.1 1.4 1.7 1.9 2.2 3.1 3.6 4.2 ...
    4.7 5.3 5.8 6.4 6.9 7.5 8.2 8.741 9.023 9.392 10]';

Texp = [180 180 180 180.6 181.58 182.04 182.67 183.9 ...
    184.74 186.1 185.93 186.68 187.74 187.7 188.14 ...
    188.75 189.16 189.42 189.73 189.85 190]';

F0 = 125;
F1 = 140;
dF = F1 - F0;

T0 = Texp(1);
Tinf = Texp(end);

%% 2. Східчаста зміна витрати гарячої води
tStep = [-1 0 0 10];
QStep = [F0 F0 F1 F1];

figure;
plot(tStep, QStep, 'LineWidth', 2.4);
grid on; box on;
xlim([-1 10]);
ylim([124 141]);
xlabel('t, хв');
ylabel('G_{г.в.}, м^3/год');
title('Східчаста зміна витрати гарячої води');


%% 3. Експериментальна перехідна характеристика

figure;
plot(t, Texp, 'o-', 'LineWidth', 1.5);
grid on;
box on;

xlabel('Час t, хв');
ylabel('Температура T, °C');
title('Експериментальна перехідна характеристика');
xlim([0 10]);

%% 4. Основні параметри для ідентифікації

T0 = Texp(1);          % початкова температура
Tust = Texp(end);      % усталена температура
dT = Tust - T0;        % зміна температури

G0 = F0;            % початкова витрата
Gust = F1;        % кінцева витрата
dG = Gust - G0;        % зміна витрати

Kobj = dT / dG;        % коефіцієнт передачі об'єкта

fprintf('\nОСНОВНІ ПАРАМЕТРИ ОБ''ЄКТА\n');
fprintf('T0 = %.3f °C\n', T0);
fprintf('Tust = %.3f °C\n', Tust);
fprintf('dT = %.3f °C\n', dT);
fprintf('G0 = %.3f м^3/год\n', G0);
fprintf('Gust = %.3f м^3/год\n', Gust);
fprintf('dG = %.3f м^3/год\n', dG);
fprintf('Kobj = %.6f (°C)/(м^3/год)\n', Kobj);


%% 5. Згладжування експериментальних даних методом п'яти точок

n = length(Texp);
Tsm = zeros(size(Texp));

for i = 1:n
    i1 = max(1, min(i-2, n-4));
    ind = i1:min(i1+4, n);

    % Локальна квадратична апроксимація п'яти точок
    p = polyfit(t(ind), Texp(ind), 2);
    Tsm(i) = polyval(p, t(i));
end

%% Графік експериментальних та згладжених даних

figure;
plot(t, Texp, 'o-', 'LineWidth', 1.2);
hold on;
plot(t, Tsm, '--', 'LineWidth', 1.5);
hold off;

grid on;
box on;
xlabel('Час t, хв');
ylabel('Температура T, °C');
title('Згладжування перехідної характеристики');
legend('Експериментальні дані', 'Згладжені дані', ...
    'Location', 'best');
xlim([0 10]);


%% 6. Апроксимація перехідної характеристики

k = Kobj;

% Початкові наближення параметрів
q0 = log([1.2 1.2 0.6]);

% Мінімізація суми квадратів відхилень
objective = @(q) sum((Tsm - sopdt(t,T0,dF,k,q)).^2);

options = optimset('Display','iter', ...
    'MaxIter',20000, ...
    'MaxFunEvals',50000, ...
    'TolX',1e-10, ...
    'TolFun',1e-12);

q = fminsearch(objective,q0,options);

% Параметри об'єкта
T2 = exp(q(1));
T1 = T2 + exp(q(2));
tau = exp(q(3));

% Розрахункова перехідна характеристика
Tmodel = sopdt(t,T0,dF,k,q);

fprintf('\nРЕЗУЛЬТАТИ АПРОКСИМАЦІЇ\n');
fprintf('k = %.6f\n',k);
fprintf('T1 = %.6f хв\n',T1);
fprintf('T2 = %.6f хв\n',T2);
fprintf('tau = %.6f хв\n',tau);


%% 7. Оцінювання точності апроксимації

% Відхилення згладжених даних від моделі
error = Tsm - Tmodel;

% Показники точності
SSE = sum(error.^2);
RMSE = sqrt(mean(error.^2));
R2 = 1 - SSE/sum((Tsm - mean(Tsm)).^2);
ISE = trapz(t, error.^2);

% Виведення результатів
fprintf('\nПОКАЗНИКИ ТОЧНОСТІ АПРОКСИМАЦІЇ\n');
fprintf('SSE = %.6f °C^2\n', SSE);
fprintf('RMSE = %.6f °C\n', RMSE);
fprintf('R^2 = %.6f\n', R2);
fprintf('ISE = %.6f °C^2*хв\n', ISE);


%% 8. Графік апроксимації перехідної характеристики

figure;
plot(t, Tsm, 'o', 'LineWidth', 1.3);
hold on;
plot(t, Tmodel, '-', 'LineWidth', 1.5);
hold off;

grid on;
box on;

xlabel('Час t, хв');
ylabel('Температура T, °C');
title('Апроксимація кривої розгону');

legend('Згладжені дані', 'Модель SOPDT', ...
    'Location', 'best');

xlim([0 10]);


%% 9. Передатна функція об'єкта

% Коефіцієнти знаменника
a2 = T1 * T2;
a1 = T1 + T2;

fprintf('\nПЕРЕДАТНА ФУНКЦІЯ ОБ''ЄКТА\n');

fprintf('\nФакторизований вигляд:\n');
fprintf('W(s) = %.6f*exp(-%.6f*s)/', k, tau);
fprintf('((%.6f*s+1)*(%.6f*s+1))\n', T1, T2);

fprintf('\nРозгорнутий вигляд:\n');
fprintf('W(s) = %.6f*exp(-%.6f*s)/', k, tau);
fprintf('(%.6f*s^2+%.6f*s+1)\n', a2, a1);


%% 10. Таблиця результатів згладжування та апроксимації

Results = table(t, Texp, Tsm, Tmodel, error, ...
    'VariableNames', {'t_min', 'T_exp', 'T_smooth', ...
    'T_model', 'Error'});

fprintf('\nТАБЛИЦЯ РЕЗУЛЬТАТІВ\n');
disp(Results);

end


function y = sopdt(t,T0,dF,k,q)

T2 = exp(q(1));
T1 = T2 + exp(q(2));
tau = exp(q(3));

y = T0 * ones(size(t));
ind = t >= tau;
theta = t(ind) - tau;

if abs(T1-T2) < 1e-3
    Tav = (T1+T2)/2;
    g = 1-exp(-theta/Tav).*(1+theta/Tav);
else
    g = 1-(T1*exp(-theta/T1) ...
        -T2*exp(-theta/T2))/(T1-T2);
end

y(ind) = T0 + k*dF*g;

end
