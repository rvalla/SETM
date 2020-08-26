from human import Human as hn
from randomization import Randomization as rd
from governmentactions import GovernmentActions as gov
from processingdata import ProcessingData as dt
from virus import Virus as vr
import pandas as pd
import time as tm

#General data
population = 0
period = 0
areaBDensity = 1.0
behavior = False
behaviorCycles = []

#Representing two separate urban areas
areaAHumans = []
areaBHumans = []
humansInA = set() 
humansInB = set()

#Saving government actions start day
govActionsStartDay = -1
govActionsCycles =[]
govActionsFailure = -1
govActionsFailurePeriod = -1
govActionsActive = False
govFailure = False
govMode = ""

#Simulation statistics
totalInfected = 0
totalTested = 0
totalDeaths = 0
totalRecovered = 0
totalIsolated = 0
actualInfected = 0
actualInTreatment = 0
actualTested = 0
actualIsolated = 0
actualAInfected = 0
ATested = 0
actualAInTreatment = 0
ADeaths = 0
ARecovered = 0
actualBInfected = 0
BTested = 0
actualBInTreatment = 0
BDeaths = 0
BRecovered = 0
infectedPopulationRatio = 0.0
knownInfectedRatio = 0.0
actualImmunity = 0
immunityRatio = 0.0
actualDeathRate = 0.0

#Save simulation start time...
simulationStartTime = 0

#Saving first simulation name...
simulationName0 = ""

#To save de data during simulation
evolutionData = pd.DataFrame(columns=["Day", "Total infected", "Total tested", "Total deaths", "Total recovered",
									"Infected", "Actual tested", "In treatment",
									"Infected in A", "Tested in A", "In treatment in A", "Deaths in A", "Recovered in A",
									"Infected in B", "Tested in B", "In treatment in B", "Deaths in B", "Recovered in B",
									"Known infected %", "Infected population %", "Population immunity %", "Death rate"])
populationData = pd.DataFrame(columns=["Human number", "Age", "Sex", "Family number", "Careful factor", 
									"Social distance", "Death risk"])
virusData = pd.DataFrame(columns=["Human number", "Infection number", "Infection date", "End date",
									"Transmission", "Age", "Sex", "Death risk factor", "Is dead?",
									"Incubation period", "Total illness period", "Is tested?", "Was tested?",
									"Had symptoms?", "Was treated?"])

