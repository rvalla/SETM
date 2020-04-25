from human import Human as hn
from randomization import Randomization as rd
from govermentactions import GovermentActions as gov
from processingdata import ProcessingData as dt
from virus import Virus as vr
import pandas as pd
import time as tm

#General data
population = 0
period = 0
psicosis = False
psicosisCycles = []

#Representing two separate urban areas
areaAHumans = []
areaBHumans = []

#Saving government actions start day
govActionsStartDay = -1
govActionsEndDay = -1
govActionsFailure = -1
govActionsFailurePeriod = -1
govActionsActive = False

#Simulation statistics
totalInfected = 0
totalTested = 0
totalDeaths = 0
totalRecovered = 0
actualInfected = 0
actualInTreatment = 0
actualTested = 0
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
actualDeathRate = 0.0

#Save simulation start time...
simulationStartTime = 0

#Saving first simulation name...
simulationName0 = ""

#To save de data during simulation
evolutionData = pd.DataFrame(columns=["Day", "Total infected", "Total tested", "Total deaths", "Total recovered",
									"Infected", "In treatment",
									"Infected in A", "Tested in A", "In treatment in A", "Deaths in A", "Recovered in A",
									"Infected in B", "Tested in B", "In treatment in B", "Deaths in B", "Recovered in B",
									"Infected population %", "Death rate"])
populationData = pd.DataFrame(columns=["Human number", "Age", "Sex", "Family number", "Careful factor", 
									"Social distance", "Death risk"])
virusData = pd.DataFrame(columns=["Human number", "Age", "Sex", "Death risk factor", "Is dead?",
									"Incubation period", "Total illness period", "Was tested?",
									"Had symptoms?", "Was treated?"])

