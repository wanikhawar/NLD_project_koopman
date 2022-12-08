clc
clear

t = linspace(0,10,100);
f0 = ones(length(t));
f1 = exp(-1.5118e-10*t).*cos(3.4119*t);
f2 = exp(-0.0001*t).*cos(6.8238*t);
f3 = exp(-0.0002*t).*cos(10.2357*t);
f4 = exp(-0.0003*t).*cos(13.6476*t);

figure(1)
plot(t,f0,'k-','linewidth',5)
xlabel("t")
ylabel("Mode Magnitude")
set(gca,"xtick",[],'ytick',[],'fontsize',22)

% figure(2)
% plot(t,f1,'k-','linewidth',5)
% xlabel("t")
% ylabel("Mode Magnitude")
% set(gca,"xtick",[],'ytick',[],'fontsize',22)
% 
% figure(3)
% plot(t,f2,'k-','linewidth',5)
% xlabel("t")
% ylabel("Mode Magnitude")
% set(gca,"xtick",[],'ytick',[],'fontsize',22)
% 
% figure(4)
% plot(t,f3,'k-','linewidth',5)
% xlabel("t")
% ylabel("Mode Magnitude")
% set(gca,"xtick",[],'ytick',[],'fontsize',22)
% 
% figure(5)
% plot(t,f4,'k-','linewidth',5)
% xlabel("t")
% ylabel("Mode Magnitude")
% set(gca,"xtick",[],'ytick',[],'fontsize',22)
