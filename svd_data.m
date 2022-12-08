clc
clear
close all

% load data
velocity = load('velocity.dat');
pressure = load('pressure.dat');

%%
% transpose the data to get each snapshot as a column vector
velocity = velocity';
pressure = pressure';

%%
% determine the mean of the quanitity under consideration
mean_vel = mean(velocity,2);
mean_pres = mean(pressure,2);

% determine the dynamic part of the quantity
dynamic_vel = velocity - repmat(mean_vel, 1, 500);
dynamic_pres = pressure - repmat(mean_pres, 1, 500);

% set the values below the tolerance as zero to avoid precision errors
dynamic_vel(abs(dynamic_vel) < 1e-15) = 0;
dynamic_pres(abs(dynamic_pres) < 1e-15) = 0;

% Perform SVD on the data
[Uv,Sv,Vv] = svd(dynamic_vel,"econ");
[Up,Sp,Vp] = svd(dynamic_pres,"econ");

% Write the first n modes to the files
Uvr = Uv(:,1:10);
Upr = Up(:,1:10);
writematrix(Uvr, 'v_pod_modes.txt')
writematrix(Upr, 'p_pod_modes.txt')


% Plot the energy content of the modes
eig_v = diag(Sv);
eig_p = diag(Sp);

energy_v = zeros(1,10);
energy_p = zeros(1,10);
n = zeros(1,11);

for i = 1:11
    n(i) = i-1;
    energy_p(i) = sum(eig_p(1:i-1))/sum(eig_p);
    energy_v(i) = sum(eig_v(1:i-1))/sum(eig_v);
end

figure(1)
plot(n, energy_v)

figure(2)
plot(n, energy_p)


