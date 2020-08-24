import pandas as pd
import matplotlib.pyplot as plt

populationFile = ""
simulationFile = ""
infectionsFile = ""

#Let's make this charts beautiful
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font 
backgroundPlot = "lightgray" #Default background color for charts
backgroundFigure = "gainsboro" #Default background color for figures
majorGridColor = "dimgrey" #Default colors for grids...
minorGridColor = "dimgray"
alphaMGC = 0.7
alphamGC = 0.9
imageResolution = 150
widthBig = 2.5
widthNormal = 2.0
widthSmall = 1.5
plotColors = ["orange", "tab:red", "tab:blue", "limegreen", "indianred", "teal", "darkslategray", \
			"mediumseagreen", "orangered", "goldenrod", "dimgrey", "whitesmoke"]
paintColors = ["seagreen", "tab:red"]

class Visualization():

	def getFileNames(simulationName):
		global populationFile
		populationFile = "SimulationData/Population/" + simulationName + "_population"
		global simulationFile
		simulationFile = "SimulationData/Simulations/" + simulationName
		global infectionsFile
		infectionsFile = "SimulationData/Infections/" + simulationName + "_infections"
	
	def loadFile(fileName):
		dataFrame = pd.read_csv(fileName)
		return dataFrame
	
	def gridsAndBackground():
		plt.grid(which='both', axis='both')
		plt.minorticks_on()
		plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
		plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		plt.gca().set_facecolor(backgroundPlot)
	
	def xgridAndBackground():
		plt.grid(which='both', axis='x')
		plt.minorticks_on()
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		plt.gca().set_facecolor(backgroundPlot)
	
	def background():
		plt.xticks(fontsize=8)
		plt.yticks(fontsize=8)
		plt.gca().set_facecolor(backgroundPlot)
	
	def getyLimit(population, maxvalue):
		ylim = []
		ylim.append(0)
		limit = population
		while limit < maxvalue:
			limit += population
		ylim.append(limit)
		return ylim
	
	def simulationVisualization(simulationName, govActions, govActionsCycles, psicosis, psicosisCycles, simulationsPopulation):
		simulationData = Visualization.loadFile(simulationFile + ".csv")			
		figure = plt.figure(num=None, figsize=(9, 6), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
		figure.suptitle("Results for " + simulationName, fontsize=13, fontname=defaultFont)
		plt.subplot2grid((3, 2), (0, 0), colspan=2)
		total = simulationData["Total infected"].plot(kind="line", linewidth=widthBig, color=plotColors[0], label="Total infected")
		total = simulationData["Total deaths"].plot(kind="line", linewidth=widthBig, color=plotColors[1], label="Total deaths")
		total = simulationData["Total tested"].plot(kind="line", linewidth=widthBig, color=plotColors[2], label="Tested")
		total = simulationData["Total recovered"].plot(kind="line", linewidth=widthBig, color=plotColors[3], label="Recovered")
		total.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 8})
		total.set_title("Total cases", fontsize=10, fontname=defaultFont)
		total.set_ylabel("")
		maxinfected = simulationData["Total infected"].max()
		ylim = Visualization.getyLimit(simulationsPopulation, maxinfected)
		total.set_ylim(ylim[0], ylim[1])
		Visualization.gridsAndBackground()
		plt.subplot2grid((3, 2), (1, 0))
		actual = simulationData["Infected"].plot(kind="line", linewidth=widthNormal, color=plotColors[0], label="Total")
		actual = simulationData["Infected in A"].plot(kind="line", linewidth=widthNormal, color=plotColors[4], label="Area A")
		actual = simulationData["Infected in B"].plot(kind="line", linewidth=widthNormal, color=plotColors[5], label="Area B")
		actual = simulationData["Actual tested"].plot(kind="line", linewidth=widthNormal, color=plotColors[7], label="Tested")
		actual.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 8})
		actual.set_title("Actual infected patients", fontsize=10, fontname=defaultFont)
		actual.set_ylabel("")
		if govActions == True:
			Visualization.paintGovActions(govActionsCycles)
		if psicosis == True:
			Visualization.paintPsicosis(psicosisCycles)
		Visualization.gridsAndBackground()
		plt.subplot2grid((3, 2), (1, 1))
		auxlist = simulationData["Total infected"].values.tolist()
		newcases = Visualization.getNewCases(auxlist)
		newcasesav = Visualization.getNewCasesAv(newcases)
		plt.plot(newcases, label="Daily count", linewidth=widthSmall, alpha=0.4, color=plotColors[6])
		plt.plot(newcasesav, label="7 day average", linewidth=widthBig, color=plotColors[0])
		if govActions == True:
			Visualization.paintGovActions(govActionsCycles)
		if psicosis == True:
			Visualization.paintPsicosis(psicosisCycles)
		plt.title("New cases", fontsize=10, fontname=defaultFont)
		plt.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 8})
		Visualization.gridsAndBackground()
		plt.subplot2grid((3, 2), (2, 0))
		treatment = simulationData["In treatment"].plot(kind="line", linewidth=widthNormal, color=plotColors[0], label="Total")
		treatment = simulationData["In treatment in A"].plot(kind="line", linewidth=widthNormal, color=plotColors[4], label="Area A")
		treatment = simulationData["In treatment in B"].plot(kind="line", linewidth=widthNormal, color=plotColors[5], label="Area B")
		treatment.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 8})
		treatment.set_title("Patients in treatment", fontsize=10, fontname=defaultFont)
		treatment.set_ylabel("")
		if govActions == True:
			Visualization.paintGovActions(govActionsCycles)
		if psicosis == True:
			Visualization.paintPsicosis(psicosisCycles)
		Visualization.gridsAndBackground()
		plt.subplot2grid((3, 2), (2, 1))
		immunity = simulationData["Population immunity %"].plot(kind="line", linewidth=widthBig, color=plotColors[7], label="Immunity ratio")
		immunity.set_ylim(0, 1)
		Visualization.xgridAndBackground()
		deathrate = immunity.twinx()
		deathrate = simulationData["Death rate"].plot(kind="line", linewidth=widthBig, color=plotColors[4], label="Death rate")
		deathrate.set_ylabel("")
		Visualization.xgridAndBackground()
		dr, drl = deathrate.get_legend_handles_labels()
		im, iml = immunity.get_legend_handles_labels()
		deathrate.legend(dr + im, drl + iml, loc=2, shadow = True,
			facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 8})
		deathrate.set_title("Immunity & death rate", fontsize=10, fontname=defaultFont)
		plt.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("SimulationPlots/Simulations/" + simulationName + ".png", facecolor=figure.get_facecolor())
	
	def infectionsVisualization(simulationName, period, govActions, govActionsCycles, psicosis, psicosisCycles):
		infectionsData = Visualization.loadFile(infectionsFile + ".csv")		
		figure = plt.figure(num=None, figsize=(9, 6), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
		figure.suptitle("Infections in " + simulationName, fontsize=13, fontname=defaultFont)
		plt.subplot2grid((4, 4), (0, 0), colspan=2)
		incubation = infectionsData["Incubation period"].plot(kind="hist", bins=8, color=plotColors[2])
		incubation.set_title("Incubation periods distribution", fontsize=10, fontname=defaultFont)
		incubation.set_ylabel("")
		Visualization.background()
		plt.subplot2grid((4, 4), (0, 2), colspan=2)
		illness = infectionsData["Total illness period"].plot(kind="hist", bins=12, color=plotColors[2])
		illness.set_title("Total illness periods distribution", fontsize=10, fontname=defaultFont)
		illness.set_ylabel("")
		Visualization.background()
		plt.subplot2grid((4, 4), (1, 0))
		tested = infectionsData["Was tested?"].value_counts().plot(kind="barh", color=plotColors[7])
		tested.set_ylabel("")
		tested.set_title("Was a confirmed case?", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 4), (1, 1))
		deaths = infectionsData["Is dead?"].value_counts().plot(kind="barh", color=plotColors[4])
		deaths.set_ylabel("")
		deaths.set_title("Had died?", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 4), (1, 2))
		symptoms = infectionsData["Had symptoms?"].value_counts().plot(kind="barh", color=plotColors[9])
		symptoms.set_ylabel("")
		symptoms.set_title("Had symptoms?", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 4), (1, 3))
		treatment = infectionsData["Was treated?"].value_counts().plot(kind="barh", color=plotColors[4])
		treatment.set_ylabel("")
		treatment.set_title("Was treated?", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 4), (2, 0), colspan=4, rowspan=2)
		tSymptomatic = infectionsData[infectionsData["Had symptoms?"]==True]
		tAsymptomatic = infectionsData[infectionsData["Had symptoms?"]==False]
		transmission = plt.scatter(tAsymptomatic["Infection date"], tAsymptomatic["Transmission"], s=15, \
						color=plotColors[11], alpha=0.5)
		transmission = plt.scatter(tSymptomatic["Infection date"], tSymptomatic["Transmission"], s=20, \
						color=plotColors[10], alpha=0.5)
		transmissionAv = Visualization.getTransmissionAv(infectionsData, tSymptomatic, tAsymptomatic, period)
		transmission = plt.plot(transmissionAv["Symptomatic"], linewidth=2.5, color=plotColors[4], alpha=1.0)
		transmission = plt.plot(transmissionAv["Asymptomatic"], linewidth=2.5, color=plotColors[2], alpha=1.0)
		transmission = plt.plot(transmissionAv["Total"], linestyle=":", linewidth=1.5, color=plotColors[10], alpha=1.0)
		plt.xlim(1,period)
		plt.ylabel("")
		plt.title("Infected humans transmission (symptomatic vs asymptomatic)", fontsize=10, fontname=defaultFont)
		Visualization.background()
		if govActions == True:
			Visualization.paintGovActions(govActionsCycles)
		if psicosis == True:
			Visualization.paintPsicosis(psicosisCycles)
		Visualization.background()
		plt.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("SimulationPlots/Infections/" + simulationName + "_infections.png", facecolor=figure.get_facecolor())
	
	def populationVisualization(simulationName):
		populationData = Visualization.loadFile(populationFile + ".csv")		
		figure = plt.figure(num=None, figsize=(8, 6), dpi=imageResolution, facecolor=backgroundFigure)
		figure.suptitle("Population summary: " + simulationName, fontsize=13, fontname=defaultFont)
		plt.subplot2grid((4, 2), (0, 0), rowspan=4)
		ageDistribution = populationData["Age"].plot(kind="hist", bins=50, color=plotColors[2])
		ageDistribution.set_ylabel("")
		ageDistribution.set_title("Age distribution", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 2), (0, 1))
		careful = populationData["Careful factor"].plot(kind="hist", bins=50, color=plotColors[5])
		careful.set_ylabel("")
		careful.set_title("Careful factor", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 2), (1, 1))
		socialDistance = populationData["Social distance factor"].plot(kind="hist", bins=50, color=plotColors[5])
		socialDistance.set_ylabel("")
		socialDistance.set_title("Social distance factor", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.subplot2grid((4, 2), (2, 1), rowspan=2)	
		deathRisk = populationData["Death risk factor"].plot(kind="hist", bins=50, color=plotColors[4])
		deathRisk.set_ylabel("")
		deathRisk.set_title("Death risk factor", fontsize=10, fontname=defaultFont)
		Visualization.background()
		plt.tight_layout(rect=[0, 0.03, 1, 0.95])
		plt.savefig("SimulationPlots/Population/" + simulationName + "_population.png", facecolor=figure.get_facecolor())
	
	def paintGovActions(govActionsCycles):
		for p in range(int(len(govActionsCycles)/2)):
			plt.axvspan(govActionsCycles[2*p], govActionsCycles[2*p+1], edgecolor="none", alpha=0.3, facecolor=paintColors[0])
			
	def paintPsicosis(psicosisCycles):
		limits = plt.ylim()
		for p in range(int(len(psicosisCycles)/2)):
			plt.fill_between([psicosisCycles[2*p], psicosisCycles[2*p+1]], limits[1]*0.9, limits[1], \
							edgecolor="none", alpha=0.9, facecolor=paintColors[1], zorder=2)
	
	def getNewCases(datalist):
		ls = []
		ls.append(datalist[0])
		for e in range(len(datalist) - 1):
			ls.append(datalist[e+1] - datalist[e])
		return ls

	def getNewCasesAv(datalist):
		ls = []
		ls.append(None)
		ls.append(None)
		ls.append(None)
		for e in range(len(datalist) - 6):
			ls.append((datalist[e+6] + datalist[e+5] + datalist[e+4] + datalist[e+3] + datalist[e+2] + datalist[e+1] + datalist[e])/7)
		index = len(datalist)
		ls.append(None)
		ls.append(None)
		ls.append(None)
		return ls
	
	def getTransmissionAv(iData, symptomatic, asymptomatic, period):
		transmissionAv = pd.DataFrame(index=range(1,period+1), columns=["Symptomatic", "Asymptomatic", "Total"])
		transmissionAv["Total"] = iData.groupby(by="Infection date")["Transmission"].mean()
		transmissionAv["Symptomatic"] = symptomatic.groupby(by="Infection date")["Transmission"].mean()
		transmissionAv["Asymptomatic"] = asymptomatic.groupby(by="Infection date")["Transmission"].mean()
		return transmissionAv