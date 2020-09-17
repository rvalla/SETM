class GovernmentActions():
	"Government default response and contingency measures modelling"

	actionsMode = "manual"
	autoActionsTrigger = 1.0
	autoActionsOff = 0.0
	startCaseCount = 0
	actionsPeriod = 0
	bInfoFactor = 1.0
	bIsolationFactor = 1.0
	bExchangeFactor = 1.0
	bSocialDistanceFactor = 1.0
	cInfoFactor = 1.0
	cIsolationFactor = 1.0
	cExchangeFactor = 1.0
	cSocialDistanceFactor = 1.0
	testingResponseThreshold = 0.5
	testingResponseASThreshold = 0.05
	activeIsolation = False #Determine if the government strictly isolate confirmed cases
	activeTracking = False #Determine if the government isolate infected human's closed contacts
	activeTrackingThreshold = 0.0 #The probability of isolating a infected human's closed contact
	activeTrackingPressureW = 0.5 #Control How the population infected ratio affects active tracking
	bLockDown = False
	cLockDown = False
	collapseStart = 0.001 #Start age to calculate death risk factor function
	collapseEnd = 0.1 #End age to calculate death risk factor function
	collapseFactorStart = 1 #Start factor to increase death risk with age
	collapseFactorEnd = 5 #End factor to increase death risk with age. For age = 100 > 4 * Risk
	linearCollapseP = 0 #Variables to store functions coefficients
	linearCollapseO = 0
	polynomialCollapseA = 0
	polynomialCollapseB = 0
	polynomialCollapseC = 0
	
	def __init__(self):
		GovernmentActions.startCollapseVariables()
	
	#Function to return death risk increase factor due to possible medical system collapse
	def treatmentCollapseFactor(infectedPopulationRatio, type):
		r = 1.0
		if GovernmentActions.infectedPopulationRatio > GovernmentActions.collapseStart \
			and GovernmentActions.infectedPopulationRatio < GovernmentActions.collapseEnd:
			if type == "linear":
				r = GovernmentActions.infectedPopulationRatio * GovernmentActions.linearCollapseP + \
					GovernmentActions.linearCollapseO
			elif type == "polynomial":
				r = GovernmentActions.infectedPopulationRatio * GovernmentActions.infectedPopulationRatio * \
					GovernmentActions.polynomialCollapseA + GovernmentActions.infectedPopulationRatio * \
					GovernmentActions.polynomialCollapseB + GovernmentActions.polynomialCollapseC
		elif GovernmentActions.infectedPopulationRatio > GovernmentActions.collapseEnd:
			r = 5
		return r
	
	#Starting variables to store functions coefficients
	def startCollapseVariables():
		GovernmentActions.linearCollapseP = (GovernmentActions.collapseFactorEnd - GovernmentActions.collapseFactorStart)/ \
					(GovernmentActions.collapseEnd - GovernmentActions.collapseStart)
		GovernmentActions.linearCollapseO = 1 - GovernmentActions.collapseStart / \
					(GovernmentActions.collapseFactorEnd - GovernmentActions.collapseFactorStart)
		GovernmentActions.polynomialCollapseA = (GovernmentActions.collapseFactorEnd - GovernmentActions.collapseFactorStart) / \
						(GovernmentActions.collapseEnd * GovernmentActions.collapseEnd - \
						2 * GovernmentActions.collapseStart * GovernmentActions.collapseEnd + \
						GovernmentActions.collapseStart * GovernmentActions.collapseStart)
		GovernmentActions.polynomialCollapseB = (-2) * GovernmentActions.collapseStart * GovernmentActions.polynomialCollapseA
		GovernmentActions.polynomialCollapseC = GovernmentActions.collapseStart * GovernmentActions.collapseStart * \
						GovernmentActions.polynomialCollapseA + GovernmentActions.collapseFactorStart
	
	def getActiveTrackingThreshold(ipRatio):
		threshold = GovernmentActions.activeTrackingThreshold * (1 - (ipRatio * GovernmentActions.activeTrackingPressureW))
		return threshold
	
	#Method to save inicial configuration to the text file
	def saveSimulationConfig(simulationName):
		govConfig = open("SimulationData/" + simulationName + ".txt", "a")
		govConfig.write("----Government b state" + "\n")
		govConfig.write("Base info factor: " + str(GovernmentActions.bInfoFactor) + "\n")
		govConfig.write("Base isolation factor: " + str(GovernmentActions.bIsolationFactor) + "\n")
		govConfig.write("Base social distance factor: " + str(GovernmentActions.bSocialDistanceFactor) + "\n")
		govConfig.write("Testing response threshold: " + str(GovernmentActions.testingResponseThreshold) + "\n")
		govConfig.write("Testing response threshold (asymptomatic humans): " + str(GovernmentActions.testingResponseASThreshold) + "\n")
		govConfig.write("Active isolation: " + str(GovernmentActions.activeIsolation) + "\n")
		govConfig.write("Active tracking: " + str(GovernmentActions.activeTracking) + "\n")
		if activeTracking == True:
			govConfig.write("Active tracking threshold: " + str(GovernmentActions.activeTrackingThreshold) + "\n")
			govConfig.write("Active tracking pressure weight: " + str(GovernmentActions.activeTrackingPressureW) + "\n")
		govConfig.write("Health system collapse start: " + str(GovernmentActions.collapseStart) + "\n")
		govConfig.write("Health system collapse end: " + str(GovernmentActions.collapseEnd) + "\n")
		govConfig.write("Health system collapse factor start: " + str(GovernmentActions.collapseFactorStart) + "\n")
		govConfig.write("Health system collapse factor end: " + str(GovernmentActions.collapseFactorEnd) + "\n")
		govConfig.write("" + "\n")
		govConfig.close()
		
	#Method to reset government contingency measures
	def resetCountermeasures():
		GovernmentActions.cInfoFactor = GovernmentActions.bInfoFactor
		GovernmentActions.cIsolationFactor = GovernmentActions.bIsolationFactor
		GovernmentActions.cExchangeFactor = GovernmentActions.bExchangeFactor
		GovernmentActions.cSocialDistanceFactor = GovernmentActions.bSocialDistanceFactor
		GovernmentActions.cLockDown = GovernmentActions.bLockDown

	def __str__(self):
		return "----------------------------------\n" + \
				"--- SETM: Human to human model ---\n" + \
				"--- https://github/rvalla/SETM ---\n" + \
				"------- Government Actions -------\n" + \
				"Actions mode: " + GovernmentActions.actionsMode + "\n" + \
				
				
				
	autoActionsTrigger = 1.0
	autoActionsOff = 0.0
	startCaseCount = 0
	actionsPeriod = 0
	bInfoFactor = 1.0
	bIsolationFactor = 1.0
	bExchangeFactor = 1.0
	bSocialDistanceFactor = 1.0
	cInfoFactor = 1.0
	cIsolationFactor = 1.0
	cExchangeFactor = 1.0
	cSocialDistanceFactor = 1.0
	testingResponseThreshold = 0.5
	testingResponseASThreshold = 0.05
	activeIsolation = False #Determine if the government strictly isolate confirmed cases
	activeTracking = False #Determine if the government isolate infected human's closed contacts
	activeTrackingThreshold = 0.0 #The probability of isolating a infected human's closed contact
	activeTrackingPressureW = 0.5 #Control How the population infected ratio affects active tracking
	bLockDown = False
	cLockDown = False
	collapseStart = 0.001 #Start age to calculate death risk factor function
	collapseEnd = 0.1 #End age to calculate death risk factor function
	collapseFactorStart = 1 #Start factor to increase death risk with age
	collapseFactorEnd = 5 #End factor to increase death risk with age. For age = 100 > 4 * Risk
	linearCollapseP = 0 #Variables to store functions coefficients
	linearCollapseO = 0
	polynomialCollapseA = 0
	polynomialCollapseB = 0
	polynomialCollapseC = 0