class Simulation():
	"Structuring one epidemic simulation"
	def __init__(self, populationcount, periodindays, simNumber, casesCero, simulationName, bDensity, \
					govActions, govActionsList, govFailureList, autoIsolationThreshold, startingImmunity, \
					behaviorB, behaviorTrigger, behaviorOff, behaviorFactor):
		
		if simNumber > 1: #We need to clean some variables
			Simulation.deleteSimulation()
		
		global simulationStartTime
		simulationStartTime = tm.time() #To know how much time a simulation takes
		
		global population
		population = populationcount

		if simNumber == 1: #Some things will be the same in all iterations
			global period
			period = periodindays
			global simulationName0
			simulationName0 = simulationName
			global areaBDensity
			areaBDensity = bDensity
			global govMode
			govMode = govActionsList[0]
			vr.startRiskVariables()
			gov.startColapseVariables()
			gov.setAutoActionsTrigger(govActionsList[1])
			gov.setAutoActionsOff(govActionsList[2])
			gov.setStartCaseCount(govActionsList[3])
			gov.setActionsPeriod(govActionsList[4])
			gov.setActiveIsolation(govActionsList[10])
			gov.setActiveTracking(govActionsList[11])
			gov.setActiveTrackingThreshold(govActionsList[12])
			gov.setActiveTrackingPressureW(govActionsList[13])
			gov.setTestingResponseThreshold(govActionsList[14])
			gov.setTestingResponseASThreshold(govActionsList[15])
			global govFailure
			govFailure = govFailureList[0]
			global govActionsFailurePeriod
			govActionsFailurePeriod = govFailureList[2]
			print("Saving starting point data...", end="\r")
			gov.saveSimulationConfig(simulationName)
			vr.saveSimulationConfig(simulationName)
			rd.saveSimulationConfig(simulationName)
			print("Starting point data saved!           ", end="\n")
		
		#Now we create the population that will suffer the outbreak
		Simulation.createHumans(population, casesCero, simulationName, autoIsolationThreshold, startingImmunity)
		
		#We inject desire number of infected humans in area A
		print("Injecting infected humans in urban area A...", end="\r")
		auxRandoms = rd.aRandomIntList(0, len(areaAHumans) - 1, casesCero)
		for i in range(casesCero):
			Simulation.setInfection(areaAHumans[auxRandoms[i]], "A", 1)
			if areaAHumans[auxRandoms[i]].hasImmunity == True:
				areaAHumans[auxRandoms[i]].hasImmunity = False
				Simulation.decreaseV("actualImmunity")
		print("Infected humans injected!                        ", end="\n")
		dt.savePopulationData(areaAHumans, areaBHumans, simulationName)
		print("", end="\n")

		#Simulating each day, one by one...
		for d in range(period):
			print("Simulating day " + str(d + 1) + "...		", end="\r")
			Simulation.simulateDay(d + 1)
			Simulation.saveDay(d + 1)
			if behaviorB == True:
				Simulation.checkHumansBehavior(d, behaviorTrigger, behaviorOff, behaviorFactor)
			if govActions == True:
				Simulation.checkGovActions(d, govActionsList, govFailureList)
			if d < period:
				Simulation.humanExchange(areaAHumans, areaBHumans)
			
		print("Simulation Complete!				", end="\n")
		print("Infected: " + str(totalInfected) + ", Recovered: " + str(totalRecovered) + ", Deaths: " +
				str(totalDeaths), end="\n")
		print("Time needed for this simulation: " +
				Simulation.getSimulationTime(simulationStartTime, tm.time()), end="\n")
				
		print("", end="\n")
		print("Saving simulation's data...", end="\r")
		evolutionData.to_csv("SimulationData/Simulations/" + simulationName + ".csv", index=False)
		virusData.to_csv("SimulationData/Infections/" + simulationName + "_infections.csv", index=False)
		Simulation.saveSimulationConfig(simulationName0, simNumber, casesCero, govActionsCycles, \
			govActions, behaviorB, behaviorCycles)
		print("Simulation's data saved!       ", end="\n")
		
	#####################################################################################################
	#Simulating a day...
	def simulateDay(d):			
		Simulation.simulateAreaA(d)
		Simulation.simulateAreaB(d)
		Simulation.getDeathRate()
		Simulation.getInfectedRatio()
		Simulation.getKnownInfectedRatio()
		Simulation.getImmunityRatio()
		
	def simulateAreaA(d):
		infectedList = Simulation.getInfectedList(areaAHumans)
		for i in range(len(infectedList)):
			hIndex = Simulation.getHumanIndex(areaAHumans, infectedList[i])
			if areaAHumans[hIndex].isIsolated == False:
				areaAHumans[hIndex].contacts = Simulation.setHumanContacts(areaAHumans, 1.0)
				for f in range (len(areaAHumans[hIndex].family)):
					indexF = Simulation.getHumanIndex(areaAHumans, areaAHumans[hIndex].family[f])
					if areaAHumans[indexF].isInfected == False:
						Simulation.decideInfection(areaAHumans[hIndex], areaAHumans[indexF], "A", d)
				for c in range (len(areaAHumans[hIndex].contacts)):
					areaAHumans[hIndex].contactsHistory.add(areaAHumans[hIndex].contacts[c])
					indexC = Simulation.getHumanIndex(areaAHumans, areaAHumans[hIndex].contacts[c])
					if areaAHumans[indexC].isInfected == False:
						Simulation.decideInfection(areaAHumans[hIndex], areaAHumans[indexC], "A", d)
			Simulation.evolInfection(areaAHumans[hIndex], "A", d)

	def simulateAreaB(d):
		infectedList = Simulation.getInfectedList(areaBHumans)
		for i in range(len(infectedList)):
			hIndex = Simulation.getHumanIndex(areaBHumans, infectedList[i])
			if areaBHumans[hIndex].isIsolated == False:
				areaBHumans[hIndex].contacts = Simulation.setHumanContacts(areaBHumans, areaBDensity)
				for f in range (len(areaBHumans[hIndex].family)):
					indexF = Simulation.getHumanIndex(areaBHumans, areaBHumans[hIndex].family[f])
					if areaBHumans[indexF].isInfected == False:
						Simulation.decideInfection(areaBHumans[hIndex], areaBHumans[indexF], "B", d)
				for c in range (len(areaBHumans[hIndex].contacts)):
					areaBHumans[hIndex].contactsHistory.add(areaBHumans[hIndex].contacts[c])
					indexC = Simulation.getHumanIndex(areaBHumans, areaBHumans[hIndex].contacts[c])
					if areaBHumans[indexC].isInfected == False:
						Simulation.decideInfection(areaBHumans[hIndex], areaBHumans[indexC], "B", d)
			Simulation.evolInfection(areaBHumans[hIndex], "B", d)

	#Deciding infection after checking immunity
	def decideInfection(infectedHuman, human, area, d):
		Simulation.checkImmunity(human, d, vr.getImmunityPeriod())
		if human.hasImmunity == False:
			r = rd.aRandom()
			c = rd.isCarefulAverage(infectedHuman, human) * gov.getInfoFactor()
			s = rd.isDistancedAverage(infectedHuman, human) * gov.getSocialDistanceFactor()
			infectionP = r * rd.getInfectionThresholdVar(c, s)
			if infectionP < vr.getInfectionThreshold() *  infectedHuman.contagiousFactor:
				Simulation.setInfection(human, area, d)
				infectedHuman.transmission += 1

	#Method to make human infected
	def setInfection(human, area, d):
		human.isInfected = True
		human.infectionNumber += 1
		human.infectionDate = d
		human.isTested = False
		illness = rd.setIllnessDevelopment()
		human.incubationPeriod = illness
		illness += rd.setIllnessDevelopment()
		human.illnessPeriod = illness
		human.evolutionState = 0
		
		#Defining if infected humans will be symptomatic or will need treatment
		auxRandom = rd.aRandom()
		symptomsThreshold = vr.getSymptomsThreshold() * human.deathRiskFactor * vr.getDeathRiskSymptomsW()
		treatmentThreshold = vr.getTreatmentThreshold() * human.deathRiskFactor * vr.getDeathRiskTreatmentW()
		reinfectionFactor = vr.getReinfectionFactor(human.infectionNumber)
		if auxRandom < symptomsThreshold * reinfectionFactor:
			human.willBeSymptomatic = True
			auxRandom = rd.aRandom()
			if auxRandom < treatmentThreshold * reinfectionFactor:
				human.willNeedTreatment = True
		
		Simulation.increaseV("totalInfected")
		Simulation.increaseV("actualInfected")
		if area == "A":
			Simulation.increaseV("actualAInfected")
		elif area == "B":
			Simulation.increaseV("actualBInfected")

	#Illness evolution	
	def evolInfection(human, area, d):
		human.evolutionState += 1
		
		#Simulating government tests
		if human.isTested == False:
			Simulation.decideTest(human, area)

		#Illness evolution...		
		if human.willBeSymptomatic == True:
			if human.evolutionState == human.incubationPeriod:
				human.isSymptomatic = True
				if human.autoIsolation == True: #Humans can isolate themselves
						human.isIsolated = True
				if human.willNeedTreatment == True:
					human.isInTreatment = True
					Simulation.increaseV("actualInTreatment")
					if area == "A":
						Simulation.increaseV("actualAInTreatment")
					elif area == "B":
						Simulation.increaseV("actualBInTreatment")
			elif human.evolutionState == human.illnessPeriod:
				if human.isSymptomatic == True:
					if human.isInTreatment == True:
						if Simulation.decideDeath(human) == True:
							Simulation.killHuman(human, area, d)
						else:
							Simulation.setCure(human, area, d)
						Simulation.decreaseV("actualInTreatment")
						if area == "A":
							Simulation.decreaseV("actualAInTreatment")
						elif area == "B":
							Simulation.decreaseV("actualBInTreatment")
					elif human.isInTreatment == False:
						Simulation.setCure(human, area, d)
			if human.evolutionState == human.incubationPeriod + vr.getContagiousShift():
				human.contagiousFactor = 1.0 #Contagious factor can change before of after the symptoms appear
			if human.evolutionState == human.illnessPeriod + vr.getContagiousShift():
				human.contagiousFactor = vr.getBaseASContagiousFactor()
		elif human.willBeSymptomatic == False:
			if human.evolutionState == human.illnessPeriod:
				Simulation.setCure(human, area, d)

	#Deciding if human is tested
	def decideTest(notTestedHuman, area):
		r = rd.aRandom()
		tested = False
		if notTestedHuman.isSymptomatic == True:
			if r < gov.getTestingResponseThreshold():
				tested = True
		elif notTestedHuman.isSymptomatic == False:
			if r < gov.getTestingResponseASThreshold():
				tested = True
		if notTestedHuman.isInTreatment == True: #Probability of being tested in treatment is 1
			tested = True
		if tested == True:
			Simulation.testHuman(notTestedHuman, area)
			if gov.getActiveTracking() == True:
				Simulation.contactTracking(notTestedHuman.family, notTestedHuman.contactsHistory, area)
	
	def testHuman(human, area):
		if human.isInfected == True and human.isTested == False:
			human.isTested = True
			human.wasTested = True
			Simulation.decideActiveIsolation(human)
			Simulation.increaseV("totalTested")
			Simulation.increaseV("actualTested")
			if area == "A":
				Simulation.increaseV("ATested")
			elif area == "B":
				Simulation.increaseV("BTested")
				
	def decideActiveIsolation(human):
		if gov.getActiveIsolation() == True:
			human.isIsolated = True
	
	#Looking tested human closed contacts to isolate or test them
	def contactTracking(family, contacts, area):
		for f in range(len(family)):
			Simulation.lookForContact(family[f], area)
		for c in contacts:
			r = rd.aRandom()
			if r < gov.getActiveTrackingThreshold(infectedPopulationRatio):
				if c in humansInA:
					Simulation.lookForContact(c, "A")
				elif c in humansInB:
					Simulation.lookForContact(c, "B")

	def lookForContact(humanNumber, area):
		if area == "A":
			hIndex = Simulation.getHumanIndex(areaAHumans, humanNumber)
			Simulation.testHuman(areaAHumans[hIndex], area)
		elif area == "B":
			hIndex = Simulation.getHumanIndex(areaBHumans, humanNumber)
			Simulation.testHuman(areaBHumans[hIndex], area)
	
	#Deciding if a human will die
	def decideDeath(human):
		death = False
		d = rd.aRandom()
		d = d * human.deathRiskFactor * gov.treatmentColapseFactor(infectedPopulationRatio, "polynomial")
		if d < vr.getDeathThreshold():
			death = True
		return death
	
	#Method for kill a human
	def killHuman(human, area, d):
		humanNumber = human.humanNumber
		human.endDate = d
		hIndex = 0
		Simulation.increaseV("totalDeaths")
		Simulation.decreaseV("actualInfected")
		Simulation.decreaseV("population")
		Simulation.saveInfection(human, True)
		if human.isTested == True:
			Simulation.decreaseV("actualTested")
		if area == "A":
			hIndex = Simulation.getHumanIndex(areaAHumans, humanNumber)
			Simulation.cleanFamilyandContacts(areaAHumans, hIndex, humanNumber)
			del areaAHumans[hIndex]
			humansInA.discard(humanNumber)
			Simulation.decreaseV("actualAInfected")
			Simulation.increaseV("ADeaths")
		elif area == "B":
			hIndex = Simulation.getHumanIndex(areaBHumans, humanNumber)
			Simulation.cleanFamilyandContacts(areaBHumans, hIndex, humanNumber)
			del areaBHumans[hIndex]
			humansInB.discard(humanNumber)
			Simulation.decreaseV("actualBInfected")
			Simulation.increaseV("BDeaths")
		
	#Cleaning contacts from dead humans...
	def cleanFamilyandContacts(humans, humanIndex, humanNumber):
		for h in range(len(humans)):
			for f in range(len(humans[h].family)):
				if humans[h].family[f] == humanNumber:
					del humans[h].family[f]
					break
			for c in range(len(humans[h].contacts)):
				if humans[h].contacts[c] == humanNumber:
					del humans[h].contacts[c]
					break
	
	#Set contacts list for infected humans
	def setHumanContacts(humans, density):
		contacts = []
		quantity = rd.setContactsQuantity(gov.getIsolationFactor(), density)
		if quantity > 0:
			auxRandoms = rd.aRandomIntList(0, len(humans) - 1, int(quantity))
			for i in range(len(auxRandoms)):
				contacts.append(Simulation.getHumanNumber(humans, auxRandoms[i]))
		return contacts
	
	#Method to set the cure
	def setCure(human, area, d):
		human.isInfected = False
		human.endDate = d
		Simulation.increaseV("totalRecovered")
		Simulation.decreaseV("actualInfected")
		Simulation.saveInfection(human, False)
		human.hasImmunity = True
		Simulation.increaseV("actualImmunity")
		human.isSymptomatic = False
		human.willBeSymptomatic = False
		human.isInTreatment = False
		human.willNeedTreatment = False
		human.isIsolated = False
		human.transmission = 0
		if human.isTested == True:
			Simulation.decreaseV("actualTested")
		if area == "A":
			Simulation.increaseV("ARecovered")
			Simulation.decreaseV("actualAInfected")
		elif area == "B":
			Simulation.increaseV("BRecovered")
			Simulation.decreaseV("actualBInfected")
	
	#Method to check if human has immunity
	def checkImmunity(human, d, immunityPeriod):
		if immunityPeriod < d - human.endDate:
			if human.hasImmunity == True:
				human.hasImmunity = False 
				Simulation.decreaseV("actualImmunity")
	
	#Setting humans exchange between urban areas
	def humanExchange(areaAH, areaBH):
		if gov.getLockDown() == False:
			areaAExits = rd.setExchangeCount(gov.getExchangeFactor())
			indexesA = rd.aRandomIntList(0, len(areaAH) - 1, areaAExits)
			humanNumbersA = []
			for n in range(len(indexesA)):
				humanNumbersA.append(Simulation.getHumanNumber(areaAH, indexesA[n]))
			for a in range(areaAExits):
				family = areaAH[Simulation.getHumanIndex(areaAH, humanNumbersA[a])].family
				for f in range(len(family)):
					if Simulation.checkInTreatmentFamily(areaAH, family) == False:
						member = Simulation.getHumanIndex(areaAH, family[f])
						humansInB.add(family[f])
						areaBH.append(areaAH[member])
						Simulation.correctStatistics("A", areaAH[member])
						humansInA.discard(family[f])
						del areaAH[member]
			areaBExits = rd.setExchangeCount(gov.getExchangeFactor())
			indexesB = rd.aRandomIntList(0, len(areaBH) - 1, areaBExits)
			humanNumbersB = []
			for n in range(len(indexesB)):
				humanNumbersB.append(Simulation.getHumanNumber(areaBH, indexesB[n]))
			for a in range(areaBExits):
				family = areaBH[Simulation.getHumanIndex(areaBH, humanNumbersB[a])].family
				for f in range(len(family)):
					if Simulation.checkInTreatmentFamily(areaBH, family) == False:
						member = Simulation.getHumanIndex(areaBH, family[f])
						humansInA.add(family[f])
						areaAH.append(areaBH[member])
						Simulation.correctStatistics("B", areaBH[member])
						humansInB.discard(family[f])
						del areaBH[member]

	#Correcting actual variables after humans exchange...
	def correctStatistics(departureArea, human):
		if departureArea == "A":
			if human.isInfected == True:
				Simulation.increaseV("actualBInfected")
				Simulation.decreaseV("actualAInfected")
		if departureArea == "B":
			if human.isInfected == True:
				Simulation.decreaseV("actualBInfected")
				Simulation.increaseV("actualAInfected")
	
	#Checking to preven exchange of patients in treatment
	def checkInTreatmentFamily(humans, familyMembers):
		inTreatment = False
		for f in range(len(familyMembers)):
			hIndex = Simulation.getHumanIndex(humans, familyMembers[f])
			if humans[hIndex].isInTreatment == True:
				inTreatment = True
		return inTreatment
		
	def checkGovActions(actualDay, govActionsList, govFaiLureList):
		if govMode == "normal":
			Simulation.checkNormalGovActions(actualDay, govActionsList, govFaiLureList)
		elif govMode == "auto":
			Simulation.checkAutoGovActions(actualDay, govActionsList)
			
	def checkNormalGovActions(actualDay, govActionsList, govFailureList):
		if totalTested >= gov.getStartCaseCount():
			global govActionsActive
			if govActionsActive == False:
				govActionsActive = True
				global govActionsStartDay
				govActionsStartDay = actualDay
				Simulation.startGovActions(actualDay, govActionsList)
			elif govActionsActive == True:
			#	global govActionsCycles
				if govFailure == True: #Checking if there will be government failures
					if actualDay == govActionsStartDay + govFailureList[1]:
						gov.resetCountermeasures()
						govActionsCycles.append(actualDay)
					elif actualDay == govActionsStartDay + govFailureList[1] + govFailureList[2]:
						Simulation.startGovActions(actualDay, govActionsList)
				if actualDay == govActionsStartDay + gov.getActionsPeriod():
					gov.resetCountermeasures()
					govActionsCycles.append(actualDay)
	
	def checkAutoGovActions(actualDay, govActionsList):
		global govActionsActive
		if knownInfectedRatio > gov.getAutoActionsTrigger():
			if govActionsActive == False:
				govActionsActive = True
				global govActionsStartDay
				govActionsStartDay = actualDay
				Simulation.startGovActions(actualDay, govActionsList)
		elif knownInfectedRatio < gov.getAutoActionsOff():
			if govActionsActive == True:
				govActionsActive = False
				gov.resetCountermeasures()
				govActionsCycles.append(actualDay)
				
	def startGovActions(actualDay, govActionsList):
		gov.setInfoFactor(govActionsList[5])
		gov.setSocialDistanceFactor(govActionsList[6])
		gov.setIsolationFactor(govActionsList[7])
		gov.setExchangeFactor(govActionsList[8])
		gov.setLockDown(govActionsList[9])
		global govActionsCycles
		govActionsCycles.append(actualDay)
	
	def checkHumansBehavior(d, behaviorTrigger, behaviorOff, behaviorFactor):
		global behavior
		if knownInfectedRatio > behaviorTrigger:
			if behavior == False:
				Simulation.improveHumans(areaAHumans, areaBHumans, d, behaviorFactor)
				behavior = True
		elif knownInfectedRatio <= behaviorOff:
			if behavior == True:
				Simulation.resetHumansImprovement(areaAHumans, areaBHumans, d, behaviorFactor)
				behavior = False
	
	def improveHumans(areaAHumans, areaBHumans, d, behaviorFactor):
		for h in range(len(areaAHumans)):
			areaAHumans[h].carefulFactor = areaAHumans[h].carefulFactor * behaviorFactor
			areaAHumans[h].socialDistanceFactor = areaAHumans[h].socialDistanceFactor * behaviorFactor
		for h in range(len(areaBHumans)):
			areaBHumans[h].carefulFactor = areaBHumans[h].carefulFactor * behaviorFactor
			areaBHumans[h].socialDistanceFactor = areaBHumans[h].socialDistanceFactor * behaviorFactor
		global behaviorCycles
		behaviorCycles.append(d)
		
	def resetHumansImprovement(areaAHumans, areaBHumans, d, behaviorFactor):
		for h in range(len(areaAHumans)):
			areaAHumans[h].carefulFactor = areaAHumans[h].carefulFactor / behaviorFactor
			areaAHumans[h].socialDistanceFactor = areaAHumans[h].socialDistanceFactor / behaviorFactor
		for h in range(len(areaBHumans)):
			areaBHumans[h].carefulFactor = areaBHumans[h].carefulFactor / behaviorFactor
			areaBHumans[h].socialDistanceFactor = areaBHumans[h].socialDistanceFactor / behaviorFactor
		global behaviorCycles
		behaviorCycles.append(d)
		
	######################################################################################################
	#Creating humans and simulation environment
	def createHumans(population, casesCero, simulationName, autoIsolationThreshold, startingImmunity):
		
		#Humans initialization
		humans = []
		auxRandom = 0
		auxRandoms = []
		
		for p in range(population):
			
			humans.append(hn(p))
			
			if p % 100 == 0:
				print("Creating humans: " + str(p) + "    ", end="\r")
				tm.sleep(0.0001)
			
			#Human configuration
			humans[p].age = rd.setAge()
			humans[p].sex = rd.setSex()
			humans[p].carefulFactor = rd.setCarefulFactor()
			humans[p].socialDistanceFactor = rd.setSocialDistanceFactor()
			humans[p].contagiousFactor = vr.getBaseASContagiousFactor()
			
			humans[p].deathRiskFactor = vr.deathRiskFactor(humans[p].age, "polynomial")
			
			#Defining if human will isolate himself in case of having symptoms
			auxRandom = rd.aRandom()
			if auxRandom <= autoIsolationThreshold:
				humans[p].autoIsolation = True
				
			auxRandom = rd.aRandom()
			if auxRandom <= startingImmunity:
				humans[p].hasImmunity = True
				Simulation.increaseV("actualImmunity")
			
		Simulation.assignFamilies(humans)
		Simulation.assignAreas(humans)
		
		print("Creating humans complete!		", end="\n")
	
	#Defining families for each human
	def assignFamilies(humans):
		hcount = 0
		actualFamily = 0
		print("Assigning families...       ", end="\r")
		while hcount < len(humans):
			members = rd.setFamilySize()
			for i in range(members):
				if i + hcount < len(humans):
					humans[i + hcount].familyNumber = actualFamily
					humans[hcount].family.append(i + hcount)
			if members > 1:
				for i in range(members - 1):
					if i + hcount + 1 < len(humans):
						humans[hcount + i + 1].family = humans[hcount].family
			hcount += members
			actualFamily += 1
		print("Assigning families complete!  ", end="\n")
	
	#Assigning urban areas	
	def assignAreas(humans):
		#Assigning urban area
		print("Assigning urban areas...     ", end="\r")
		p = 0
		while p < len(humans):
			area = rd.aRandom()
			if area > 0.5:
				for f in range(len(humans[p].family)):
					areaAHumans.append(humans[p])
					humansInA.add(humans[p].humanNumber)
					p += 1
			else:
				for f in range(len(humans[p].family)):
					areaBHumans.append(humans[p])
					humansInB.add(humans[p].humanNumber)
					p += 1
		print("Assigning urban areas complete!     ", end="\n")
		
	#####################################################################################################
	#Some methods to get the code above here more clean	
	def getInfectedList(humans):
		ls = []
		for i in range(len(humans)):
			if humans[i].isInfected == True:
				ls.append(Simulation.getHumanNumber(humans, i))
		return ls
	
	def getHumanIndex(humans, humanNumber):
		hIndex = -1
		for i in range(len(humans)):
			if humans[i].humanNumber == humanNumber:
				hIndex = i
				break
		return hIndex
	
	def getHumanNumber(humans, hIndex):
		humanNumber = humans[hIndex].humanNumber
		return humanNumber

	def printHumans(humans):
		for i in range(len(humans)):
			dt.printHuman(humans[i])
	
	def getInfectedRatio():
		global infectedPopulationRatio
		infectedPopulationRatio = actualInfected / population

	def getKnownInfectedRatio():
		global knownInfectedRatio
		knownInfectedRatio = actualTested / population
		
	def getImmunityRatio():
		global immunityRatio
		immunityRatio = actualImmunity / population
	
	def getDeathRate():
		global actualDeathRate
		actualDeathRate = totalDeaths / totalInfected
	
	def saveDay(day):
		global evolutionData
		auxRow = pd.DataFrame([[day, totalInfected, totalTested, totalIsolated, totalDeaths, totalRecovered,
								actualInfected,	actualTested, actualInTreatment, actualIsolated, actualAInfected,
								ATested, actualAInTreatment,	ADeaths, ARecovered, actualBInfected, BTested,
								actualBInTreatment, BDeaths, BRecovered, round(knownInfectedRatio, 5),
								round(infectedPopulationRatio, 5), round(immunityRatio, 5),
								round(actualDeathRate, 5)]],
								columns=["Day", "Total infected", "Total tested", "Total isolated", "Total deaths",
									"Total recovered", "Infected", "Actual tested", "In treatment", "Isolated",
									"Infected in A", "Tested in A", "In treatment in A", "Deaths in A",
									"Recovered in A","Infected in B", "Tested in B", "In treatment in B",
									"Deaths in B", "Recovered in B", "Known infected %", "Infected population %",
									"Population immunity %", "Death rate"])
		evolutionData = pd.concat([evolutionData, auxRow])

	def saveInfection(human, isDead):
		global virusData
		auxRow = pd.DataFrame([[human.humanNumber, human.infectionNumber, human.infectionDate, human.endDate,
								human.transmission, human.age, human.sex, human.deathRiskFactor, isDead,
								human.incubationPeriod, human.illnessPeriod, human.isTested, human.wasTested,
								human.willBeSymptomatic, human.willNeedTreatment]],
								columns=["Human number", "Infection number",  "Infection date", "End date",
									"Transmission", "Age", "Sex", "Death risk factor", "Is dead?",
									"Incubation period", "Total illness period", "Is tested?", "Was tested?",
									"Had symptoms?", "Was treated?"])
		virusData = pd.concat([virusData, auxRow])
	
	def saveSimulationConfig(simulationName, sinNumber, casesCero, govActionsC, govActions, behaviorB, behaviorC):
		startConfig = open("SimulationData/" + simulationName + ".txt", "a")
		if sinNumber == 1:
			startConfig.write("----Simulation start" + "\n")
			if casesCero < 2:
				startConfig.write(str(casesCero) +  " infected human was injected in urban area A." + "\n")
			else:
				startConfig.write(str(casesCero) +  " infected humans were injected in urban area A." + "\n")
			startConfig.write("" + "\n")
		if govActions == True:
			if govActionsStartDay == -1:
				startConfig.write(str(sinNumber) + ". Government actions never started." + "\n")
			else:
				startConfig.write(str(sinNumber) + ". Government actions cycles: " + str(govActionsC) + "\n")
		if behaviorB == True:
			startConfig.write(str(sinNumber) + ". Population behavior cycles: " + str(behaviorC) + "\n")

	#Deleting data and humans to run a new simulation
	def deleteSimulation():
		print("Deleting humans from previous population...", end="\r")
		areaAHumans.clear()
		areaBHumans.clear()
		Simulation.restartV()
		print("Humans from previous population deleted!        ", end="\n")
		print("Erasing outbreak evolution data...", end="\r")
		global evolutionData
		evolutionData = pd.DataFrame(columns=evolutionData.columns)
		print("Outbreak evolution data erased!      ", end="\n")
		print("Erasing infections data...", end="\r")
		global virusData
		virusData = pd.DataFrame(columns=virusData.columns)
		print("Infections data erased!             ", end="\n")
	
	#Calculating time needed for simulation to finish...
	def getSimulationTime(startTime, endTime):
		time = endTime - startTime
		formatedTime = Simulation.formatTime(time)
		return formatedTime
	
	def formatTime(time):
		ms = ""
		minutes = time // 60
		seconds = time - minutes * 60
		seconds = round(seconds, 2)
		ms = "{:02d}".format(int(minutes))
		ms += ":"
		ms += "{:05.2f}".format(seconds)
		return ms
	
	def getGovActionsCycles():
		global govActionsCycles
		length = len(govActionsCycles)
		if length %2 != 0:
			govActionsCycles.append(period)
		return govActionsCycles
	
	def getBehaviorCycles():
		global behaviorCycles
		length = len(behaviorCycles)
		if length % 2 != 0:
			behaviorCycles.append(period)
		return behaviorCycles
	
	#Restarting variables in case another simulation is needed...
	def restartV():
		global totalInfected
		totalInfected = 0
		global totalTested
		totalTested = 0
		global totalDeaths
		totalDeaths = 0
		global totalRecovered
		totalRecovered = 0
		global totalIsolated
		totalIsolated = 0
		global actualInfected
		actualInfected = 0
		global actualInTreatment
		actualInTreatment = 0
		global actualTested
		actualTested = 0
		global actualIsolated
		actualIsolated = 0
		global actualAInfected
		actualAInfected = 0
		global ATested
		ATested = 0
		global actualAInTreatment
		actualAInTreatment = 0
		global ADeaths
		ADeaths = 0
		global ARecovered
		ARecovered = 0
		global actualBInfected
		actualBInfected = 0
		global BTested
		BTested = 0
		global actualBInTreatment
		actualBInTreatment = 0
		global BDeaths
		BDeaths = 0
		global BRecovered
		BRecovered = 0
		global actualImmunity
		actualImmunity = 0
		global govActionsStartDay
		govActionsStartDay = -1
		global govActionsActive
		govActionsActive = False
		global govActionsFailure
		govActionsFailure = -1
		global govActionsFailurePeriod
		govActionsFailurePeriod = -1

	#Simple methods to increase or decrease global variables
	def increaseV(vName):
		if vName == "population":
			global population
			population += 1
		if vName == "totalInfected":
			global totalInfected
			totalInfected += 1
		if vName == "totalTested":
			global totalTested
			totalTested += 1
		if vName == "totalDeaths":
			global totalDeaths
			totalDeaths += 1
		if vName == "totalRecovered":
			global totalRecovered
			totalRecovered += 1
		if vName == "totalIsolated":
			global totalIsolated
			totalIsolated += 1
		if vName == "actualInfected":
			global actualInfected
			actualInfected += 1
		if vName == "actualInTreatment":
			global actualInTreatment
			actualInTreatment += 1
		if vName == "actualTested":
			global actualTested
			actualTested += 1
		if vName == "actualIsolated":
			global actualIsolated
			actualIsolated += 1
		if vName == "actualAInfected":
			global actualAInfected
			actualAInfected += 1
		if vName == "ATested":
			global ATested
			ATested += 1
		if vName == "actualAInTreatment":
			global actualAInTreatment
			actualAInTreatment += 1
		if vName == "ADeaths":
			global ADeaths
			ADeaths += 1
		if vName == "ARecovered":
			global ARecovered
			ARecovered += 1
		if vName == "actualBInfected":
			global actualBInfected
			actualBInfected += 1
		if vName == "BTested":
			global BTested
			BTested += 1
		if vName == "actualBInTreatment":
			global actualBInTreatment
			actualBInTreatment += 1
		if vName == "BDeaths":
			global BDeaths
			BDeaths += 1
		if vName == "BRecovered":
			global BRecovered
			BRecovered += 1
		if vName == "actualImmunity":
			global actualImmunity
			actualImmunity += 1
	
	def decreaseV(vName):
		if vName == "population":
			global population
			population -= 1
		if vName == "totalInfected":
			global totalInfected
			totalInfected -= 1
		if vName == "totalTested":
			global totalTested
			totalTested -= 1
		if vName == "totalDeaths":
			global totalDeaths
			totalDeaths -= 1
		if vName == "totalRecovered":
			global totalRecovered
			totalRecovered -= 1
		if vName == "totalIsolated":
			global totalIsolated
			totalIsolated -= 1
		if vName == "actualInfected":
			global actualInfected
			actualInfected -= 1
		if vName == "actualInTreatment":
			global actualInTreatment
			actualInTreatment -= 1
		if vName == "actualTested":
			global actualTested
			actualTested -= 1
		if vName == "actualIsolated":
			global actualIsolated
			actualIsolated -= 1
		if vName == "actualAInfected":
			global actualAInfected
			actualAInfected -= 1
		if vName == "ATested":
			global ATested
			ATested -= 1
		if vName == "actualAInTreatment":
			global actualAInTreatment
			actualAInTreatment -= 1
		if vName == "ADeaths":
			global ADeaths
			ADeaths -= 1
		if vName == "ARecovered":
			global ARecovered
			ARecovered -= 1
		if vName == "actualBInfected":
			global actualBInfected
			actualBInfected -= 1
		if vName == "BTested":
			global BTested
			BTested -= 1
		if vName == "actualBInTreatment":
			global actualBInTreatment
			actualBInTreatment -= 1
		if vName == "BDeaths":
			global BDeaths
			BDeaths -= 1
		if vName == "BRecovered":
			global BRecovered
			BRecovered -= 1
		if vName == "actualImmunity":
			global actualImmunity
			actualImmunity -= 1