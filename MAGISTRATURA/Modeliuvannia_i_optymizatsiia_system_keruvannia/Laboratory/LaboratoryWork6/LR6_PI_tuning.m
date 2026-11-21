function LR6_PI_tuning
% Синтез системи автоматичного регулювання з ПІ-регулятором
clear; clc; close all;

%% 1. Вихідні параметри об'єкта

k = 0.666667;    % °C/(м^3/год)
T1 = 1.949257;   % хв
T2 = 1.948402;   % хв
tau = 0.460484;  % хв

%% 2. Заданий ступінь загасання

psi = 0.80;
m = -log(1-psi)/(2*pi);

fprintf('psi = %.4f\n', psi);
fprintf('m = %.6f\n', m);
%% 3. Зворотна розширена АФХ об'єкта

w = 0.0005:0.0005:2.0; % рад/хв
p = (-m + 1i).*w;

Winv = ((T1.*p + 1).*(T2.*p + 1).*exp(tau.*p))./k;

R = real(Winv);
J = imag(Winv);

%% 4. Розрахунок параметрів C0 та C1

C0 = w.*(1+m^2).*J;
C1 = m.*J - R;

% Виділення точок першого квадранта
valid = (C0 >= 0) & (C1 >= 0);

w = w(valid);
C0 = C0(valid);
C1 = C1(valid);

fprintf('w_min = %.6f рад/хв\n', min(w));
fprintf('w_max = %.6f рад/хв\n', max(w));

%% 5. Лінія рівного ступеня загасання

[C0max, imax] = max(C0);
C1max = C1(imax);
wmax = w(imax);

fprintf('\nМАКСИМУМ ЛІНІЇ ЗАГАСАННЯ\n');
fprintf('C0_max = %.6f\n', C0max);
fprintf('C1_max = %.6f\n', C1max);
fprintf('w_max = %.6f рад/хв\n', wmax);

figure;
plot(C1,C0,'LineWidth',1.5);
hold on;
plot(C1max,C0max,'ro','MarkerSize',7,'LineWidth',1.2);
grid on;
box on;

xlabel('C_1 = K_p');
ylabel('C_0');
title('Лінія рівного ступеня загасання');
legend('Лінія \psi=const','Максимум C_0', ...
    'Location','best');

%% 6. Вибір робочої точки

rightFactor = 1.10;
targetC1 = rightFactor*C1max;

[~, rel] = min(abs(C1(imax:end)-targetC1));
iopt = imax + rel - 1;

C0opt = C0(iopt);
C1opt = C1(iopt);
wopt = w(iopt);

fprintf('\nОБРАНА РОБОЧА ТОЧКА\n');
fprintf('C1 = %.6f\n', C1opt);
fprintf('C0 = %.6f\n', C0opt);
fprintf('w_opt = %.6f рад/хв\n', wopt);

plot(C1opt,C0opt,'ks','MarkerSize',7,...
    'LineWidth',1.2);

legend('Лінія \psi=const','Максимум C_0',...
    'Обрана точка','Location','best');

hold off;

%% 7. Параметри ПІ-регулятора

Kp = C1opt;
Ti = C1opt/C0opt;

fprintf('\nПАРАМЕТРИ ПІ-РЕГУЛЯТОРА\n');
fprintf('Kp = %.6f\n', Kp);
fprintf('Ti = %.6f хв\n', Ti);

%% 8. Таблиця лінії рівного ступеня загасання

wTable = [0.3000; 0.3500; 0.4000; 0.4500; 0.5000; ...
    0.5500; 0.6000; 0.6500; 0.6965; 0.7000; ...
    0.7340; 0.7500; 0.8000; 0.8500; 0.9000; ...
    0.9500; 1.0000];

pTable = (-m + 1i).*wTable;

WinvTable = ((T1.*pTable + 1).*(T2.*pTable + 1).* ...
    exp(tau.*pTable))./k;

RTable = real(WinvTable);
JTable = imag(WinvTable);

C0Table = wTable.*(1+m^2).*JTable;
C1Table = m.*JTable - RTable;
TiTable = C1Table./C0Table;

Note = strings(size(wTable));

[~, idxMaxTable] = min(abs(wTable-wmax));
[~, idxOptTable] = min(abs(wTable-wopt));

Note(idxMaxTable) = "Максимум C0";
Note(idxOptTable) = "Обрана точка";

Table = table(wTable,C1Table,C0Table,TiTable,Note, ...
    'VariableNames', ...
    {'omega_rad_min','C1','C0','Ti_min','Prymitka'});

fprintf('\nЛІНІЯ РІВНОГО СТУПЕНЯ ЗАГАСАННЯ\n');
disp(Table);

%% 9. Реакція замкнутої системи на ступінчасте збурення

