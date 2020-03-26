baseDeathRate = 0.4 #Base death rate for patients who needed treatment
baseInfectionThreshold = 0.2 #How contagious the virus is
baseSymptomsThreshold = 0.5 #Probability of having symptoms
baseTreatmentThreshold = 0.2 #Probability of needing treatment
deathRiskSymptomsWeight = 0.5 #The probability of been symptomatic is related to death risk
deathRiskTreatmentWeight = 0.8 #The probability of need treatment is related to death risk
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