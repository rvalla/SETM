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