from simulation import Simulation as sim
from visualization import Visualization as vz
from processingdata import ProcessingData as dt

#General simulation configuration
simulationsPeriod = 180
simulationsPopulation = 3000 #Recommendation: Population > 500 to prevent randomization errors.
simulationsCount = 1
simulationsName = "25042020_3K_180d_GovPsi"

#How many infected humans will be injected in urban area A
casesCeroCount = 3

#Human autoisolation threshold [0;1]
autoIsolationThreshold = 0.0 #The probability of a human will auto-isolate himself when having symptoms
psicosis = True #Deciding if the outbreak will change humans behaivor
psicosisThreshold = 0.03 #Infected population percentage threshold which trigger psicosis factor
psicosisFactor = 1.7 #Improvement of humans' habits while infected population ratio > psicosisThreshold

#Government countermeasures
startCaseCount = 50 #Number of confirmed cases needed to start government actions
actiosPeriod = 56 #Duration for government countermeasures in days
infoFactor = 1.2 #Value to represent government awareness campaigns
socialDistanceFactor = 1.5 #Value to represent control of social distance
isolationFactor = 2.0 #Value to reduce human interchange between urban areas
activeIsolation = False #Decide if a confirmed case is totally isolated by the government
lockDown = False #Decide if government close urban areas (human exchange will not exist)
testingResponse = 0.5 #The probability for a symptomatic human of being tested by the government
testingASResponse = 0.05 #The probability for a asymptomatic human of being tested by the government
govFailure = True #To set a temporarily suspension of government measures
govFailureMoment = 10 #Day since actions start in which failure occurs: < (actionsPeriod - govFailurePeriod).
govFailurePeriod = 3 #Days during the government measures are suspended

#Deciding to run or not tu run government actions
runGovActions = True
govActions = [startCaseCount, actiosPeriod, infoFactor, socialDistanceFactor, isolationFactor, \
				activeIsolation, lockDown, testingResponse, testingASResponse, govFailure, \
				govFailureMoment, govFailurePeriod]

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
			govActions, autoIsolationThreshold, psicosis, psicosisThreshold, psicosisFactor)
	s = sim(simulationsPopulation, simulationsPeriod, i + 1, casesCeroCount, simulationName, \
		govActions, runGovActions, autoIsolationThreshold, psicosis, psicosisThreshold, psicosisFactor)
	vz.getFileNames(simulationName)
	vz.populationVisualization(simulationName)
	govStart = sim.getGovActionsStartDay()
	govEnd = sim.getGovActionsEndDay()
	govFailureS = sim.getGovActionsFailure()
	govFailureP = sim.getGovActionsFailurePeriod()
	psicosisCycles = sim.getPsicosisCycles()
	vz.simulationVisualization(simulationName, simulationsPopulation, runGovActions, govFailure, \
		govStart, govEnd, govFailureS, govFailureP, psicosis, psicosisCycles)
	vz.infectionsVisualization(simulationName)