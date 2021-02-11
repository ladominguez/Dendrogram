clear all
close all

beta = 3600;
kappa= 0.32;

Mw   = 2.0:0.5:4.5;
M0   = 10.^(1.5.*Mw +9.1);
f    = linspace(1,25,101);

figure

for k = 1:numel(M0)
    stress =  (M0(k)*(7/16)*(f/(kappa*beta)).^3)/1e6;
    fc(k)  =  ((16/7)*3e6/M0(k))^(1/3)*kappa*beta;
    semilogy(f,stress,'linewidth',3)
    hold all
    plot(fc(k),3,'kp','markersize',14, 'handlevisibility','off','MarkerFaceColor','r')
end
legend(['Mw=' num2str(Mw(1))], ['Mw=' num2str(Mw(2))], ['Mw=' num2str(Mw(3))],['Mw=' num2str(Mw(4))], ['Mw=' num2str(Mw(5))],['Mw=' num2str(Mw(6))])
%legend(['Mw=' num2str(Mw(1))], ['Mw=' num2str(Mw(2))], ['Mw=' num2str(Mw(3))],['Mw=' num2str(Mw(4))])
xlabel('f_c[Hz]')
ylabel('\Delta\sigma[MPa]')
fontsize(14)
grid

figure
setwin([86 241 1188 516])
f    = linspace(1,50,101);
fc   = [1 5 10 15];

for k = 1:numel(fc)
    subplot(1,3,1)
    loglog(f,1./(1+(f/fc(k)).^2), 'linewidth',2)
    hold all
    subplot(1,3,2)
    loglog(f,2*pi*f./(1+(f/fc(k)).^2), 'linewidth',2)
    hold all
    subplot(1,3,3)
    loglog(f,(2*pi*f).^2./(1+(f/fc(k)).^2), 'linewidth',2)
    hold all
end
subplot(1,3,1)
legend('fc=1Hz', 'fc=5Hz','fc=10Hz','fc=15Hz')
grid()

subplot(1,3,2)
legend('fc=1Hz', 'fc=5Hz','fc=10Hz','fc=15Hz')
grid()

subplot(1,3,3)
legend('fc=1Hz', 'fc=5Hz','fc=10Hz','fc=15Hz')
grid()