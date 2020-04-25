clear all
close all

root   = ['/Users/antonio/Dropbox/BSL/CRSMEX/Dendrograms/2019JUN11/sequence_xc9500_coh9500/sequence_00055_N08/'];
input  = [root 'inversion.dat'];
locmag = [root 'locmag_mean.dat'];
ds_lim = 100e6;

inversion = load(input);
loc       = load(locmag);
plot(inversion(:,1),inversion(:,2),'kp','MarkerSize',18,'LineWidth',2,'MarkerFaceColor','y')
hold on

Mo    = 10^(1.5*loc(4)+9.1);
r_max = ((7/16)*Mo/ds_lim)^(1/3)
N     = size(inversion,1);

for i=1:N
    circle(inversion(i,1),inversion(i,2),r_max)
    if i ~= N
        plot([inversion(i,1) inversion(i+1,1)],[inversion(i,2) inversion(i+1,2)],'k')
    else
        plot([inversion(N,1) inversion(1,1)],[inversion(N,2) inversion(1,2)],'k')
    end
end
fontsize(18)
grid minor
axis equal
setw

function circle(x,y,r)
%x and y are the coordinates of the center of the circle
%r is the radius of the circle
%0.01 is the angle step, bigger values will draw the circle faster but
%you might notice imperfections (not very smooth)
ang=0:0.01:2*pi; 
xp=r*cos(ang);
yp=r*sin(ang);
plot(x+xp,y+yp,'LineWidth',2);
end


