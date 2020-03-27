from matplotlib.pyplot import figure
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator

populationFile = ""
simulationFile = ""

class Visualization():

	def getFileNames(simulationName):
		global populationFile
		populationFile = "SimulationData/Population/" + simulationName + "_population"
		global simulationFile
		simulationFile = "SimulationData/Simulations/" + simulationName
	
	def loadFile(fileName):
		dataFrame = pd.read_csv(fileName)
		return dataFrame
	
	def simulationVisualization(simulationName):
		Visualization.getFileNames(simulationName)
		simulationData = Visualization.loadFile(simulationFile + ".csv")
				
		figure = plt.figure(num=None, figsize=(9, 6), dpi=150, facecolor='w', edgecolor='k')
		figure.suptitle("Results for " + simulationName, fontsize=13)
		plt.subplot2grid((3, 2), (0, 0), colspan=2)
		total = simulationData["Total infected"].plot(kind="line", linewidth=2.0, color="orange", label="Total infected")
		total = simulationData["Total deaths"].plot(kind="line", linewidth=2.0, color="tab:red", label="Total deaths")
		total = simulationData["Total tested"].plot(kind="line", linewidth=2.0, color="tab:blue", label="Tested")
		total = simulationData["Total recovered"].plot(kind="line", linewidth=2.0, color="limegreen", label="Recovered")
		total.legend(loc=2, prop={'size': 8})
		total.set_title("Total cases", fontsize=10)
		total.set_ylabel("")
		plt.subplot2grid((3, 2), (1, 0))
		actual = simulationData["Infected"].plot(kind="line", linewidth=1.5, color="orange", label="Total")
		actual = simulationData["Infected in A"].plot(kind="line", linewidth=1.5, color="indianred", label="Area A")
		actual = simulationData["Infected in B"].plot(kind="line", linewidth=1.5, color="teal", label="Area B")
		actual.legend(loc=2, prop={'size': 8})
		actual.set_title("Actual infected patients", fontsize=10)
		actual.set_ylabel("")
		plt.subplot2grid((3, 2), (1, 1))
		treatment = simulationData["In treatment"].plot(kind="line", linewidth=1.5, color="orange", label="Total")
		treatment = simulationData["In treatment in A"].plot(kind="line", linewidth=1.5, color="indianred", label="Area A")
		treatment = simulationData["In treatment in B"].plot(kind="line", linewidth=1.5, color="teal", label="Area B")
		treatment.legend(loc=2, prop={'size': 8})
		treatment.set_title("Patients in treatment", fontsize=10)
		treatment.set_ylabel("")
		plt.subplot2grid((3, 2), (2, 0))
		deathrate = simulationData["Death rate"].plot(kind="line", linewidth=2.0, color="indianred")
		deathrate.set_ylabel("")
		deathrate.set_title("Death rate evolution", fontsize=10)
		plt.subplot2grid((3, 2), (2, 1))
		infectedratio = simulationData["Infected population %"].plot(kind="line", linewidth=2.0, color="teal")
		infectedratio.set_ylabel("")
		infectedratio.set_title("Infected population %", fontsize=10)
		plt.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("SimulationPlots/Simulations/" + simulationName + ".png")
	
	def populationVisualization(simulationName):
		Visualization.getFileNames(simulationName)
		populationData = Visualization.loadFile(populationFile + ".csv")
				
		figure = plt.figure(num=None, figsize=(8, 6), dpi=150)
		figure.suptitle("Population summary: " + simulationName, fontsize=13)
		plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=5)
		ageDistribution = populationData["Age"].plot(kind="hist", bins=50, color="tab:blue")
		ageDistribution.set_ylabel("")
		ageDistribution.set_title("Age distribution", fontsize=10)
		plt.subplot2grid((4, 4), (0, 2))
		symptoms = populationData["Symptomatic"].value_counts().plot(kind="barh", color="orange")
		symptoms.set_ylabel("")
		symptoms.set_title("Symptomatic", fontsize=10)
		plt.subplot2grid((4, 4), (0, 3))
		treatment = populationData["Severe illness"].value_counts().plot(kind="barh", color="orangered")
		treatment.set_ylabel("")
		treatment.set_title("Sever illness", fontsize=10)
		plt.subplot2grid((4, 4), (1, 2), colspan=2)
		careful = populationData["Careful factor"].plot(kind="hist", bins=50, color="teal")
		careful.set_ylabel("")
		careful.set_title("Careful factor", fontsize=10)
		plt.subplot2grid((4, 4), (2, 2), colspan=2)
		socialDistance = populationData["Social distance factor"].plot(kind="hist", bins=50, color="teal")
		socialDistance.set_ylabel("")
		socialDistance.set_title("Social distance factor", fontsize=10)
		plt.subplot2grid((4, 4), (3, 2), colspan=2)	
		deathRisk = populationData["Death risk factor"].plot(kind="hist", bins=50, color="teal")
		deathRisk.set_ylabel("")
		deathRisk.set_title("Death risk factor", fontsize=10)
		plt.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("SimulationPlots/Population/" + simulationName + "_population.png")