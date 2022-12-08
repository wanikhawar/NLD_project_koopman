clc
clear
close all

velocity = load('velocity.dat');
pressure = load('pressure.dat');
velocity = velocity';
pressure = pressure';
velocity(abs(velocity)<1e-15) = 0;
pressure(abs(pressure)<1e-15) = 0;
[dmd_modes_v, Dv, bv, omegav, Atildev] = DMD(velocity, 20, 0.1);
[dmd_modes_p, Dp, bp, omegap, Atildep] = DMD(pressure, 20, 0.1);
rp_dmd_modes_v = real(dmd_modes_v);
rp_dmd_modes_p = real(dmd_modes_p);
rp_dmd_modes_v(abs(rp_dmd_modes_v) < 1e-15) = 0;
rp_dmd_modes_p(abs(rp_dmd_modes_p) < 1e-15) = 0;
writematrix(rp_dmd_modes_v, 'v_dmd_modes.txt')
writematrix(rp_dmd_modes_p, 'p_dmd_modes.txt')


function [Phi, D, b, omega, Atilde] = DMD(X,r,dt)

% Create DMD data matrices
X1 = X(:,1:end-1);
X2 = X(:,2:end);

[U,S,V] = svd(X1,'econ');
Ur = U(:,1:r);
Sr = S(1:r,1:r);
Vr = V(:,1:r);

% Atilde and DMD modes
Atilde = Ur'*X2*Vr/Sr;
[W,D] = eig(Atilde);
Phi = X2*(Vr/Sr)*W;

%DMD Spectra
lambda = diag(D);
omega = log(lambda)./dt;

x1 = X(:,1);
b = Phi\x1;
end
