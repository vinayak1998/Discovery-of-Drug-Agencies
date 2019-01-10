import sys
import time

filename = sys.argv[1]

f = open(filename + '.satoutput', 'r')
dic = {}

final = open(filename + '.subgraphs', 'w')

sat = (f.readline()).strip()
if sat == "SAT":
	val = (f.readline()).split(" ")
	
	g = open('vars', 'r')
	num = int(g.readline())
	
	temp = g.readlines()
	for i in range(num):
		if val[i][0] != "-":
			var_num = int(val[i])
			var_name = (temp[var_num-1].split(" "))[1]
			#print(var_name)
			temp_store = var_name.split("-")
			component = temp_store[2] 
			variable = temp_store[1]
			if component not in dic:	
				dic[component] = []
			(dic[component]).append(variable)
	
	for i in dic:
		variables = dic[i]
		if int(len(variables)) == 1:
			#print "esa"
			final.close()
			final = open(filename + '.subgraphs', 'w')
			final.write("0")
			break
		else:
			first = "#" + (str(i)).strip() + " " + str(len(variables))
			second = ' '.join(variables)
			final.write(first.strip() + "\n")
			final.write(second.strip() + "\n")		
	g.close()
	
else:
	final.write("0")

f.close()
final.close()
