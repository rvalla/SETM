"Variables to control government default response and simulate countermeasures"
actionsMode = "manual"
autoActionsTrigger = 1.0
autoActionsOff = 0.0
startCaseCount = 0
actionsPeriod = 0
baseInfoFactor = 1.0
baseIsolationFactor = 1.0
baseExchangeFactor = 1.0
baseSocialDistanceFactor = 1.0
currentInfoFactor = 1.0
currentIsolationFactor = 1.0
currentExchangeFactor = 1.0
currentSocialDistanceFactor = 1.0
testingResponseThreshold = 0.5
testingResponseASThreshold = 0.05
activeIsolation = False #Determine if the government strictly isolate confirmed cases
activeTracking = False #Determine if the government isolate infected human's closed contacts
activeTrackingThreshold = 0.0 #The probability of isolating a infected human's closed contact
activeTrackingPressureW = 0.5 #Control How the population infected ratio affects active tracking
lockDown = False
colapseStart = 0.001 #Start age to calculate death risk factor function
colapseEnd = 0.1 #End age to calculate death risk factor function
colapseFactorStart = 1 #Start factor to increase death risk with age
colapseFactorEnd = 5 #End factor to increase death risk with age. For age = 100 > 4 * Risk
linearColapseP = 0 #Variables to store functions coefficients
linearColapseO = 0
polynomialColapseA = 0
polynomialColapseB = 0
polynomialColapseC = 0

class GovernmentActions():
	
	#Function to return death risk increase factor due to possible medical system colapse
	def treatmentColapseFactor(infectedPopulationRatio, type):
		r = 1.0
		if infectedPopulationRatio > colapseStart and infectedPopulationRatio < colapseEnd:
			if type == "linear":
				r = infectedPopulationRatio * linearColapseP + linearColapseO
			elif type == "polynomial":
				r = infectedPopulationRatio * infectedPopulationRatio * polynomialColapseA + \
				infectedPopulationRatio * polynomialColapseB + polynomialColapseC
		elif infectedPopulationRatio > colapseEnd:
			r = 5
		return r
	
	#Starting variables to store functions coefficients
	def startColapseVariables():
		global linearColapseP
		linearColapseP = (colapseFactorEnd - colapseFactorStart)/ \
					(colapseEnd - colapseStart)
		global linearColapseO
		linearColapseO = 1 - colapseStart / \
					(colapseFactorEnd - colapseFactorStart)
		global polynomialColapseA
		polynomialColapseA = (colapseFactorEnd - colapseFactorStart) / \
						(colapseEnd * colapseEnd - \
						2 * colapseStart * colapseEnd + \
						colapseStart * colapseStart)
		global polynomialColapseB
		polynomialColapseB = (-2) * colapseStart * polynomialColapseA
		global polynomialColapseC
		polynomialColapseC = colapseStart * colapseStart * \
						polynomialColapseA + colapseFactorStart
	
	def setActionsMode(status):
		global actionsMode
		actionsMode = status
	
	def getActionsMode():
		return actionsMode
	
	def setAutoActionsTrigger(threshold):
		global autoActionsTrigger
		autoActionsTrigger = threshold
	
	def getAutoActionsTrigger():
		return autoActionsTrigger
	
	def setAutoActionsOff(threshold):
		global autoActionsOff
		autoActionsOff = threshold
	
	def getAutoActionsOff():
		return autoActionsOff
	
	def setStartCaseCount(day):
		global startCaseCount
		startCaseCount = day
	
	def getStartCaseCount():
		return startCaseCount
	
	def setActionsPeriod(day):
		global actionsPeriod
		actionsPeriod = day
	
	def getActionsPeriod():
		return actionsPeriod
	
	def setInfoFactor(factor):
		global currentInfoFactor
		currentInfoFactor = factor
	
	def getInfoFactor():
		return currentInfoFactor
	
	def setIsolationFactor(factor):
		global currentIsolationFactor
		currentIsolationFactor = factor
	
	def getIsolationFactor():
		return currentIsolationFactor
	
	def setSocialDistanceFactor(factor):
		global currentSocialDistanceFactor
		currentSocialDistanceFactor = factor
	
	def getSocialDistanceFactor():
		return currentSocialDistanceFactor
	
	def setExchangeFactor(factor):
		global currentExchangeFactor
		currentExchangeFactor = factor
	
	def getExchangeFactor():
		return currentExchangeFactor
	
	def setLockDown(status):
		global lockDown
		lockDown = status
	
	def getLockDown():
		return lockDown
	
	def setActiveIsolation(status):
		global activeIsolation
		activeIsolation = status
	
	def getActiveIsolation():
		return activeIsolation
	
	def setActiveTracking(status):
		global activeTracking
		activeTracking = status
	
	def getActiveTracking():
		return activeTracking
	
	def setActiveTrackingThreshold(threshold):
		global activeTrackingThreshold
		activeTrackingThreshold = threshold
	
	def getActiveTrackingThreshold(ipRatio):
		threshold = activeTrackingThreshold * (1 - (ipRatio * activeTrackingPressureW))
		return threshold
	
	def setActiveTrackingPressureW(weight):
		global activeTrackingPressureW
		activeTrackingPressureW = weight
	
	def getActiveTrackingPressureW():
		return activeTrackingPressureW
	
	def setTestingResponseThreshold(threshold):
		global testingResponseThreshold
		testingResponseThreshold = threshold
	
	def getTestingResponseThreshold():
		return testingResponseThreshold
		
	def setTestingResponseASThreshold(threshold):
		global testingResponseASThreshold
		testingResponseASThreshold = threshold
	
	def getTestingResponseASThreshold():
		return testingResponseASThreshold
	
	#Method to save inicial data to text file
	def saveSimulationConfig(simulationName):
		govConfig = open("SimulationData/" + simulationName + ".txt", "a")
		govConfig.write("----Government base state" + "\n")
		govConfig.write("Base info factor: " + str(baseInfoFactor) + "\n")
		govConfig.write("Base isolation factor: " + str(baseIsolationFactor) + "\n")
		govConfig.write("Base social distance factor: " + str(baseSocialDistanceFactor) + "\n")
		govConfig.write("Testing response threshold: " + str(testingResponseThreshold) + "\n")
		govConfig.write("Testing response threshold (asymptomatic humans): " + str(testingResponseASThreshold) + "\n")
		govConfig.write("Active isolation: " + str(activeIsolation) + "\n")
		govConfig.write("Active tracking: " + str(activeTracking) + "\n")
		if activeTracking == True:
			govConfig.write("Active tracking threshold: " + str(activeTrackingThreshold) + "\n")
			govConfig.write("Active tracking pressure weight: " + str(activeTrackingPressureW) + "\n")
		govConfig.write("Health system colapse start: " + str(colapseStart) + "\n")
		govConfig.write("Health system colapse end: " + str(colapseEnd) + "\n")
		govConfig.write("Health system colapse factor start: " + str(colapseFactorStart) + "\n")
		govConfig.write("Health system colapse factor end: " + str(colapseFactorEnd) + "\n")
		govConfig.write("" + "\n")
		govConfig.close()
		
	#Method to reset government countermeasures
	def resetCountermeasures():
		global currentInfoFactor
		currentInfoFactor = baseInfoFactor
		global currentIsolationFactor
		currentIsolationFactor = baseIsolationFactor
		global currentExchangeFactor
		currentExchangeFactor = baseExchangeFactor
		global currentSocialDistanceFactor
		currentSocialDistanceFactor = baseSocialDistanceFactor
		global lockDown
		lockDown = False