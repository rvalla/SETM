class Human():
	"Human being modelling for epidemic simulations"
	
	def __init__(self, humanNumber):
	
		self.humanNumber = humanNumber
		
		#Defining some human characteristics
		self.age = 0
		self.sex = '?'
		
		#Possible infection targets
		self.familyNumber = 0
		self.family = []
		self.contacts = []
		
		#Risk evaluation...
		self.carefulFactor = 1.0
		self.socialDistanceFactor = 1.0
		self.deathRiskFactor = 1.0
	
		#Variables to managing the disease
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
		
		#Boolean to define if human was diagnosed
		self.wasTested = False