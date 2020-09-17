class Human():
	"Human being modelling for epidemic simulations"
	
	def __init__(self, humanNumber):
	
		self.humanNumber = humanNumber
		self.infectionNumber = 0
		
		#Defining some human characteristics
		self.age = 0
		self.sex = '?'
		
		#Possible infection targets
		self.familyNumber = 0
		self.family = []
		self.contacts = []
		self.contactsHistory = set()
		
		#Risk evaluation...
		self.carefulFactor = 1.0
		self.socialDistanceFactor = 1.0
		self.deathRiskFactor = 1.0
		self.isIsolated = False
		self.autoIsolation = False #If True, the human will isolate himself when the symptoms appear
	
		#Variables to manage the disease
		self.isInfected = False
		self.willBeSymptomatic = False
		self.isSymptomatic = False
		self.hasImmunity = False
		self.isRecovered = False
		self.willNeedTreatment = False
		self.isInTreatment = False
		self.incubationPeriod = 0
		self.illnessPeriod = 0
		self.evolutionState = 0
		self.contagiousFactor = 0.15 #Probability of infect others depends on the presence of symptoms
		
		#Variables to manage post disease
		self.hasImmunity = False
		self.infectionDate = 0 #Day in which human's infection occur
		self.endDate = 0 #Day in which human's infection ended
		self.transmission = 0 #Number of other humans infected
		
		#Boolean to define if human was diagnosed
		self.wasTested = False
		self.isTested = False
	
	def __str__(self):
		return "----------------------------------\n" + \
				"--- SETM: Human to human model ---\n" + \
				"--- https://github/rvalla/SETM ---\n" + \
				"-------------- Human -------------\n" + \
				"Human number: " + str(self.humanNumber) + "\n" + \
				"Family number: " + str(self.familyNumber) + "\n" + \
				"Age: " + str(self.age) +  ", Sex: " + str(self.sex) + "\n" + \
				"Infected: " + str(self.isInfected) + ", Was tested?: " + str(self.wasTested) + "\n" + \
				"Had symptoms: " + str(self.isSymptomatic) + ", Need treatment?: " + str(self.willNeedTreatment) + "\n" + \
				"Infection data: " +  str(self.incubationPeriod) + ", " + str(self.illnessPeriod) + ", " + \
				str(self.evolutionState) + "\n" + \
				"Behavior and risk: " + str(round(self.carefulFactor, 2)) + ", " + \
				str(round(self.socialDistanceFactor, 2)) + ", " + str(round(self.deathRiskFactor, 2))