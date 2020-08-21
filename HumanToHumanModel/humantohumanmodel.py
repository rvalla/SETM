from simulation import Simulation as sim
from visualization import Visualization as vz
from processingdata import ProcessingData as dt

#General simulation configuration
simulationsPeriod = 120
simulationsPopulation = 1000 #Recommendation: Population > 500 to prevent randomization errors.
simulationsCount = 1
simulationsName = "saraza2"

#How many infected humans will be injected in urban area A
casesCeroCount = 3

#Human autoisolation threshold [0;1]
autoIsolationThreshold = 0.0 #The probability of a human will auto-isolate himself when having symptoms
startingImmunity = 0.3 #The proportion of the population which has immunity before the outbreak
psicosis = False #Deciding if the outbreak will change humans behaivor
psicosisTrigger = 0.05 #Infected population percentage threshold which trigger psicosis factor
psicosisOff = 0.02 #Infected population percentage threshold which deactivates psicosis factor
psicosisFactor = 1.7 #Improvement of humans' habits while infected population ratio > psicosisTrigger

#Government countermeasures
govActionsMode = "normal" #Can be "normal" or "auto"
govActionsAutoTrigger =  0.03 #Decide the infected population % that triggers auto government actions.
govActionsAutoOff = 0.02 #Decide the infected population % that deactivates auto government actions.
startCaseCount = 50 #Number of confirmed cases needed to start government actions
actiosPeriod = 63 #Duration for government countermeasures in days
infoFactor = 1.3 #Value to represent government awareness campaigns
socialDistanceFactor = 1.5 #Value to represent control of social distance
isolationFactor = 2.0 #Value to reduce number of human contacts
exchangeFactor = 2.5 #Value to reduce human interchange between urban areas
activeIsolation = False #Decide if a confirmed case is totally isolated by the government
activeTracking = False #Decide if government track tested humans close contacts to test and isolate them.
activeTrackingThreshold = 0.3 #The probability for government to recognize a closed contact.
lockDown = False #Decide if government close urban areas (human exchange will not exist)
testingResponse = 0.065 #The probability for a symptomatic human of being tested by the government each day
testingASResponse = 0.02 #The probability for a asymptomatic human of being tested by the government each day

#Government countermeasures failure
govFailure = False #To set a temporarily suspension of government measures
govFailureMoment = 5 #Day since actions start in which failure occurs: < (actionsPeriod - govFailurePeriod).
govFailurePeriod = 10 #Days during the government measures are suspended

#Deciding to run or not tu run government actions
runGovActions = False
govActions = [govActionsMode, govActionsAutoTrigger, govActionsAutoOff, startCaseCount, actiosPeriod, infoFactor, \
				socialDistanceFactor, isolationFactor, exchangeFactor, activeIsolation, activeTracking, \
				activeTrackingThreshold, lockDown, testingResponse, testingASResponse]
govFailureList = [govFailure, govFailureMoment, govFailurePeriod]

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
		dt.saveConfigStart(simulationsPopulation, simulationsPeriod, simulationName, runGovActions, \
			govActions, govFailureList, autoIsolationThreshold, psicosis, psicosisTrigger, psicosisOff, psicosisFactor)
	s = sim(simulationsPopulation, simulationsPeriod, i + 1, casesCeroCount, simulationName, \
		runGovActions, govActions, govFailureList, autoIsolationThreshold, startingImmunity, psicosis, \
		psicosisTrigger, psicosisOff, psicosisFactor)
	vz.getFileNames(simulationName)
	vz.populationVisualization(simulationName)
	govActionsCycles = sim.getGovActionsCycles()
	psicosisCycles = sim.getPsicosisCycles()
	print("Building data visualization...", end="\r")
	vz.simulationVisualization(simulationName, runGovActions, govActionsCycles, psicosis, psicosisCycles, simulationsPopulation)
	vz.infectionsVisualization(simulationName, runGovActions, govActionsCycles, psicosis, psicosisCycles)
	print("Data visualization complete!     ", end="\n")
	print("", end="\n")