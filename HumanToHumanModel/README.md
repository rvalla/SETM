# Simple Epidemic Transmission Models

### Simulating the spread of a human to human transmitted virus

This a model to simulate the effect from actions taken by the authorities in case of
an epidemic outbreak. Is inspired in **COVID-19** pandemic, but you can adapt the variables to represent
another contagious desease.</br>

#### humantohumanmodel.py
You can run a certain number of simulations adapting the code of *humantohumanmodel.py* simply
by specifying among others:
* Population size
* Number of days to simulate
* Number or simulations
* File name for exported data
* Number of infected humans to start the outbreak
* Government actions list

#### simulation.py
The code that actually run the simulation. You can not set anything in it, unless you want to change
the simulation algorithm. It starts setting some global variables and saving the data to a text file
in which all the important variables will be saved to allow a critic analysis of the results. Then
the population is created and simulation starts.</br>
There are two different lists of *humans* to represent two cities in the simulated country. Each day,
the infected humans make contact with their family members and an aleatory contact list. Some of them may
be infected.</br>
The evolution state of the simulation is saved to a *csv* file as well as the population and infections
data. General plots to display population data and simulation evolution will be saved automatically.

#### human.py
You could edit some human's characteristics directly on *human.py*, although its atributes will
be overide by *simulation.py* when population is created.

#### virus.py
The place where you can change the virus characteristics. You can use them to change how contagious
the virus is, its base death rate, how many infected humans will have symptoms or need treatment,
and more.

#### government.py
The place where the variables to manage contingency measures are saved. You can edit most of them in
*humantohumanmodel.py*. Take into account thar some of the variables are fixed during all the simulations
while some of them change when the contingency measures occurred.

#### randomization.py
The place where you can edit the probabilistic distribution of some of the atributes (population age
distribution, incubation periods and illness periods distribution).

#### processingdata.py
Some code to process and save the data correctly.

#### visualization.py
Some code to plot results automatically.

Contact [rodrigovalla[at]protonmail.ch](mailto:rodrigovalla@protonmail.ch)