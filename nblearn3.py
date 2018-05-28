import sys
import json
from collections import defaultdict

if  len(sys.argv) > 0:	
	try:
		class1Prior = defaultdict(dict)
		class2Prior = defaultdict(dict)
		features = defaultdict(dict)
		model = defaultdict(dict)
		frequencies = defaultdict(dict)
		
		with open(sys.argv[1], 'r',encoding='utf8') as file:
			totalLines = 0
			for line in file:
				words = line.split();
				
				class1 = words[1]
				class2 = words[2]				
				#computing true/fake priors
				if class1 in class1Prior:
					class1Prior [class1] += 1
				else:
					class1Prior [class1] = 1
				
				#computing pos/neg priors
				if words[2] in class2Prior:
					class2Prior [class2] +=1
				else:
					class2Prior [class2] = 1
				
				totalLines+=1
				
			
			#insert classes as keys in feature dictionary
			for key in class1Prior:
				features [key] = {}
				features [key] ["class_total_count"] = 0
			for key in class2Prior:
				features [key] = {}
				features [key] ["class_total_count"] = 0
			
			#computing feature counts for each class
			file.seek(0)
			for line in file:
				words = line.split()
				for i in range(3,len(words)):
					word = ''.join(ch for ch in words[i] if ch.isalnum())
					word = word.lower()
					if word in features [words[1]]:
						features [words[1]] [word]+=1
					else:
						for key in class1Prior:
							if key == words[1]:
								features [key] [word] = 1
							else:
								features [key] [word] = 0
								
					if word in features [words[2]]:
						features [words[2]] [word]+=1
					else:
						for key in class2Prior:
							if key == words[2]:
								features [key] [word] = 1
							else:
								features [key] [word] = 0
					
					#computing word frequencies
					if word in frequencies:
						frequencies [word]+=1
					else:
						frequencies [word] = 1
			
			#add-1 smoothing for each class in features					
			for featureKey in features:
				for key in features [featureKey]:
					if key != "class_total_count":
						features [featureKey] [key] +=1
						features [featureKey] ["class_total_count"] += features [featureKey] [key]							
				
			#computing prior probabilities for each class	
			for key in class1Prior:
				class1Prior[key] = class1Prior[key]/totalLines
			for key in class2Prior:
				class2Prior[key] = class2Prior[key]/totalLines
				
			#computing feature probabilities
			for featureKey in features:
				for key in features [featureKey]:
					if key!="class_total_count":
						features [featureKey] [key] = features [featureKey] [key] / features [featureKey] ["class_total_count"]
		
		#computing stop word list
		sortedfrequencies = sorted((value,key) for (key,value) in frequencies.items())
		sortedfrequencies = sortedfrequencies[-10:]
		stopwords=[]
		for item in sortedfrequencies:
			stopwords.append(item[1])

		
		#populating json model
		model ["features"] = {}
		model ["features"] = features
		
		model ["class1prior"] = {}
		model ["class1prior"] = class1Prior
		
		model ["class2prior"] ={}
		model ["class2prior"] = class2Prior
		
		model ["stopwords"] = stopwords
				
		json = json.dumps(model)
		fileToWrite = open("nbmodel.txt", "w")
		fileToWrite.write(json)
		fileToWrite.close()
	except OSError as e:
		print("File not found")
else:
	print("Enter file name and path")

