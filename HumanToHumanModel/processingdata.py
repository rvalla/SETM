import pandas as pd

class ProcessingData():
	"Functions to process, print and save simulations' data"
	
	def printHuman(human):
		print("_________________")
		print("-- Human number: " + str(human.humanNumber) + "	Family number: " +
				str(human.familyNumber))
		print("-- Age: " + str(human.age) +  "	" + "Sex: " + str(human.sex))
		print("-- Infected: " + str(human.isInfected) + " Was tested?: " + str(human.wasTested))
		print("-- Infection data: " + str(human.incubationPeriod) + ", " +
				str(human.illnessPeriod) + ", " + str(human.evolutionState))
		print("-- Variable factors: " + str(round(human.carefulFactor, 2)) + ", " +
				str(round(human.socialDistanceFactor, 2)) + ", " + str(round(human.deathRiskFactor, 2)))
		print("-- Will need treatment: " + str(human.willNeedTreatment) + ", Will be Symptomatic: " +
				str(human.willBeSymptomatic))
		print("-- Is symptomatic: " + str(human.isSymptomatic) + ", Contagious factor: " +
				str(human.contagiousFactor))
	
	def savePopulationData(areaAHumans, areaBHumans, simulationName):
		populationData = pd.DataFrame([[areaAHumans[0].humanNumber, areaAHumans[0].age, str(areaAHumans[0].sex),
							areaAHumans[0].familyNumber, areaAHumans[0].carefulFactor,
							areaAHumans[0].socialDistanceFactor, areaAHumans[0].deathRiskFactor,
							areaAHumans[0].willBeSymptomatic, areaAHumans[0].willNeedTreatment, "A"]],
							columns=["Number", "Age", "Sex", "Family number", "Careful factor",
							"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
							"Urban area"])
		for h in range(len(areaAHumans)-1):
			newRow = pd.DataFrame([[areaAHumans[h + 1].humanNumber, areaAHumans[h + 1].age, str(areaAHumans[h + 1].sex),
						areaAHumans[h + 1].familyNumber, areaAHumans[h + 1].carefulFactor, areaAHumans[h + 1].socialDistanceFactor,
						areaAHumans[h + 1].deathRiskFactor, areaAHumans[h + 1].willBeSymptomatic,
						areaAHumans[h + 1].willNeedTreatment, "A"]],
						columns=["Number", "Age", "Sex", "Family number", "Careful factor",
						"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
						"Urban area"])
			populationData = pd.concat([populationData, newRow])
		for h in range(len(areaBHumans)):
			newRow = pd.DataFrame([[areaBHumans[h].humanNumber, areaBHumans[h].age, str(areaBHumans[h].sex),
						areaBHumans[h].familyNumber, areaBHumans[h].carefulFactor, areaBHumans[h].socialDistanceFactor,
						areaBHumans[h].deathRiskFactor, areaBHumans[h].willBeSymptomatic,
						areaBHumans[h].willNeedTreatment, "B"]],
						columns=["Number", "Age", "Sex", "Family number", "Careful factor",
						"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
						"Urban area"])
			populationData = pd.concat([populationData, newRow])
		populationData.sort_values(by=["Number"], inplace=True)
		populationData.to_csv("SimulationData/" + simulationName + "_population.csv", index=False)