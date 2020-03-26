from matplotlib.pyplot import figure
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator

populationFile = ""
simulationFile = ""

class Visualization():

	def getFileNames(simulationName):
		global populationFile
		populationFile = "SimulationData/" + simulationName + "_population"
		global simulationFile
		simulationFile = "SimulationData/" + simulationName
	
	def loadSimulationFile(simulationData):
		simulationDFrame = pd.read_csv(simulationData)
		return simulationDFrame
	
	def loadPopulationFile(populationData):
		populationDFrame = pd.read_csv(populationData)
		return populationDFrame
	
	def simulationVisualization(simulationName):
		Visualization.getFileNames(simulationName)
		simulationData = Visualization.loadPopulationFile(simulationFile + ".csv")
				
		figure = plt.figure(num=None, figsize=(8, 6), dpi=150, facecolor='w', edgecolor='k')
		plt.subplot2grid((3, 2), (0, 0), colspan=2)
		total = simulationData["Total infected"].plot(kind="line", linewidth=1.5, color="orange", label="Total infected")
		total = simulationData["Total deaths"].plot(kind="line", linewidth=1.5, color="tab:red", label="Total deaths")
		total = simulationData["Total tested"].plot(kind="line", linewidth=1.5, color="tab:blue", label="Tested")
		total = simulationData["Total recovered"].plot(kind="line", linewidth=1.5, color="limegreen", label="Recovered")
		total.legend()
		total.set_title("Total cases")
		total.set_ylabel("")
		plt.subplot2grid((3, 2), (1, 0))
		actual = simulationData["Infected"].plot(kind="line", linewidth=1.5, color="orange", label="Total")
		actual = simulationData["Infected in A"].plot(kind="line", linewidth=1.5, color="indianred", label="Area A")
		actual = simulationData["Infected in B"].plot(kind="line", linewidth=1.5, color="teal", label="Area B")
		actual.legend()
		actual.set_title("Actual infected patients")
		actual.set_ylabel("")
		plt.subplot2grid((3, 2), (1, 1))
		treatment = simulationData["In treatment"].plot(kind="line", linewidth=1.5, color="orange", label="Total")
		treatment = simulationData["In treatment in A"].plot(kind="line", linewidth=1.5, color="indianred", label="Area A")
		treatment = simulationData["In treatment in B"].plot(kind="line", linewidth=1.5, color="teal", label="Area B")
		treatment.legend()
		treatment.set_title("Patients in treatment")
		treatment.set_ylabel("")
		plt.subplot2grid((3, 2), (2, 0))
		deathrate = simulationData["Death rate"].plot(kind="line", linewidth=1.5, color="indianred")
		deathrate.set_ylabel("")
		deathrate.set_title("Death rate evolution")
		plt.subplot2grid((3, 2), (2, 1))
		infectedratio = simulationData["Infected population %"].plot(kind="line", linewidth=1.5, color="teal")
		infectedratio.set_ylabel("")
		infectedratio.set_title("Infected population %")
		plt.tight_layout()
		plt.savefig("SimulationPlots/" + simulationName + ".png")
	
	def populationVisualization(simulationName):
		Visualization.getFileNames(simulationName)
		populationData = Visualization.loadPopulationFile(populationFile + ".csv")
				
		figure = plt.figure(num=None, figsize=(8, 6), dpi=150)
		plt.subplot2grid((4, 4), (0, 0), colspan=2, rowspan=5)
		ageDistribution = populationData["Age"].plot(kind="hist", bins=50, color="tab:blue", title="Age distribution")
		ageDistribution.set_ylabel("")
		plt.subplot2grid((4, 4), (0, 2))
		symptoms = populationData["Symptomatic"].value_counts().plot(kind="barh", title="Symptomatic", color="orange")
		symptoms.set_ylabel("")
		plt.subplot2grid((4, 4), (0, 3))
		treatment = populationData["Severe illness"].value_counts().plot(kind="barh", title="Sever illness", color="orangered")
		treatment.set_ylabel("")
		plt.subplot2grid((4, 4), (1, 2), colspan=2)
		careful = populationData["Careful factor"].plot(kind="hist", bins=50, title="Careful factor", color="teal")
		careful.set_ylabel("")
		plt.subplot2grid((4, 4), (2, 2), colspan=2)
		socialDistance = populationData["Social distance factor"].plot(kind="hist", bins=50, title="Social distance factor", color="teal")
		socialDistance.set_ylabel("")
		plt.subplot2grid((4, 4), (3, 2), colspan=2)	
		deathRisk = populationData["Death risk factor"].plot(kind="hist", bins=50, title="Death risk factor", color="teal")
		deathRisk.set_ylabel("")	
		plt.tight_layout()
		plt.savefig("SimulationPlots/" + simulationName + "_population.png")