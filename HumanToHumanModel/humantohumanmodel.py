from simulation import Simulation as sim
from visualization import Visualization as vz
from processingdata import ProcessingData as dt

#General simulation configuration
simulationsPeriod = 180
simulationsPopulation = 5000 #Recommendation: Population > 500 to prevent randomization errors.
simulationsCount = 3
simulationsName = "02042020_5K_180d_SDisIsoGer28d"

#How many infected humans will be injected in urban area A
casesCeroCount = 1

#Human autoisolation threshold [0;1]
autoIsolationThreshold = 0.3 #The probability of a human will auto-isolate himself when having symptoms

#Government countermeasures
startCaseCount = 150 #Number of confirmed cases needed to start government actions
actiosPeriod = 28 #Duration for government countermeasures in days
infoFactor = 1.3 #Value to represent government awareness campaigns
socialDistanceFactor = 1.5 #Value to represent control of social distance
isolationFactor = 2.0 #Value to reduce human interchange between urban areas
activeIsolation = True #Decide if a confirmed case is totally isolated by the government
lockDown = False #Decide if government close urban areas (human exchange will not exist)
testingResponse = 0.8 #The probability for a symptomatic human of being tested by the government
testingASResponse = 0.05 #The probability for a asymptomatic human of being tested by the government

#Deciding to run or not tu run government actions
runGovActions = True
govActions = [startCaseCount, actiosPeriod, infoFactor, socialDistanceFactor, isolationFactor, \
				activeIsolation, lockDown, testingResponse, testingASResponse]

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
		dt.saveConfigStart(simulationsPopulation, simulationsPeriod, simulationName, runGovActions, govActions, autoIsolationThreshold)
	s = sim(simulationsPopulation, simulationsPeriod, i + 1, casesCeroCount, simulationName, govActions, runGovActions, autoIsolationThreshold)
	vz.getFileNames(simulationName)
	vz.populationVisualization(simulationName)
	vz.simulationVisualization(simulationName, simulationsPopulation)
	vz.infectionsVisualization(simulationName)