class Simulation():
	"Structuring one epidemic simulation"
	def __init__(self, populationcount, periodindays, simNumber, casesCero, simulationName, govActionsList, \
					govActions, autoIsolationThreshold, psicosisB, psicosisThreshold, psicosisFactor):
		
		if simNumber > 1: #We need to clean some variables
			Simulation.deleteSimulation()
		
		global simulationStartTime
		simulationStartTime = tm.time() #To know how much time a simulation takes
		
		if simNumber == 1: #Some things will be the same in all iterations
			global population
			population = populationcount
			global period
			period = periodindays
			global simulationName0
			simulationName0 = simulationName
			vr.startRiskVariables()
			gov.startColapseVariables()
			gov.setStartCaseCount(govActionsList[0])
			gov.setActionsPeriod(govActionsList[1])
			gov.setActiveIsolation(govActionsList[5])
			gov.setTestingResponseThreshold(govActionsList[7])
			gov.setTestingResponseASThreshold(govActionsList[8])
			global govActionsFailurePeriod
			govActionsFailurePeriod = govActionsList[11]
			print("Saving starting point data...", end="\r")
			gov.saveSimulationConfig(simulationName)
			vr.saveSimulationConfig(simulationName)
			rd.saveSimulationConfig(simulationName)
			print("Starting point data saved!           ", end="\n")
		
		#Now we create the population that will suffer the outbreak.
		Simulation.createHumans(population, casesCero, simulationName, autoIsolationThreshold)

		#Simulating each day, one by one...
		for d in range(period):
			print("Simulating day " + str(d) + "...		", end="\r")
			Simulation.simulateDay()
			Simulation.saveDay(d + 1)
			if psicosisB == True:
				Simulation.checkHumansPsicosis(d, psicosisThreshold, psicosisFactor)
			if govActions == True:
				Simulation.checkGovermentActions(d, govActionsList)
			if d < period:
				Simulation.humanExchange(areaAHumans, areaBHumans)
			
		evolutionData.to_csv("SimulationData/Simulations/" + simulationName + ".csv", index=False)
		virusData.to_csv("SimulationData/Infections/" + simulationName + "_infections.csv", index=False)
		Simulation.saveSimulationConfig(simulationName0, simNumber, casesCero, govActionsStartDay, \
			govActions, psicosisB, psicosisCycles)
			
		print("Simulation Complete!				", end="\n")
		print("Infected: " + str(totalInfected) + ", Recovered: " + str(totalRecovered) + ", Deaths: " +
				str(totalDeaths), end="\n")
		print("Time needed for this simulation: " +
				Simulation.getSimulationTime(simulationStartTime, tm.time()), end="\n")
		
	#####################################################################################################
	#Simulating a day...
	def simulateDay():			
		Simulation.simulateAreaA()
		Simulation.simulateAreaB()
		Simulation.getDeathRate()
		Simulation.getInfectedRatio()
		Simulation.getKnownInfectedRatio()
		
	def simulateAreaA():
		infectedList = Simulation.getInfectedList(areaAHumans)
		for i in range(len(infectedList)):
			index = Simulation.getHumanIndex(areaAHumans, infectedList[i])
			if areaAHumans[index].isIsolated == False:
				areaAHumans[index].contacts = Simulation.setHumanContacts(areaAHumans)
				for f in range (len(areaAHumans[index].family)):
					indexF = Simulation.getHumanIndex(areaAHumans, areaAHumans[index].family[f])
					if areaAHumans[indexF].isInfected == False:
						Simulation.decideInfection(areaAHumans[index], areaAHumans[indexF], "A")
				for c in range (len(areaAHumans[index].contacts)):
					indexC = Simulation.getHumanIndex(areaAHumans, areaAHumans[index].contacts[c])
					if areaAHumans[indexC].isInfected == False:
						Simulation.decideInfection(areaAHumans[index], areaAHumans[indexC], "A")
			Simulation.evolInfection(areaAHumans[index], "A")

	def simulateAreaB():
		infectedList = Simulation.getInfectedList(areaBHumans)
		for i in range(len(infectedList)):
			index = Simulation.getHumanIndex(areaBHumans, infectedList[i])
			if areaBHumans[index].isIsolated == False:
				areaBHumans[index].contacts = Simulation.setHumanContacts(areaBHumans)
				for f in range (len(areaBHumans[index].family)):
					indexF = Simulation.getHumanIndex(areaBHumans, areaBHumans[index].family[f])
					if areaBHumans[indexF].isInfected == False:
						Simulation.decideInfection(areaBHumans[index], areaBHumans[indexF], "B")
				for c in range (len(areaBHumans[index].contacts)):
					indexC = Simulation.getHumanIndex(areaBHumans, areaBHumans[index].contacts[c])
					if areaBHumans[indexC].isInfected == False:
						Simulation.decideInfection(areaBHumans[index], areaBHumans[indexC], "B")
			Simulation.evolInfection(areaBHumans[index], "B")

	#Deciding infection after checking immunity
	def decideInfection(infectedHuman, human, area):
		if human.hasImmunity == False:
			r = rd.aRandom()
			c = rd.isCarefulAverage(infectedHuman, human) * gov.getInfoFactor()
			s = rd.isDistancedAverage(infectedHuman, human) * gov.getSocialDistanceFactor()
			infectionP = r * rd.getInfectionThresholdVar(c, s)
			if infectionP < vr.getInfectionThreshold() *  infectedHuman.contagiousFactor:
				Simulation.setInfection(human, area)

	#Method to make human infected
	def setInfection(human, area):
		human.isInfected = True
		illness = rd.setIllnessDevelopment()
		human.incubationPeriod = illness
		illness += rd.setIllnessDevelopment()
		human.illnessPeriod = illness
		human.evolutionState = 0
		Simulation.increaseV("totalInfected")
		Simulation.increaseV("actualInfected")
		if area == "A":
			Simulation.increaseV("actualAInfected")
		elif area == "B":
			Simulation.increaseV("actualBInfected")

	#Illness evolution	
	def evolInfection(human, area):
		human.evolutionState += 1
		
		#Simulating government tests
		if human.wasTested == False:
			Simulation.decideTest(human, area)

		#Illness evolution...		
		if human.willBeSymptomatic == True:
			if human.evolutionState == human.incubationPeriod: #and human.evolutionState < human.illnessPeriod:
				human.isSymptomatic = True
				if human.autoIsolation == True: #Humans can isolate themselves
						human.isIsolated = True
				if human.willNeedTreatment == True:
					#if human.isInTreatment == False:
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
							Simulation.killHuman(human, area)
						else:
							Simulation.setCure(human, area)
						Simulation.decreaseV("actualInTreatment")
						if area == "A":
							Simulation.decreaseV("actualAInTreatment")
						elif area == "B":
							Simulation.decreaseV("actualBInTreatment")
					elif human.isInTreatment == False:
						Simulation.setCure(human, area)
			if human.evolutionState == human.incubationPeriod + vr.getContagiousShift():
				human.contagiousFactor = 1.0 #Contagious factor can change before of after the symptoms appear
			if human.evolutionState == human.illnessPeriod + vr.getContagiousShift():
				human.contagiousFactor = vr.getBaseASContagiousFactor()
		elif human.willBeSymptomatic == False:
			if human.evolutionState == human.illnessPeriod:
				Simulation.setCure(human, area)

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
			notTestedHuman.wasTested = True
			Simulation.decideActiveIsolation(notTestedHuman)
			Simulation.increaseV("totalTested")
			Simulation.increaseV("actualTested")
			if area == "A":
				Simulation.increaseV("ATested")
			elif area == "B":
				Simulation.increaseV("BTested")
				
	def decideActiveIsolation(human):
		if gov.getActiveIsolation() == True:
			human.isIsolated = True
	
	#Deciding if a human will die
	def decideDeath(human):
		death = False
		d = rd.aRandom()
		d = d * human.deathRiskFactor * gov.treatmentColapseFactor(infectedPopulationRatio, "polynomial")
		if d < vr.getDeathThreshold():
			death = True
		return death
	
	#Method for kill human
	def killHuman(human, area):
		humanNumber = human.humanNumber
		index = 0
		Simulation.increaseV("totalDeaths")
		Simulation.decreaseV("actualInfected")
		Simulation.saveInfection(human, True)
		if human.wasTested == True:
			Simulation.decreaseV("actualTested")
		if area == "A":
			index = Simulation.getHumanIndex(areaAHumans, humanNumber)
			Simulation.cleanFamilyandContacts(areaAHumans, index, humanNumber)
			del areaAHumans[index]
			Simulation.decreaseV("actualAInfected")
			Simulation.increaseV("ADeaths")
		elif area == "B":
			index = Simulation.getHumanIndex(areaBHumans, humanNumber)
			Simulation.cleanFamilyandContacts(areaBHumans, index, humanNumber)
			del areaBHumans[index]
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
	def setHumanContacts(humans):
		contacts = []
		count = rd.setContactsCount(gov.getIsolationFactor())
		if count > 0:
			auxRandoms = rd.aRandomIntList(0, len(humans) - 1, int(count))
			for i in range(len(auxRandoms)):
				contacts.append(Simulation.getHumanNumber(humans, auxRandoms[i]))
		return contacts
	
	#Method to set the cure
	def setCure(human, area):
		human.isInfected = False
		human.hasImmunity = True
		Simulation.increaseV("totalRecovered")
		Simulation.decreaseV("actualInfected")
		Simulation.saveInfection(human, False)
		if human.wasTested == True:
			Simulation.decreaseV("actualTested")
		if area == "A":
			Simulation.increaseV("ARecovered")
			Simulation.decreaseV("actualAInfected")
		elif area == "B":
			Simulation.increaseV("BRecovered")
			Simulation.decreaseV("actualBInfected")
	
	#Setting humans exchange between urban areas
	def humanExchange(areaAH, areaBH):
		if gov.getLockDown() == False:
			areaAExits = rd.setExchangeCount(gov.getIsolationFactor())
			indexesA = rd.aRandomIntList(0, len(areaAH) - 1, areaAExits)
			humanNumbersA = []
			for n in range(len(indexesA)):
				humanNumbersA.append(Simulation.getHumanNumber(areaAH, indexesA[n]))
			for a in range(areaAExits):
				family = areaAH[Simulation.getHumanIndex(areaAH, humanNumbersA[a])].family
				for f in range(len(family)):
					if Simulation.checkInTreatmentFamily(areaAH, family) == False:
						member = Simulation.getHumanIndex(areaAH, family[f])
						areaBH.append(areaAH[member])
						Simulation.correctStatistics("A", areaAH[member])
						del areaAH[member]
			areaBExits = rd.setExchangeCount(gov.getIsolationFactor())
			indexesB = rd.aRandomIntList(0, len(areaBH) - 1, areaBExits)
			humanNumbersB = []
			for n in range(len(indexesB)):
				humanNumbersB.append(Simulation.getHumanNumber(areaBH, indexesB[n]))
			for a in range(areaBExits):
				family = areaBH[Simulation.getHumanIndex(areaBH, humanNumbersB[a])].family
				for f in range(len(family)):
					if Simulation.checkInTreatmentFamily(areaBH, family) == False:
						member = Simulation.getHumanIndex(areaBH, family[f])
						areaAH.append(areaBH[member])
						Simulation.correctStatistics("B", areaBH[member])
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
			index = Simulation.getHumanIndex(humans, familyMembers[f])
			if humans[index].isInTreatment == True:
				inTreatment = True
		return inTreatment
		
	def checkGovermentActions(actualDay, govActionsList):
		if totalTested >= gov.getStartCaseCount():
			global govActionsActive
			if govActionsActive == False:
				govActionsActive = True
				global govActionsStartDay
				govActionsStartDay = actualDay
				Simulation.startGovActions(govActionsList)
			elif govActionsActive == True:
				if govActionsList[9] == True: #Checking if there will be government failures
					if actualDay == govActionsStartDay + govActionsList[10]:
						gov.resetCountermeasures()
						global govActionsFailure
						govActionsFailure = actualDay
					elif actualDay == govActionsStartDay + govActionsList[10] + govActionsList[11]:
						Simulation.startGovActions(govActionsList)
				if actualDay == govActionsStartDay + gov.getActionsPeriod():
					gov.resetCountermeasures()
					global govActionsEndDay
					govActionsEndDay = actualDay
			
	def startGovActions(govActionsList):
		gov.setInfoFactor(govActionsList[2])
		gov.setSocialDistanceFactor(govActionsList[3])
		gov.setIsolationFactor(govActionsList[4])
		gov.setLockDown(govActionsList[6])
	
	def checkHumansPsicosis(d, psicosisThreshold, psicosisFactor):
		global psicosis
		if knownInfectedRatio > psicosisThreshold:
			if psicosis == False:
				Simulation.improveHumans(areaAHumans, areaBHumans, d, psicosisFactor)
				psicosis = True
		elif knownInfectedRatio <= psicosisThreshold:
			if psicosis == True:
				Simulation.resetHumansImprovement(areaAHumans, areaBHumans, d, psicosisFactor)
				psicosis = False
	
	def improveHumans(areaAHumans, areaBHumans, d, psicosisFactor):
		for h in range(len(areaAHumans)):
			areaAHumans[h].carefulFactor = areaAHumans[h].carefulFactor * psicosisFactor
			areaAHumans[h].socialDistanceFactor = areaAHumans[h].socialDistanceFactor * psicosisFactor
		for h in range(len(areaBHumans)):
			areaBHumans[h].carefulFactor = areaBHumans[h].carefulFactor * psicosisFactor
			areaBHumans[h].socialDistanceFactor = areaBHumans[h].socialDistanceFactor * psicosisFactor
		global psicosisCycles
		psicosisCycles.append(d)
		
	def resetHumansImprovement(areaAHumans, areaBHumans, d, psicosisFactor):
		for h in range(len(areaAHumans)):
			areaAHumans[h].carefulFactor = areaAHumans[h].carefulFactor / psicosisFactor
			areaAHumans[h].socialDistanceFactor = areaAHumans[h].socialDistanceFactor / psicosisFactor
		for h in range(len(areaBHumans)):
			areaBHumans[h].carefulFactor = areaBHumans[h].carefulFactor / psicosisFactor
			areaBHumans[h].socialDistanceFactor = areaBHumans[h].socialDistanceFactor / psicosisFactor
		global psicosisCycles
		psicosisCycles.append(d)
		
	######################################################################################################
	#Creating humans and simulation environment
	def createHumans(population, casesCero, simulationName, autoIsolationThreshold):
		
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
			
			#Defining if infected humans will be symptomatic or will need treatment
			auxRandom = rd.aRandom()
			if auxRandom < vr.getSymptomsThreshold() * humans[p].deathRiskFactor * vr.getDeathRiskSymptomsW():
				humans[p].willBeSymptomatic = True
				auxRandom = rd.aRandom()
				if auxRandom < vr.getTreatmentThreshold() * humans[p].deathRiskFactor * vr.getDeathRiskTreatmentW():
					humans[p].willNeedTreatment = True
			
			#Defining if human will isolate himself in case of having symptoms
			auxRandom = rd.aRandom()
			if auxRandom <= autoIsolationThreshold:
				humans[p].autoIsolation = True
			
		print("Creating humans complete!		", end="\n")
		
		Simulation.assignFamilies(humans)
		
		Simulation.assignAreas(humans)
		
		print("Injecting infected human/s in urban area A...", end="\r")
		auxRandoms = rd.aRandomIntList(0, len(areaAHumans) - 1, casesCero)
		for i in range(casesCero):
			Simulation.setInfection(areaAHumans[auxRandoms[i]], "A")		
		print("Infected human/s injected!                        ", end="\n")
		dt.savePopulationData(areaAHumans, areaBHumans, simulationName)
	
	#Defining families for each human
	def assignFamilies(humans):
		count = 0
		actualFamily = 0
		print("Assigning families...       ", end="\r")
		while count < len(humans):
			members = rd.setFamilySize()
			for i in range(members):
				if i + count < len(humans):
					humans[i + count].familyNumber = actualFamily
					humans[count].family.append(i + count)
			if members > 1:
				for i in range(members - 1):
					if i + count + 1 < len(humans):
						humans[count + i + 1].family = humans[count].family
			count += members
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
					p += 1
			else:
				for f in range(len(humans[p].family)):
					areaBHumans.append(humans[p])
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
		index = -1
		for i in range(len(humans)):
			if humans[i].humanNumber == humanNumber:
				index = i
				break
		return index
	
	def getHumanNumber(humans, index):
		humanNumber = humans[index].humanNumber
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
		
	def getDeathRate():
		global actualDeathRate
		actualDeathRate = totalDeaths / totalInfected
	
	def saveDay(day):
		global evolutionData
		auxRow = pd.DataFrame([[day, totalInfected, totalTested, totalDeaths, totalRecovered, actualInfected,
								actualInTreatment, actualAInfected,	ATested, actualAInTreatment,
								ADeaths, ARecovered, actualBInfected, BTested, actualBInTreatment,
								BDeaths, BRecovered, round(infectedPopulationRatio, 5), round(actualDeathRate, 5)]],
								columns=["Day", "Total infected", "Total tested", "Total deaths", "Total recovered",
									"Infected", "In treatment", "Infected in A", "Tested in A",
									"In treatment in A", "Deaths in A", "Recovered in A","Infected in B",
									"Tested in B", "In treatment in B", "Deaths in B", "Recovered in B",
									"Infected population %", "Death rate"])
		evolutionData = pd.concat([evolutionData, auxRow])

	def saveInfection(human, isDead):
		global virusData
		auxRow = pd.DataFrame([[human.humanNumber, human.age, human.sex, human.deathRiskFactor, isDead,
								human.incubationPeriod, human.illnessPeriod, human.wasTested,
								human.willBeSymptomatic, human.willNeedTreatment]],
								columns=["Human number", "Age", "Sex", "Death risk factor", "Is dead?",
									"Incubation period", "Total illness period", "Was tested?",
									"Had symptoms?", "Was treated?"])
		virusData = pd.concat([virusData, auxRow])
	
	def saveSimulationConfig(simulationName, sinNumber, casesCero, govActionsStartDay, govActions, psicosisB, psicosisC):
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
				startConfig.write(str(sinNumber) + ". Government actions started in day " + str(govActionsStartDay) +
						" and finished in day " + str(govActionsEndDay) + "\n")
		if psicosisB == True:
			startConfig.write(str(sinNumber) + ". Population psicosis cycles:" + str(psicosisC) + "\n")

	#Deleting data and humans to run a new simulation
	def deleteSimulation():
		print("Deleting humans from previous population...", end="\r")
		areaAHumans.clear()
		areaBHumans.clear()
		Simulation.restartV()
		print("Humans from previous population deleted!        ", end="\n")
		print("Erasing previous simulation data...", end="\r")
		global evolutionData
		evolutionData.drop(evolutionData.index, inplace=True)
		global virusData
		virusData.drop(virusData.index, inplace=True)
		print("Previous simulation data erased!             ", end="\n")
	
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
	
	def getGovActionsStartDay():
		return govActionsStartDay
	
	def getGovActionsEndDay():
		return govActionsEndDay
		
	def getGovActionsFailure():
		return govActionsFailure
	
	def getGovActionsFailurePeriod():
		return govActionsFailurePeriod
	
	def getPsicosisCycles():
		global psicosisCycles
		length = len(psicosisCycles)
		if length % 2 != 0:
			psicosisCycles.append(period)
		return psicosisCycles
	
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
		global actualInfected
		actualInfected = 0
		global actualInTreatment
		actualInTreatment = 0
		global actualAInfected
		actualAInfected = 0
		global actualTested
		actualTested = 0
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
		global govActionsStartDay
		govActionsStartDay = -1
		global govActionsEndDay
		govActionsEndDay = -1
		global govActionsActive
		govActionsActive = False
		global govActionsFailure
		govActionsFailure = -1
		global govActionsFailurePeriod
		govActionsFailurePeriod = -1

	#Simple methods to increase or decrease global variables
	def increaseV(vName):
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
		if vName == "actualInfected":
			global actualInfected
			actualInfected += 1
		if vName == "actualInTreatment":
			global actualInTreatment
			actualInTreatment += 1
		if vName == "actualTested":
			global actualTested
			actualTested += 1
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
	
	def decreaseV(vName):
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
		if vName == "actualInfected":
			global actualInfected
			actualInfected -= 1
		if vName == "actualInTreatment":
			global actualInTreatment
			actualInTreatment -= 1
		if vName == "actualTested":
			global actualTested
			actualTested -= 1
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