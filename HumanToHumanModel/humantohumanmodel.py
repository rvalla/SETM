from processingdata import ProcessingData as dt
from simulation import Simulation as sim
from visualization import Visualization as vz

print("#################################")
print("SIMPLE EPIDEMIC TRANSMISION MODEL")
print("Human to human disease simulation")
print("---------------------------------")
print("---https://github/rvalla/SETM----")
print("#################################")

simulationsPeriod = 60
simulationsPopulation = 1000
simulationsCount = 1
simulationName = "26032020_testing_"

#Government countermeasures
#Passing the values for government actions in order:
#startDay, endDay, infoFactor, isolationFactor, socialDistanceFactor, lockDown, testing, testingAS

govActions = [15, 45, 1.3, 1.7, 1.3, False, 0.5, 0.05]

for i in range(simulationsCount):
	simulationCName = simulationName + str(i)
	s = sim(simulationsPopulation, simulationsPeriod, simulationCName, govActions, True)
	vz.populationVisualization(simulationCName)
	vz.simulationVisualization(simulationCName)