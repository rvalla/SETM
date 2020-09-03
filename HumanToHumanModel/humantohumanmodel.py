from simulation import Simulation as sim
from visualization import Visualization as vz
from processingdata import ProcessingData as dt

#General simulation configuration
simulationsPeriod = 360
simulationsPopulation = 10000 #Recommendation: Population > 500 to prevent randomization errors.
simulationsCount = 3
simulationsName = "02092020_10K_360d_Opt"
casesCeroCount = 5 #How many infected humans will be injected in urban area A
areaBDensity = 1.0 #Population density in area B (relative to area A)
startingImmunity = 0.0 #The proportion of the population which has immunity before the outbreak

#Control of population behavior in response to the outbreak
autoIsolationThreshold = 0.0 # [0,1] The probability of a human will auto-isolate himself when having symptoms
behavior = True #Deciding if the outbreak will change humans behavior
behaviorTrigger = 0.004 # [0,1] Infected population percentage threshold which trigger behavior factor
behaviorOff = 0.002 # [0,1] Infected population percentage threshold which deactivates behavior factor
behaviorFactor = 1.25 # [1,inf) Improvement of humans' habits while infected population ratio > behaviorTrigger

#Government default response
activeIsolation = True #Decide if a confirmed case is totally isolated by the government
activeTracking = True #Decide if government track tested humans close contacts to test and isolate them.
activeTrackingThreshold = 0.15 # [0,1] The probability for government to recognize a closed contact.
activeTrackingPressureW = 1.0 # [0,inf) Control How the population infected ratio affects active tracking
testingResponse = 0.056 # [0,1] The probability for a symptomatic human of being tested by the government each day
testingASResponse = 0.005 # [0,1] The probability for a asymptomatic human of being tested by the government each day

#Government countermeasures
govActionsMode = "normal" #Can be "normal" or "auto"
govActionsAutoTrigger =  0.004 # [0,1] Decide the infected population % that triggers auto government actions.
govActionsAutoOff = 0.002 # [0,1] Decide the infected population % that deactivates auto government actions.
startCaseCount = 50 # [1,population) Number of confirmed cases needed to start government actions
actionsPeriod = 28 # [1, period) Duration for government countermeasures in days
infoFactor = 1.1 # (1, inf) Value to represent government awareness campaigns
socialDistanceFactor = 1.25 # (1,inf) Value to represent control of social distance
isolationFactor = 1.5 # (1,inf) Value to reduce number of human contacts
exchangeFactor = 1.75 # (1,inf) Value to reduce human interchange between urban areas
lockDown = False #Decide if government close urban areas (human exchange will not exist)

#Government countermeasures failure
govFailure = False #To set a temporarily suspension of government measures
govFailureMoment = 14 # [1, actionsPeriod) Day since actions start in which failure occurs: < (actionsPeriod - govFailurePeriod).
govFailurePeriod = 5 # [1, actionsPeriod - govFailureMoment) Days during the government measures are suspended

#Deciding to run or not tu run government actions
runGovActions = True
govActions = [govActionsMode, govActionsAutoTrigger, govActionsAutoOff, startCaseCount, actionsPeriod, infoFactor, \
				socialDistanceFactor, isolationFactor, exchangeFactor, lockDown, activeIsolation, activeTracking, \
				activeTrackingThreshold, activeTrackingPressureW, testingResponse, testingASResponse]
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
		dt.saveConfigStart(simulationsPopulation, simulationsPeriod, simulationName, areaBDensity, runGovActions, \
			govActions, govFailureList, autoIsolationThreshold, startingImmunity, behavior, behaviorTrigger, \
			behaviorOff, behaviorFactor)
	s = sim(simulationsPopulation, simulationsPeriod, i + 1, casesCeroCount, simulationName, areaBDensity, \
		runGovActions, govActions, govFailureList, autoIsolationThreshold, startingImmunity, behavior, \
		behaviorTrigger, behaviorOff, behaviorFactor)
	vz.getFileNames(simulationName)
	vz.populationVisualization(simulationName)
	govActionsCycles = sim.getGovActionsCycles()
	behaviorCycles = sim.getBehaviorCycles()
	print("Building data visualization...", end="\r")
	vz.simulationVisualization(simulationName, runGovActions, govActionsCycles, behavior, behaviorCycles, simulationsPopulation)
	vz.infectionsVisualization(simulationName, simulationsPeriod, runGovActions, govActionsCycles, behavior, behaviorCycles)
	print("Data visualization complete!     ", end="\n")
	print("", end="\n")