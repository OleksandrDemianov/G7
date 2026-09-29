clear all;
close all;
clc;

global T1 T2 K_obj
global K_sens T_sens
global K_mech
global K_p

T1 = 100;
T2 = 250;
K_obj = 1;
K_sens = 3.9;
T_sens = 20;
K_mech = 1;
K_p = 6;

W_obj = tf(K_obj, [T1*T2, T1+T2, 1]);
W_sens = tf(K_sens, [T_sens, 1]);

W_forward = K_p * K_mech * W_obj;

W_closed = K_sens * feedback(W_forward, W_sens);

info = stepinfo(W_closed,'SettlingTimeThreshold',0.05);
y_ss = dcgain(W_closed);
e_st = 1 - y_ss;

disp(info)
disp(['Steady State = ', num2str(y_ss)])
disp(['Static Error = ', num2str(e_st)])

Kp_values = [0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5];
sigma_values = [11.60 27.17 39.98 50.77 60.13 68.61 76.15 83.05 89.42 95.36 100.94];

figure;
plot(Kp_values, sigma_values, '-o');
grid on;

xlabel('K_p');
ylabel('\sigma, %');
title('Залежність перерегулювання від коефіцієнта K_p');

treg_values = [494.82 570.19 664.71 766.10 866.72 1094.8 1435.2 1888.0 2583.1 4424.2 11697];

figure;
plot(Kp_values, treg_values, '-o');
grid on;

xlabel('K_p');
ylabel('t_{рег}, c');
title('Залежність часу регулювання від коефіцієнта K_p');

est_values = [0.33898 0.20408 0.14599 0.11364 0.09302 0.07874 0.06826 0.06024 0.05391 0.04878 0.04454];

figure;
plot(Kp_values, est_values, '-o');
grid on;

xlabel('K_p');
ylabel('e_{ст}');
title('Залежність статичної помилки від коефіцієнта K_p');