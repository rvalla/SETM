"Store values to simulate goverment countermeasures"
startDay = 0
endDay = 0
baseInfoFactor = 1.0
baseIsolationFactor = 1.0
baseSocialDistanceFactor = 1.0
baseTestingFactor = 0.5
baseTestingASFactor = 0.05
currentInfoFactor = 1.0
currentIsolationFactor = 1.0
currentSocialDistanceFactor = 1.0
testingResponseFactor = 0.5
testingResponseASFactor = 0.05
lockDown = False
colapseStart = 0.001 #Start age to calculate death risk factor function
colapseEnd = 0.2 #End age to calculate death risk factor function
colapseFactorStart = 1 #Start factor to increase death risk with age
colapseFactorEnd = 5 #End factor to increase death risk with age. For age = 100 > 4 * Risk
linearColapseP = 0 #Variables to store functions coefficients
linearColapseO = 0
polynomialColapseA = 0
polynomialColapseB = 0
polynomialColapseC = 0

class GovermentActions():
	
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
	
	def setStartDay(day):
		global startDay
		startDay = day
	
	def getStartDay():
		return startDay
	
	def setEndDay(day):
		global endDay
		endDay = day
	
	def getEndDay():
		return endDay
	
	def setInfoFactor(factor):
		global currentInfoFactor
		currentInfoFactor = factor
	
	def getInfoFactor():
		return currentInfoFactor
	
	def setIsolationFactor(factor):
		global currentIsolationFactor
		currentIsolationFactor = factor
	
	def getSocialDistanceFactor():
		return currentSocialDistanceFactor
	
	def setSocialDistanceFactor(factor):
		global currentSocialDistanceFactor
		currentSocialDistanceFactor = factor
	
	def getIsolationFactor():
		return currentIsolationFactor
	
	def setLockDown(status):
		global lockDown
		lockDown = status
	
	def getLockDown():
		return lockDown
	
	def setTestingResponseFactor(factor):
		global testingResponseFactor
		testingResponseFactor = factor
	
	def getTestingResponseFactor():
		return testingResponseFactor
		
	def setTestingResponseASFactor(factor):
		global testingResponseASFactor
		testingResponseASFactor = factor
	
	def getTestingResponseASFactor():
		return testingResponseASFactor
			
	def resetCountermeasures():
		global currentInfoFactor
		currentInfoFactor = baseInfoFactor
		global currentIsolationFactor
		currentIsolationFactor = baseIsolationFactor
		global currentSocialDistanceFactor
		currentSocialDistanceFactor = baseSocialDistanceFactor
		global lockDown
		lockDown = False
		global testingResponseFactor
		testingResponseFactor = baseTestingFactor
		global testingResponseASFactor
		testingResponseASFactor = baseTestingASFactor