dAmp = 15;      % м^3/год
dt = 0.002;     % хв
tEnd = 60;      % хв

[t,y,u] = simulateDisturbance(k,T1,T2,tau, ...
    C1opt,C0opt,dAmp,dt,tEnd);

figure;
plot(t,y,'LineWidth',1.5);
grid on;
box on;
xlim([0 30]);

xlabel('Час t, хв');
ylabel('Відхилення температури \DeltaT, °C');
title('Реакція САР на ступінчасте збурення');
%% 10. Показники якості регулювання

[dTdyn, iMax] = max(y);
[dTmin, iMin] = min(y);

dTstat = mean(y(round(0.95*numel(y)):end));

band = 0.05*abs(dTdyn);

lastOutside = find(abs(y-dTstat)>band,1,'last');

if isempty(lastOutside) || lastOutside == numel(t)
    treg = NaN;
else
    treg = t(lastOutside+1);
end

% Фактичний ступінь загасання

peakInd = find(y(2:end-1)>y(1:end-2) & ...
    y(2:end-1)>=y(3:end)) + 1;

peakInd = peakInd(y(peakInd)>0);

if numel(peakInd)>=2
    psiFact = (y(peakInd(1))-y(peakInd(2)))/y(peakInd(1));
else
    psiFact = NaN;
end

fprintf('\nПОКАЗНИКИ ЯКОСТІ РЕГУЛЮВАННЯ\n');
fprintf('Максимальне відхилення = %.6f °C\n',dTdyn);
fprintf('Час максимуму = %.6f хв\n',t(iMax));
fprintf('Мінімальне відхилення = %.6f °C\n',dTmin);
fprintf('Час мінімуму = %.6f хв\n',t(iMin));
fprintf('Межі 5%% = +/- %.6f °C\n',band);
fprintf('Час регулювання = %.6f хв\n',treg);
fprintf('Статична помилка = %.8f °C\n',dTstat);
fprintf('Фактичний ступінь загасання = %.6f\n',psiFact);

% Нанесення меж п'ятивідсоткової зони

hold on;
plot(t,(dTstat+band)*ones(size(t)),'r--');
plot(t,(dTstat-band)*ones(size(t)),'r--');

legend('\DeltaT(t)','Верхня межа 5 %', ...
    'Нижня межа 5 %','Location','best');

hold off;

%% 11. Таблиця значень перехідного процесу

tOut = unique(sort([0:1:20 25 30 40 60 ...
    t(iMax) t(iMin) treg]))';

yOut = interp1(t,y,tOut,'linear');
TOut = 180 + yOut;

Result = table(tOut,yOut,TOut, ...
    'VariableNames',{'t_min','DeltaT_C','T_C'});

fprintf('\nТАБЛИЦЯ ЗНАЧЕНЬ ПЕРЕХІДНОГО ПРОЦЕСУ\n');
disp(Result);

end

%% Функція чисельного моделювання

function [t,y,u] = simulateDisturbance(k,T1,T2,tau, ...
    C1,C0,dAmp,dt,tEnd)

N = round(tEnd/dt)+1;
t = (0:N-1)'*dt;

y = zeros(N,1);
v = zeros(N,1);
z = zeros(N,1);
u = zeros(N,1);
q = zeros(N,1);

q(1) = dAmp;

for i = 1:N-1
    s = [y(i); v(i); z(i)];
    ti = t(i);

    k1 = rhsDelay(s,ti,q,i,dt,tau,k,T1,T2);
    k2 = rhsDelay(s+dt*k1/2,ti+dt/2,q,i,dt,tau,k,T1,T2);
    k3 = rhsDelay(s+dt*k2/2,ti+dt/2,q,i,dt,tau,k,T1,T2);
    k4 = rhsDelay(s+dt*k3,ti+dt,q,i,dt,tau,k,T1,T2);

    sn = s + dt*(k1+2*k2+2*k3+k4)/6;

    y(i+1) = sn(1);
    v(i+1) = sn(2);
    z(i+1) = sn(3);

    u(i+1) = -C1*y(i+1) + C0*z(i+1);
    q(i+1) = u(i+1) + dAmp;
end
end

function ds = rhsDelay(s,time,q,i,dt,tau,k,T1,T2)

y = s(1);
v = s(2);
qd = delayedValue(q,time-tau,i,dt);

ds = [v;
    (k*qd-(T1+T2)*v-y)/(T1*T2);
    -y];
end

function qd = delayedValue(q,td,i,dt)

if td < 0
    qd = 0;
    return;
end

x = td/dt;
j = floor(x)+1;
alpha = x-floor(x);

if j < 1
    qd = 0;
elseif j >= i
    qd = q(i);
else
    qd = (1-alpha)*q(j) + alpha*q(j+1);
end
end
