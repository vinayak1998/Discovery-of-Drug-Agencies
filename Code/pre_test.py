import sys
import time

start = time.time()

filename = sys.argv[1]

f = open(filename+'.graph', 'r')

lines = f.readlines()
f.close()

a = lines[0].strip().split(' ')

num_vertices = int(a[0])
num_edges = int(a[1])
num_components = int(a[2])

dic_edges = {}
dic_vars = {}

for i in range(1,num_edges+1):
	temp = lines[i]
	t = temp.strip().split(' ')
	string = 'E'+'-'+t[0]+'-'+t[1]
	dic_edges[string] = 1
	string = 'E'+'-'+t[1]+'-'+t[0]
	dic_edges[string] = 1

g = open("vars", 'w')
g.write(str(num_vertices*num_components) + "\n")

count_var = 1

for i in range(1,num_components+1):
	for j in range(1,num_vertices+1):
		temp_str = " X-"+str(j)+"-"+str(i)+ "\n" 
		g.write(str(count_var) + temp_str)
		dic_vars[temp_str.strip()] = str(count_var)
		count_var += 1

for i in range(1,num_components+1):
	for j in dic_edges:
		temp_str = " " +str(j)+'-'+str(i)+ "\n"
		g.write(str(count_var) + temp_str)
		dic_vars[temp_str.strip()] = str(count_var)
		count_var += 1

temp_clause = []

"""
for k in range(1, num_components+1):
	for i in range(1, num_vertices+1):
		for j in range(1, num_vertices+1):
			if (i!=j):
				temp_str = "E-"+str(i)+"-"+str(j)
				if temp_str not in dic_edges:
					t_clause = temp_str+"-"+str(k)
					temp_clause.append("-" + t_clause + "\n")
					g.write(str(count_var) + " " + t_clause + "\n")
					dic_vars[t_clause.strip()] = str(count_var)
					count_var += 1
				
"""

def get_satinput(clause):
	temp = clause.strip().split(' ')
	temp_list = []
	for i in temp:
		if i[0] != '-':
			temp_list.append(dic_vars[i])
		else:
			temp_list.append('-' + dic_vars[i[1:]])		
	temp_list.append(str(0))
	temp_str = ' '.join(temp_list) + '\n'
	return temp_str

f = open(filename+'.satinput', 'w')

clauses_array = []

clauses_array.append('p cnf \n')
count_clause= 0

#at least one node in a component
for i in range(1,num_components+1):
	clause = ""
	for j in range(1,num_vertices+1):
		clause += "X-" + str(j) + "-" + str(i) + " "
	clauses_array.append(clause.strip() + '\n')
	count_clause+= 1
	
clauses_array.append("NOW")
	
"""
#at least one edge in a component
for i in range(1,num_components+1):
	clause = ""
	for j in dic_edges:
		clause += j + "-" + str(i) + " "
	clauses_array.append(clause.strip() + '\n')
	count_clause+= 1
	
clauses_array.append("NOW")
"""

#each node in at least one component
for i in range(1, num_vertices+1):
	clause = ""
	for j in range(1,num_components+1):
		clause += "X-" + str(i) + "-" + str(j) + " "
	clauses_array.append(clause.strip() + '\n')
	count_clause+= 1
	
clauses_array.append("NOW")

"""
#each edge in at least one component
for i in dic_edges:
	clause = ""
	for j in range(1,num_components+1):
		clause += i + "-" + str(j) + " "
	clauses_array.append(clause.strip() + '\n')
	count_clause+= 1
	
clauses_array.append("NOW")
	
#if edge i-j in k then edge j-i also in k
for k in range(1, num_components):
	for edge in dic_edges:
		tell = edge.split("-")
		clause = edge +"-" +str(k) + " -E-"+str(tell[2])+"-"+str(tell[1])+"-"+str(k)
		clauses_array.append(clause.strip() + '\n')
		count_clause+= 1
	
clauses_array.append("NOW")
"""

#at least one edge in a component


for i in range(1, num_vertices+1):
	for j in range(1, num_vertices +1):
		if i!=j:
			temp = "E-"+str(i)+"-"+str(j)
			if temp in dic_edges:
				t1 = "Y-"+str(i)+"-"+str(j)
				clause = ""
				for k in range(1,num_components+1):
					temp_str = t1+"-"+str(k)+"\n"
					g.write(str(count_var) + " " + temp_str)
					dic_vars[temp_str.strip()] = str(count_var)
					count_var += 1
		
					clause1 = "-X-" + str(i)+"-"+str(k) + " -X-" + str(j) +"-" + str(k) + " Y-"+str(i)+'-'+str(j)+'-'+str(k) + '\n'
					clauses_array.append(clause1)
					count_clause+= 1
					clause1 = "-Y-" + str(i)+'-'+str(j)+'-'+str(k) + " X-" + str(i) + "-" + str(k)
					clauses_array.append(clause1)
					count_clause+= 1
					clause1 = "-Y-" + str(i)+'-'+str(j)+'-'+str(k) + " X-" + str(j) + "-" + str(k)
					clauses_array.append(clause1)
					count_clause+= 1
			
					clause += " " + temp_str.strip()
				clauses_array.append(clause)
				count_clause +=1
		
					
			
					
		    


#subgraphs are complete
for k in range(1, num_components+1):
	for i in range(1, num_vertices + 1):
		for j in range(1, num_vertices + 1):
			if i!=j:
				temp = "E-"+str(i)+"-"+str(j)
				if temp not in dic_edges:
					clause = "-X-" + str(i) + '-' + str(k) + " -X-" + str(j) + '-' + str(k) + '\n'
					clauses_array.append(clause)
					count_clause += 1

clauses_array.append("NOW")


#not a subgraph

for k1 in range(1,num_components+1):
	for k2 in range(k1+1, num_components+1):
		clause = ""
		for i in range(1, num_vertices+1):
			temp_str = " X-" +str(i)+'-'+str(k1)+'-'+str(k2) + '\n'
			g.write(str(count_var) + temp_str)
			dic_vars[temp_str.strip()] = str(count_var)
			count_var += 1
			
			clause1 = "-X-" + str(i)+"-"+str(k1) + " -X-" + str(i) +"-" + str(k2) + " X-"+str(i)+'-'+str(k1)+'-'+str(k2) + '\n'
			clauses_array.append(clause1)
			count_clause+= 1
			clause1 = "-X-" + str(i)+'-'+str(k1)+'-'+str(k2) + " X-" + str(i) + "-" + str(k1)
			clauses_array.append(clause1)
			count_clause+= 1
			clause1 = "-X-" + str(i)+'-'+str(k1)+'-'+str(k2) + " X-" + str(i) + "-" + str(k2)
			clauses_array.append(clause1)
			count_clause+= 1
			
			clause += " " + temp_str.strip()
		clauses_array.append(clause)
		count_clause +=1
		

#print(clauses_array)
for i in clauses_array:
	try:
		if i == "NOW":
			continue
		elif i[0] != "p":
			f.write(get_satinput(i))
		else:
			temp = "p cnf " + str(count_var-1) + " " + str(count_clause) + "\n"
			f.write(temp)
	except KeyError:
		print i
		break
g.close()
f.close()
