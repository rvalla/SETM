import matplotlib.pyplot as plt
import random as random

#About population age triangular distribution
population_age_start = 0
population_age_end = 100
population_age_mode = 26

#About family size triangular distribution
family_size_start = 1
family_size_end = 5
family_size_mode = 1.5

#Limits for triangular distribution for factors
factor_start = 0.8
factor_end = 1.2
factor_mode = 1.0

#Limits for illness development
illness_start = 2
illness_end = 10
illness_mode = 4

#Limits for triangular distribution for contacts
contacts_start = 1
contacts_end = 6
contacts_mode = 3

#Limits for triangular distribution for human exchange between urban areas
exchange_start = 4
exchange_end = 18
exchange_mode = 8

#Adjusting relative weights for government infoFactor and socialDistanceFactor
infoFactorW = 2
socialDistanceW = 3

class Randomization():
	"Functions to work with the randomization of elements for simulations"
	
	def isCarefulAverage(infectedHuman, human):
		a = (infectedHuman.carefulFactor + human.carefulFactor) / 2
		return a
	
	def isDistancedAverage(infectedHuman, human):
		a = (infectedHuman.socialDistanceFactor + human.socialDistanceFactor) / 2
		return a
	
	def setFamilySize():
		s = random.triangular(family_size_start, family_size_end, family_size_mode)
		s = round(s)
		return s
	
	def setSex():
		sex = random.choice(["Male", "Female"])
		return sex
	
	def setAge():
		a = random.triangular(population_age_start, population_age_end, population_age_mode)
		a = round(a)
		return a
	
	def aRandom():
		r = random.random()
		return r
	
	def aRandomInt(n, m):
		r = random.randint(n, m)
		return r
	
	def aRandomIntList(n, m, c):
		r = random.sample(range(n, m), c)
		return r
	
	def setCarefulFactor():
		f = random.triangular(factor_start, factor_end, factor_mode)
		return f
	
	def setSocialDistanceFactor():
		f = random.triangular(factor_start, factor_end,	factor_mode)
		return f
	
	def setIllnessDevelopment():
		i = random.triangular(illness_start, illness_end, illness_mode)
		return(round(i, 0))
	
	def setContactsCount(govIsolationFactor):
		c = random.triangular(contacts_start, contacts_end, contacts_mode)
		c = c / govIsolationFactor
		return(int(c))
	
	def setExchangeCount(govIsolationFactor):
		c = random.triangular(exchange_start, exchange_end, exchange_mode)
		c = c / govIsolationFactor
		return (int(c))
	
	#Determining how much will change the random number before deciding infection...
	def getInfectionThresholdVar(i, d):
		t = (i *  infoFactorW + d * socialDistanceW) / (infoFactorW + socialDistanceW)
		return t
	
	def saveSimulationConfig(simulationName):
		rdConfig = open("SimulationData/" + simulationName + ".txt", "a")
		rdConfig.write("----Human general randomization" + "\n")
		rdConfig.write("Triangular ages distribution references: " + str(population_age_start) + ", " + 
						str(population_age_end) + ", " + str(population_age_mode) + "\n")
		rdConfig.write("Triangular family size distribution references: " + str(family_size_start) + ", " + 
						str(family_size_end) + ", " + str(family_size_mode) + "\n")
		rdConfig.write("Triangular careful/socialDistance factor distribution references: " + str(factor_start) + ", " + 
						str(factor_end) + ", " + str(factor_mode) + "\n")
		rdConfig.write("Triangular incubation/illness periods distribution references: " + str(illness_start) + ", " + 
						str(illness_end) + ", " + str(illness_mode) + "\n")
		rdConfig.write("" + "\n")
		rdConfig.write("----Human movement randomization" + "\n")
		rdConfig.write("Triangular contacts count distribution references: " + str(contacts_start) + ", " +
						str(contacts_end) + ", " + str(contacts_mode) + "\n")
		rdConfig.write("Triangular exchange humans distribution references: " + str(exchange_start) + ", " + 
						str(exchange_end) + ", " + str(exchange_mode) + "\n")
		rdConfig.write("Relatives weights for government infoFactor and socialDistanceFactor: " + 
						str(infoFactorW) + ", " + str(socialDistanceW) + "\n")
		rdConfig.write("" + "\n")
		rdConfig.close()