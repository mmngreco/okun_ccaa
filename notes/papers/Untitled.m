T = length(y);
figure
plot(y/1000)
h1 = gca;
h1.XLim = [0,T];
h1.XTick = 1:12:T;
title 'Monthly Accidental Deaths';
ylabel 'Number of Deaths (in thousands)';
hold on

t = (1:T)';
X = [ones(T,1) t t.^2];

b = X\y;
tH = X*b;

h2 = plot(tH/1000,'r','LineWidth',2);
legend(h2,'Quadratic Trend Estimate')
hold off
xtx = y - tH;

[xthpt,xthp] = hpfilter(y)

xtbk=bpf(y,1,1,2)