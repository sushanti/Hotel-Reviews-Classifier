import sys
import json
import math
from collections import defaultdict
from collections import OrderedDict

features={}
class1Prior={}
class2Prior={}

#load model features
with open('nbmodel.txt','r',encoding='utf8') as file:
	data = json.loads(file.read())
	features = data ["features"]
	class1Prior = data["class1prior"]
	class2Prior = data["class2prior"]
	stopwords = data["stopwords"]
	output =  OrderedDict()
	
#read file
with open(sys.argv[1],'r',encoding='utf8') as file:
	fileToWrite = open("nboutput.txt", "w",encoding='utf-8')
	for line in file:
		words = line.split()
		output[words[0]]={}
		
		#compute probability for each class
		for key in features:
			probability = 1
			for i in range(1,len(words)):
				word = ''.join(ch for ch in words[i] if ch.isalnum())
				word = word.lower()
				if word in features [key] and word not in stopwords:
					probability += math.log(features [key] [word])
					#fileToWrite.write("key: "+words[0]+" "+words[i]+" "+str(features[key][words[i]])+"\n");
			if key in class1Prior:
				output[words[0]] [key] = probability + math.log(class1Prior [key])
			elif key in class2Prior:
				output[words[0]] [key] = probability + math.log(class2Prior [key])
	
	#choose class with more probability
	for key in output:
		class1Values=defaultdict(dict)
		class2Values=defaultdict(dict)
		
		for prior in class1Prior:
			class1Values [prior] = output[key][prior]
		
		class1 = max(class1Values, key=class1Values.get)
		
		
		for prior in class2Prior:
			class2Values [prior] = output[key][prior]
			
		class2 = max(class2Values, key=class2Values.get)
		

		fileToWrite.write(key+" "+class1+" "+class2+"\n")
			
	fileToWrite.close()
				
				
			
		   

