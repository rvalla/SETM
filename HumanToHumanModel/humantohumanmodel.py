from simulation import Simulation as sim
from visualization import Visualization as vz

print("#################################")
print("SIMPLE EPIDEMIC TRANSMISION MODEL")
print("Human to human disease simulation")
print("---------------------------------")
print("---https://github/rvalla/SETM----")
print("#################################")

simulationsPeriod = 120
simulationsPopulation = 1000
simulationsCount = 1
simulationName = "27032020_testing_GovLocDown"

#Government countermeasures
#Passing the values for government actions in order:
#startCaseCount, actionsPeriod, infoFactor, isolationFactor, socialDistanceFactor,
#	activeIsolation, lockDown, testing, testingAS


runGovActions = False
govActions = [10, 60, 1.3, 2.0, 1.2, False, True, 0.8, 0.3]

for i in range(simulationsCount):
	simulationCName = simulationName
	if simulationsCount > 1:
		simulationCName = simulationName + "_" + str(i)
	s = sim(simulationsPopulation, simulationsPeriod, simulationCName, govActions, runGovActions)
	vz.populationVisualization(simulationCName)
	vz.simulationVisualization(simulationCName)