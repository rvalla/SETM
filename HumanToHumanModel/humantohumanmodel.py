from simulation import Simulation as sim
from visualization import Visualization as vz

print("#################################")
print("SIMPLE EPIDEMIC TRANSMISION MODEL")
print("Human to human disease simulation")
print("---------------------------------")
print("---https://github/rvalla/SETM----")
print("#################################")

simulationsPeriod = 120
simulationsPopulation = 2000
simulationsCount = 1
simulationName = "28032020_2K_120d_03_SDisIso"

#Government countermeasures
#Passing the values for government actions in order:
#startCaseCount, actionsPeriod, infoFactor, isolationFactor, socialDistanceFactor,
#	activeIsolation, lockDown, testing, testingAS

casesCeroCount = 1
runGovActions = True
govActions = [10, 56, 1.3, 2.0, 2.5, False, False, 0.5, 0.05]

startConfig = open("SimulationData/" + simulationName + ".txt", "a")
startConfig.write("#################################" + "\n")
startConfig.write("SIMPLE EPIDEMIC TRANSMISION MODEL" + "\n")
startConfig.write("Human to human disease simulation" + "\n")
startConfig.write("---------------------------------" + "\n")
startConfig.write("---https://github/rvalla/SETM----" + "\n")
startConfig.write("#################################" + "\n")
startConfig.write("" + "\n")
startConfig.write(simulationName + "\n")
startConfig.write("Population: " + str(simulationsPopulation) + "\n")
startConfig.write("Period in days: " + str(simulationsPeriod) + "\n")
startConfig.write("" + "\n")
if runGovActions == True:
	startConfig.write("----Goverment actions" + "\n")
	startConfig.write("startCaseCount: " + str(govActions[0]) + "\n")
	startConfig.write("actionsPeriod: " + str(govActions[1]) + "\n")
	startConfig.write("infoFactor: " + str(govActions[2]) + "\n")
	startConfig.write("isolationFactor: " + str(govActions[3]) + "\n")
	startConfig.write("socialDistanceFactor: " + str(govActions[4]) + "\n")
	startConfig.write("activeIsolation: " + str(govActions[5]) + "\n")
	startConfig.write("lockDown: " + str(govActions[6]) + "\n")
	startConfig.write("testingResponseFactor: " + str(govActions[7]) + "\n")
	startConfig.write("testingResponseASFactor: " + str(govActions[8]) + "\n")
	startConfig.write("" + "\n")
startConfig.close()

for i in range(simulationsCount):
	print("", end="\n")
	print("Starting simulation number " + str(i + 1), end="\n")
	simulationCName = simulationName
	if simulationsCount > 1:
		simulationCName = simulationName + "_" + str(i)
	s = sim(simulationsPopulation, simulationsPeriod, casesCeroCount, simulationCName, govActions, runGovActions)
	vz.populationVisualization(simulationCName)
	vz.simulationVisualization(simulationCName)