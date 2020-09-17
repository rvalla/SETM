class Virus():
	"Virus modelling for epidemic simulations"
	
	bInfectionThreshold = 0.10 #How contagious the virus is
	bASContagiousFactor = 0.2 #Contagious factor in absence of symptoms
	bSymptomsThreshold = 0.4 #Probability of having symptoms
	bTreatmentThreshold = 0.2 #Probability of needing treatment
	immunityPeriod = 360 #Days of immunity after an infection
	reinfectionFactor = 1.0 #Control the power of disease in a reinfected human
	contagiousShift = 0 #Days offset between most contagious face and symptoms
	bDeathRate = 0.4 #Base death rate for patients who needed treatment
	deathRiskSymptomsWeight = 0.7 #The probability of been symptomatic is related to death risk
	deathRiskTreatmentWeight = 0.6 #The probability of need treatment is related to death risk
	riskFunctionStart = 30 #Start age to calculate death risk factor function
	riskFunctionEnd = 100 #End age to calculate death risk factor function
	deathRiskatStart = 1 #Start factor to increase death risk with age
	deathRiskatEnd = 5 #End factor to increase death risk with age. For age = 100 > 4 * Risk
	linearRiskP = 0 #Variables to store functions coefficients
	linearRiskO = 0
	polynomialRiskA = 0
	polynomialRiskB = 0
	polynomialRiskC = 0
	
	def __init__(self):
		Virus.startRiskVariables()
		
	#Function to return death risk factor in function of human's age
	def deathRiskFactor(age, type):
		r = 1.0
		if age > Virus.riskFunctionStart:
			if type == "linear":
				r = age * Virus.linearRiskP + Virus.linearRiskO
			elif type == "polynomial":
				r = age * age * Virus.polynomialRiskA + age * Virus.polynomialRiskB + \
				Virus.polynomialRiskC
		return r
	
	#Method to control de power the disease on a reinfected human
	def getReinfectionFactor(iNumber):
		if iNumber == 1:
			return 1.0
		elif iNumber > 1:
			f = pow(Virus.reinfectionFactor, iNumber - 1)
			return f
		
	#Method to save virus inicial configuration
	def saveSimulationConfig(simulationName):
		virConfig = open("SimulationData/" + simulationName + ".txt", "a")
		virConfig.write("----Virus variables" + "\n")
		virConfig.write("Base infection threshold: " + str(Virus.bInfectionThreshold) + "\n")
		virConfig.write("Base symptoms threshold: " + str(Virus.bSymptomsThreshold) + "\n")
		virConfig.write("Base treatment threshold: " + str(Virus.bTreatmentThreshold) + "\n")
		virConfig.write("Contagious fase shift from incubation end: " + str(Virus.contagiousShift) + "\n")
		virConfig.write("Contagious factor when there are no symptoms: " + str(Virus.bASContagiousFactor) + "\n")
		virConfig.write("Maximum contagious factor when there are symptoms: " + str(1.0) + "\n")
		virConfig.write("Days of immunity after cure: " + str(Virus.immunityPeriod) + "\n")
		virConfig.write("Virus reinfection factor: " + str(Virus.reinfectionFactor) + "\n")
		virConfig.write("Death rate for patients in treatment: " + str(Virus.bDeathRate) + "\n")
		virConfig.write("Weight of death risk in symptoms: " + str(Virus.deathRiskSymptomsWeight) + "\n")
		virConfig.write("Weight of death risk in treatment: " + str(Virus.deathRiskTreatmentWeight) + "\n")
		virConfig.write("Death risk function start age: " + str(Virus.riskFunctionStart) + "\n")
		virConfig.write("Death risk function end age: " + str(Virus.riskFunctionEnd) + "\n")
		virConfig.write("Death risk factor start: " + str(Virus.deathRiskatStart) + "\n")
		virConfig.write("Death risk factor end: " + str(Virus.deathRiskatEnd) + "\n")
		virConfig.write("" + "\n")
		virConfig.close()

	#Starting variables to store functions coefficients
	def startRiskVariables():
		Virus.linearRiskP = (Virus.deathRiskatEnd - Virus.deathRiskatStart)/ \
					(Virus.riskFunctionEnd - Virus.riskFunctionStart)
		Virus.linearRiskO = 1 - Virus.riskFunctionStart / \
					(Virus.deathRiskatEnd - Virus.deathRiskatStart)
		Virus.polynomialRiskA = (Virus.deathRiskatEnd - Virus.deathRiskatStart) / \
						(Virus.riskFunctionEnd * Virus.riskFunctionEnd - \
						2 * Virus.riskFunctionStart * Virus.riskFunctionEnd + \
						Virus.riskFunctionStart * Virus.riskFunctionStart)
		Virus.polynomialRiskB = (-2) * Virus.riskFunctionStart * Virus.polynomialRiskA
		Virus.polynomialRiskC = Virus.riskFunctionStart * Virus.riskFunctionStart * \
						Virus.polynomialRiskA + Virus.deathRiskatStart
	
	def __str__(self):
		return "----------------------------------\n" + \
				"--- SETM: Human to human model ---\n" + \
				"--- https://github/rvalla/SETM ---\n" + \
				"-------------- Virus -------------\n" + \
				"Infection threshold: " + str(Virus.bInfectionThreshold) + "\n" + \
				"Asymptomatic contagious factor: " + str(Virus.bASContagiousFactor) + "\n" + \
				"Symptoms threshold: " + str(Virus.bSymptomsThreshold) + "\n" + \
				"Treatment threshold: " + str(Virus.bTreatmentThreshold) + "\n" + \
				"Immunity period: " + str(Virus.immunityPeriod) + "\n" + \
				"Contagious symptoms shift: " + str(Virus.contagiousShift) + "\n"