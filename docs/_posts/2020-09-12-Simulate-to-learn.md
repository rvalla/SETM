---
layout: post_eng
title:  Simulate to learn
category: general
tags: english simulation "computational model"
---
There is nothing I like more than to learn new things. It makes me feel active and awake. When I say new things
I am talking about really new things. I have never paid attention to epidemic transmission dynamics but in 2020
I had reasons to do it. While monitoring the *Dengue* outbreak in Argentina first cases of *COVID-19* were
confirmed.  
Immediately newspapers got full of news and hundreds of experts start talking about what to do and what not to
do. They did it as, in the world, all were disconnected. Economists were talking about saving the economy and
epidemiologists like it was possible to stay at home during 60 days. I changed my information sources very fast
of course. Today is possible to make contact with a lot of people instantly so I started following on *twitter*  
those who helped me to stay tuned and make sense about a lot of problems around the *COVID-19* pandemic.  
But the future does not exist. And when things are so dynamic and reactions of governments and people interact
with a virus, you never know what to expect.  
So I complemented my reading about *SARS-CoV-2*, *COVID-19* and different *contingency measures* with a
computational model which allowed me to question myself about the outbreak and the effects of different 
social responses in its evolution. I learnt a lot about the problem and I was surprised sometimes by the 
results.

![chart](https://rvalla.github.io/SETM/assets/img/2020-09-12-Simular-para-aprender.png)
> Para poder leer rápido los resultados trabajé mucho en los gráficos automáticos que se crean después
de cada simulación.

I said I enjoy to learn new things so I coded the software in [Python](https://www.python.org). A programming
language I had not used a lot. The main goal was always to make a model which serves to study a dynamic problem
so I designed it in a way which allows me to make a lot of changes. The firsts runs could only simulate
mobility reductions of the population in certain period of time. Now it is possible to simulate things as
the social response to the outbreak (changing how much careful the population is) or isolation of *closed
contacts* of *confirmed cases*.  
Since today I will try to write a more complete and clear documentation for curious people like me who wants
to run simulations or analyse the results without needing to study the code. Perhaps they find out something
that until now has eluded me.