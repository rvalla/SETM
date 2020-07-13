baseInfectionThreshold = 0.2 #How contagious the virus is
baseASContagiousFactor = 0.2 #Contagious factor in absence of symptoms
baseSymptomsThreshold = 0.4 #Probability of having symptoms
baseTreatmentThreshold = 0.2 #Probability of needing treatment
baseFutureImmunity = 1.0 #Probability of being inmune after infection
contagiousShift = 0 #Days offset between mosto contagious face and symptoms
baseDeathRate = 0.4 #Base death rate for patients who needed treatment
deathRiskSymptomsWeight = 0.7 #The probability of been symptomatic is related to death risk
deathRiskTreatmentWeight = 0.6 #The probability of need treatment is related to death risk
riskFunctionStart = 30 #Start age to calculate death risk factor function
riskFunctionEnd = 100 #End age to calculate death risk factor function
deathRiskatStart = 1 #Start factor to increase death risk with age
deathRiskatEnd = 4 #End factor to increase death risk with age. For age = 100 > 4 * Risk
linearRiskP = 0 #Variables to store functions coefficients
linearRiskO = 0
polynomialRiskA = 0
polynomialRiskB = 0
polynomialRiskC = 0

class Virus():

	#Function to return death risk factor in function of human's age
	def deathRiskFactor(age, type):
		r = 1.0
		if age > riskFunctionStart:
			if type == "linear":
				r = age * linearRiskP + linearRiskO
			elif type == "polynomial":
				r = age * age * polynomialRiskA + age * polynomialRiskB + \
				polynomialRiskC
		return r
		
	def getDeathRiskSymptomsW():
		return deathRiskSymptomsWeight
	
	def getDeathRiskTreatmentW():
		return deathRiskTreatmentWeight
	
	def getSymptomsThreshold():
		return baseSymptomsThreshold
	
	def getTreatmentThreshold():
		return baseSymptomsThreshold
	
	def getInfectionThreshold():
		return baseInfectionThreshold
	
	def getHospitalThreshold():
		return baseHospitalThreshold
	
	def getDeathThreshold():
		return baseDeathRate
		
	def getBaseASContagiousFactor():
		return baseASContagiousFactor
	
	def getContagiousShift():
		return contagiousShift
	
	def getFutureImmunity():
		return baseFutureImmunity
		
	#Method to save virus inicial configuration
	def saveSimulationConfig(simulationName):
		virConfig = open("SimulationData/" + simulationName + ".txt", "a")
		virConfig.write("----Virus variables" + "\n")
		virConfig.write("Base infection threshold: " + str(baseInfectionThreshold) + "\n")
		virConfig.write("Base symptoms threshold: " + str(baseSymptomsThreshold) + "\n")
		virConfig.write("Base treatment threshold: " + str(baseTreatmentThreshold) + "\n")
		virConfig.write("Contagious fase shift from incubation end: " + str(contagiousShift) + "\n")
		virConfig.write("Contagious factor when there are no symptoms: " + str(baseASContagiousFactor) + "\n")
		virConfig.write("Probabilty of getting inmunity after infection: " + str(baseFutureImmunity) + "\n")
		virConfig.write("Death rate for patients in treatment: " + str(baseDeathRate) + "\n")
		virConfig.write("Weight of death risk in symptoms: " + str(deathRiskSymptomsWeight) + "\n")
		virConfig.write("Weight of death risk in treatment: " + str(deathRiskTreatmentWeight) + "\n")
		virConfig.write("Death risk function start age: " + str(riskFunctionStart) + "\n")
		virConfig.write("Death risk function end age: " + str(riskFunctionEnd) + "\n")
		virConfig.write("Death risk factor start: " + str(deathRiskatStart) + "\n")
		virConfig.write("Death risk factor end: " + str(deathRiskatEnd) + "\n")
		virConfig.write("" + "\n")
		virConfig.close()

	#Starting variables to store functions coefficients
	def startRiskVariables():
		global linearRiskP
		linearRiskP = (deathRiskatEnd - deathRiskatStart)/ \
					(riskFunctionEnd - riskFunctionStart)
		global linearRiskO
		linearRiskO = 1 - riskFunctionStart / \
					(deathRiskatEnd - deathRiskatStart)
		global polynomialRiskA
		polynomialRiskA = (deathRiskatEnd - deathRiskatStart) / \
						(riskFunctionEnd * riskFunctionEnd - \
						2 * riskFunctionStart * riskFunctionEnd + \
						riskFunctionStart * riskFunctionStart)
		global polynomialRiskB
		polynomialRiskB = (-2) * riskFunctionStart * polynomialRiskA
		global polynomialRiskC
		polynomialRiskC = riskFunctionStart * riskFunctionStart * \
						polynomialRiskA + deathRiskatStart