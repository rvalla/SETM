from simulation import Simulation as sim
from visualization import Visualization as vz
from processingdata import ProcessingData as dt

#General simulation configuration
simulationsPeriod = 120
simulationsPopulation = 3000 #Recommendation: Population > 500 to prevent randomization errors.
simulationsCount = 3
simulationsName = "29032020_3K_120d_SDisIso42dless"

#Government countermeasures
#Passing the values for government actions in order:
#startCaseCount, actionsPeriod, infoFactor, isolationFactor, socialDistanceFactor,
#	activeIsolation, lockDown, testing, testingAS

casesCeroCount = 1
runGovActions = True
govActions = [10, 42, 1.3, 1.7, 2.0, False, False, 0.5, 0.05]


print("#################################")
print("SIMPLE EPIDEMIC TRANSMISION MODEL")
print("Human to human disease simulation")
print("---------------------------------")
print("---https://github/rvalla/SETM----")
print("#################################")
		
#Running desired number of simulations...
for i in range(simulationsCount):
	print("", end="\n")
	print("Starting simulation number " + str(i + 1), end="\n")
	simulationName = simulationsName
	simulationName = simulationsName + "_" + str(i)
	if i == 0:
		dt.saveConfigStart(simulationsPopulation, simulationsPeriod, simulationName, runGovActions, govActions)
	s = sim(simulationsPopulation, simulationsPeriod, i + 1, casesCeroCount, simulationName, govActions, runGovActions)
	vz.populationVisualization(simulationName)
	vz.simulationVisualization(simulationName)