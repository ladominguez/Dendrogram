clear all
close all

beta = 3600;
kappa= 0.32;

Mw   = 2.0:0.5:4.5;
M0   = 10.^(1.5.*Mw +9.1);
f    = linspace(1,25,101);

Adata = [   0.78   0.0602472969295
 1.56   0.0580813223329
 2.34   0.0614612335256
 3.12   0.0490407943659
 3.91   0.0479599115564
 4.69   0.03636100284
 5.47   0.0262481423362
 6.25   0.0209177617996
 7.03   0.0167386476457
 7.81   0.016055028011
 8.59   0.00879657923076
 9.38   0.00878081147472
10.16   0.00730129743722
10.94   0.00604203280711
11.72   0.00686270613049
12.50   0.00650320043422
13.28   0.00508956008206
14.06   0.00411497905699
14.84   0.00340780983626
];

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
f    = linspace(0,50,101);
fc   = [1 2 3 4];

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
legend('fc=1Hz', 'fc=2Hz','fc=3Hz','fc=4Hz')
grid()

subplot(1,3,2)
legend('fc=1Hz', 'fc=2Hz','fc=3Hz','fc=4Hz')
grid()

subplot(1,3,1)
legend('fc=1Hz', 'fc=2Hz','fc=3Hz','fc=4Hz')
grid()

plot(Adata(:,1),Adata(:,2),'ko-')