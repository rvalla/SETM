---
layout: index
title:  SETM
---
At the beginning of 2020 I finally decided to write code in [Python](https://www.python.org). I had nothing
special to do until *SARS-CoV-2* spread all over the world. So I propose myself to code two simple
computational models to simulate not only the spread of some disease but the effect of government contingency
measures and social behavioral changes.  
I named the project **S**imple **E**pidemic **T**ransmission **M**odels (**SETM**). There are two models
because I wanted to learn about the spread of viruses transmitted between humans and other in which some
vector take part. They are inspired in *COVID-19* and *Dengue fever* respectively.  
If you want to run your own simulations you will need *Python 3* with *Pandas* and *Matplotlib*. You can
contact me by [mail](mailto:rodrigovalla@protonmail.ch) o reach me in [telegram](https://t.me/rvalla)
or <a rel="me" href="https://fosstodon.org/@rvalla">mastodon</a>. You can read more about who I am
[here](https://rvalla.github.io/eng/aboutme_eng/). 

<p></p>
<hr class="red" />
<hr class="green" />
<hr class="blue" />
<p></p>

## Human > Human Model

The model is simple. There is a *human population* divided in two *cities*. Each *day*, the *Infected humans*
make contact with other *humans*. A series of calculations decide if they get infected or not. The *virus*
has its own characteristics and define among other things an *incubation period* and a *total illness period*.
Furthermore the *virus* define how much contagious it is, how likely is that an *infected* develops *sympthoms* and how
much *symptoms* affect the probability of infecting others. There are variables to represent such things as
how *careful* the humans are or *social distancing*.  
The *government* can take different contingency measures to stop the outbreak. These measures are triggered
by *known cases count* and not *real cases count*. Both numbers can be more or less similar depending on
*testing* strategy. The *government* can isolate *confirmed cases*, look for *closed contacts*, reduce
humans mobility or stop human exchange between *urban areas*.  
After each *simulation* all the data is saved (configuration, population, infections and outbreak data)
in [/SimulationData](https://github.com/rvalla/SETM/tree/master/HumanToHumanModel/SimulationData) folder.
Charts are automatically saved in
[/SimulationPlots](https://github.com/rvalla/SETM/tree/master/HumanToHumanModel/SimulationPlots) folder.  

### Continue reading (under construction)

Of course some details of the model has changed over time. Sometimes intending to obtain better charts and
save more data, sometimes to solve errors, sometimes to improve the algorithm. I learnt a lot while thinking
how to implement the model and writing the code and also analyzing its results. The model is simple but not
so simple. It can be useful to think about the *problem* if and only if its results are interpreted carefully.  
I share some of the results which I find interesting and ideas about implementation and modeling challenges
in a [blog](https://rvalla.github.io/SETM/eng/blog_eng).  
You will be able to read more details about the model and how it works here (remember that you can always jump
to the [code](https://github.com/rvalla/SETM)):

- How to run simulations?
- How to read the results?
- About model structure
- About the algorithm
- About extrapolation danger

<p></p>
<hr class="red" />
<hr class="green" />
<hr class="blue" />
<p></p>

## Human > Vector > Human Model

Continuous improvements in the *human>human* model have delayed my work on the model inspired by *Dengue fever*.
But eventually It will be available. A *mosquito* is very different from a *human*, has its own lifecycle.
The problem to solve is a very different one.