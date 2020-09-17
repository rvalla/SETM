class ProcessingData():
	"Functions to process, print and save simulations data"

	def saveConfigStart(population, period, simulationName, areaBDensity, govB, govActions, govFailure, \
			autoIsolationThreshold, startingImmunity, behaviorB, behaviorTrigger, behaviorOff, behaviorFactor):
		startConfig = open("SimulationData/" + simulationName + ".txt", "a")
		startConfig.write("#################################" + "\n")
		startConfig.write("SIMPLE EPIDEMIC TRANSMISION MODEL" + "\n")
		startConfig.write("Human to human disease simulation" + "\n")
		startConfig.write("---------------------------------" + "\n")
		startConfig.write("---https://github/rvalla/SETM----" + "\n")
		startConfig.write("#################################" + "\n")
		startConfig.write("" + "\n")
		startConfig.write(simulationName + "\n")
		startConfig.write("Population: " + str(population) + "\n")
		startConfig.write("Period in days: " + str(period) + "\n")
		startConfig.write("Area B population density (relative to area A): " + str(areaBDensity) + "\n")
		startConfig.write("Humans auto isolation threshold: " + str(autoIsolationThreshold) + "\n")
		startConfig.write("Population immunity when simulation starts: " + str(startingImmunity) + "%\n")
		if behaviorB == True:
			startConfig.write("Humans behavior trigger threshold: " + str(behaviorTrigger) + "\n")
			startConfig.write("Humans behavior off threshold: " + str(behaviorOff) + "\n")
			startConfig.write("Humans behavior improvement factor: " + str(behaviorFactor) + "\n")
		startConfig.write("" + "\n")
		if govB == True:
			startConfig.write("----Government actions" + "\n")
			if govActions[0] == "normal":
				startConfig.write("Government actions mode: normal" + "\n")
				startConfig.write("startCaseCount: " + str(govActions[3]) + "\n")
				startConfig.write("actionsPeriod: " + str(govActions[4]) + "\n")
				if govFailure[0] == True:
					startConfig.write("Government failure moment: " + str(govFailure[1]) + "\n")
					startConfig.write("Government failure period: " + str(govFailure[2]) + "\n")
			if govActions[0] == "auto":
				startConfig.write("Government actions mode: auto" + "\n")
				startConfig.write("Auto trigger threshold: " + str(govActions[1]) + "\n")
				startConfig.write("Auto Off threshold: " + str(govActions[2]) + "\n")
			startConfig.write("infoFactor: " + str(govActions[5]) + "\n")
			startConfig.write("socialDistanceFactor: " + str(govActions[6]) + "\n")
			startConfig.write("isolationFactor: " + str(govActions[7]) + "\n")
			startConfig.write("exchangeFactor: " + str(govActions[8]) + "\n")
			startConfig.write("lockDown: " + str(govActions[9]) + "\n")
			startConfig.write("" + "\n")
		startConfig.close()
	
	def savePopulationData(areaAHumans, areaBHumans, simulationName):
		print("Saving population data...", end="\r")
		populationData = pd.DataFrame([[areaAHumans[0].humanNumber, areaAHumans[0].age, str(areaAHumans[0].sex),
							areaAHumans[0].familyNumber, areaAHumans[0].autoIsolation, areaAHumans[0].carefulFactor,
							areaAHumans[0].socialDistanceFactor, areaAHumans[0].deathRiskFactor,
							areaAHumans[0].willBeSymptomatic, areaAHumans[0].willNeedTreatment, "A"]],
							columns=["Number", "Age", "Sex", "Family number", "Auto isolation", "Careful factor",
							"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
							"Urban area"])
		for h in range(len(areaAHumans)-1):
			newRow = pd.DataFrame([[areaAHumans[h + 1].humanNumber, areaAHumans[h + 1].age, str(areaAHumans[h + 1].sex),
						areaAHumans[h + 1].familyNumber, areaAHumans[0].autoIsolation, areaAHumans[h + 1].carefulFactor,
						areaAHumans[h + 1].socialDistanceFactor, areaAHumans[h + 1].deathRiskFactor,
						areaAHumans[h + 1].willBeSymptomatic, areaAHumans[h + 1].willNeedTreatment, "A"]],
						columns=["Number", "Age", "Sex", "Family number", "Auto isolation", "Careful factor",
						"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
						"Urban area"])
			populationData = pd.concat([populationData, newRow])
		for h in range(len(areaBHumans)):
			newRow = pd.DataFrame([[areaBHumans[h].humanNumber, areaBHumans[h].age, str(areaBHumans[h].sex),
						areaBHumans[h].familyNumber, areaBHumans[h].autoIsolation, areaBHumans[h].carefulFactor,
						areaBHumans[h].socialDistanceFactor, areaBHumans[h].deathRiskFactor,
						areaBHumans[h].willBeSymptomatic, areaBHumans[h].willNeedTreatment, "B"]],
						columns=["Number", "Age", "Sex", "Family number", "Auto isolation", "Careful factor",
						"Social distance factor", "Death risk factor", "Symptomatic", "Severe illness",
						"Urban area"])
			populationData = pd.concat([populationData, newRow])
		populationData.sort_values(by=["Number"], inplace=True)
		populationData.to_csv("SimulationData/Population/" + simulationName + "_population.csv", index=False)
		print("Population data saved to SimulationData/Population/" + simulationName + "_population.csv", end="\n")