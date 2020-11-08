def fileParser(target):
	f = open(target, "r")
	doctorList = []
	colourList = []
	patientList = []

	for l in f:
		prelist = l.split(" ")
		prelist[-1] = prelist[-1].split('\n')[0]
		if prelist[0] == 'MD':
			doctorList.append( (prelist[1], prelist[2]) )
		elif prelist[0] == 'PL':
			colourList.append( (prelist[1], prelist[2], prelist[3]) )
		elif prelist[0] == 'P':
			patientList.append( (prelist[1], prelist[2], prelist[3]) )
	
	return [doctorList, colourList, patientList]
