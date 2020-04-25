clear all
close all

Mw = 2:0.1:4.5;
M0 = 10.^(1.5*Mw + 9.1);

ds = linspace(10e6,10e7,10);  % Stress drop



figure()
hold on

for k = 1:numel(ds)
    r = (7/16)*(M0./ds(k)).^(1/3);
    
    plot(Mw,r,'Linewidth',Mw(k)/2,'Color',hsv2rgb([0.8*((ds(k)-min(ds)))/(max(ds)-min(ds)),1,1]))
end
grid
fontsize(18)
xlabel('Magnitude')
ylabel('Radius [m]')
setw

ds = 10e6;
r = (7/16)*(M0./ds).^(1/3);
plot(Mw,r,'r','Linewidth',Mw(k)/2)
return

r  = (7/16)*(M0./ds).^(1/3);


subplot(2,1,1)
semilogy(Mw,M0,'k','LineWidth',3)
grid

subplot(2,1,2)

for k=1:numel(r)
    circle(0,0,r(k))
end
axis equal