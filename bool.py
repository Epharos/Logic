#!/usr/bin/python2.7
#coding:utf-8

#Author : Aurélien REY
#Date : November 16th 17th and 18th, 2016
#Utility : L'utilisateur rentre une équation booléenne et le programme retourne un tableau de vérité correspondant à l'équation

import os

allVars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
width, height = 500, 500

def containsOperator(string, operator) :
		return len(string.split(operator)) > 1

def getVars(string) :
	vars1 = list()
	count = 0

	for c in string :
		if not listContains(vars1, c) and isVarAllowed(c) :
			vars1.append(c)
			count += 1

	final = list()
	final.append(count)
	final.append(vars1)
	return final

def listContains(list1, var) :
	for i in list1 :
		if i == var :
			return True

	return False

def isVarAllowed(char) :
	for c in allVars :
		if c == char :
			return True

	return False

def printInformations(string) :
	vars1 = getVars(string)
	if vars1[0] > 1 :
		print "L'équation contient {} variables différentes,".format(vars1[0])
	else :
		print "L'équation contient {} variable,".format(vars1[0])
	v = 2 ** vars1[0]
	o = 2 ** v

	if v > 1 :
		print "il y a donc {} lignes au tableau".format(v)
	else :
		print "il y a donc {} ligne au tableau".format(v)

def regex(string) :
	r = 0
	results = list()

	firstIndex = -1

	for i in range(len(string)) :
		if string[i] == "(" and r == 0 :
			firstIndex = i
			r += 1
		elif string[i] == "(" :
			r += 1

		if string[i] == ")" :
			r -= 1

			if r == 0 :
				results.append(string[firstIndex + 1 : i])

			if r < 0 : 
				print "Erreur de parenthèse !"

	if r > 0 :
		print "Erreur de parenthèse"

	return results


def operate(op, vars1) :
	if len(vars1) == 1 and op == "~" :
		return not int(vars1[0])
	elif len(vars1) == 1 and op != "~" :
		print "Désolé, le seul opérateur qui n'accepte qu'une variable est l'opérateur 'not' ('~')"

	if len(vars1) == 2 :
		if op == '.' :
			return int(vars1[0]) and int(vars1[1])
		if op == '+' :
			return int(vars1[0]) or int(vars1[1])

	if len(vars1) > 2 :
		lastValue = 0

		if op == '.' :
			lastValue = int(vars1[0]) and int(vars1[1])

			for i in range(2, len(vars1)) :
				lastValue = convert(lastValue) and int(vars1[i])

		if op == '+' :
			lastValue = int(vars1[0]) or int(vars1[1])

			for i in range(2, len(vars1)) :
				lastValue = convert(lastValue) or int(vars1[i])

		return lastValue
 
	return "Inopérable !"

def calculate(string, vars1 = None) :
	vars2 = getVars(string)[1]

	if vars1 is not None :
		for i in range(len(vars2)) :
			string = string.replace(vars2[i], str(vars1[i]))

	prior = regex(string)

	prior2 = list(prior)

	for i, v in enumerate(prior2) :
		prior2[i] = calculate(v)

	for i in range(len(prior)) :
		string = string.replace(str(prior[i]), str(prior2[i]))

	string = string.replace("(", "")
	string = string.replace(")", "")

	string = string.replace("~0", "1")
	string = string.replace("~1", "0")

	toOperateOr = string.split('+')

	for i in range(len(toOperateOr)) :
		if len(toOperateOr[i].split('.')) > 1 :
			toOperateOr[i] = operate('.', toOperateOr[i].split('.'))

	if(len(toOperateOr) > 1) :
		return operate('+', toOperateOr)

	return toOperateOr[0]

def convert(boolean) :
	if boolean :
		return 1
	else :
		return 0

def decToBin(i) :
    return bin(i)[2:]

def layout(string) :
	string = string.replace("or", "+")
	string = string.replace("and", ".")
	string = string.replace("nand", ",")
	string = string.replace("xor", "*")
	string = string.replace("nor", "-")
	string = string.replace("nxor", "^")
	string = string.replace("xnor", "^")
	string = string.replace("imp", ">")
	string = string.replace("!", "~")
	string = string.replace("not", "~")

	return string

def stringContains(string) :
	nand = "," in string
	xor = "*" in string
	nor = "-" in string
	nxor = "^" in string
	imp = ">" in string

	return nand or xor or nor or nxor or imp

def formatOperation(string) :
	while stringContains(string) :
		for i in range(len(string) + 1) :
			if string[i] == ">" : #IMPLICATION
				before = str(string[i - 1])
				after = str(string[i + 1])

				if before == ")" :
					r = 0
					for a in range(i - 2, -1, -1) :
						if string[a] == "(" and r == 0 :
							before = string[a : i]
						elif string[a] == ")" :
							r += 1
						elif string[a] == "(" and r > 0 :
							r -= 1

				if after == "(" :
					r = 0
					for a in range(i + 2, len(string)) :
						if string[a] == ")" and r == 0 :
							after = string[i + 1 : a + 1]
						elif string[a] == "(" :
							r += 1
						elif string[a] == ")" and r > 0 :
							r -= 1


				tor = before + ">" + after

				tor2 = "(~" + before + "+" + after + ")"

				string = string.replace(tor, tor2)

				break

			if string[i] == "-" : #NOR
				before = str(string[i - 1])
				after = str(string[i + 1])

				if before == ")" :
					r = 0
					for a in range(i - 2, -1, -1) :
						if string[a] == "(" and r == 0 :
							before = string[a : i]
						elif string[a] == ")" :
							r += 1
						elif string[a] == "(" and r > 0 :
							r -= 1

				if after == "(" :
					r = 0
					for a in range(i + 2, len(string)) :
						if string[a] == ")" and r == 0 :
							after = string[i + 1 : a + 1]
						elif string[a] == "(" :
							r += 1
						elif string[a] == ")" and r > 0 :
							r -= 1

				tor = before + "-" + after

				tor2 = "(~(" + before + "+" + after + "))"

				string = string.replace(tor, tor2)

				break

			if string[i] == "," : #NAND
				before = str(string[i - 1])
				after = str(string[i + 1])

				if before == ")" :
					r = 0
					for a in range(i - 2, -1, -1) :
						if string[a] == "(" and r == 0 :
							before = string[a : i]
						elif string[a] == ")" :
							r += 1
						elif string[a] == "(" and r > 0 :
							r -= 1

				if after == "(" :
					r = 0
					for a in range(i + 2, len(string)) :
						if string[a] == ")" and r == 0 :
							after = string[i + 1 : a + 1]
						elif string[a] == "(" :
							r += 1
						elif string[a] == ")" and r > 0 :
							r -= 1

				tor = before + "," + after

				tor2 = "(~(" + before + "." + after + "))"

				string = string.replace(tor, tor2)

				break

			if string[i] == "^" : #NXOR / XNOR
				before = str(string[i - 1])
				after = str(string[i + 1])

				if before == ")" :
					r = 0
					for a in range(i - 2, -1, -1) :
						if string[a] == "(" and r == 0 :
							before = string[a : i]
						elif string[a] == ")" :
							r += 1
						elif string[a] == "(" and r > 0 :
							r -= 1

				if after == "(" :
					r = 0
					for a in range(i + 2, len(string)) :
						if string[a] == ")" and r == 0 :
							after = string[i + 1 : a + 1]
						elif string[a] == "(" :
							r += 1
						elif string[a] == ")" and r > 0 :
							r -= 1

				tor = before + "^" + after

				tor2 = "(~(~" + before + "." + after + "+" + before + ".~" + after + "))"

				string = string.replace(tor, tor2)

				break

			if string[i] == "*" : #XOR
				before = str(string[i - 1])
				after = str(string[i + 1])

				if before == ")" :
					r = 0
					for a in range(i - 2, -1, -1) :
						if string[a] == "(" and r == 0 :
							before = string[a : i]
						elif string[a] == ")" :
							r += 1
						elif string[a] == "(" and r > 0 :
							r -= 1

				if after == "(" :
					r = 0
					for a in range(i + 2, len(string)) :
						if string[a] == ")" and r == 0 :
							after = string[i + 1 : a + 1]
						elif string[a] == "(" :
							r += 1
						elif string[a] == ")" and r > 0 :
							r -= 1

				tor = before + "*" + after

				tor2 = "(~" + before + "." + after + "+" + before + ".~" + after + ")"

				string = string.replace(tor, tor2)

				break

	return string

def clear() :
	os.system("clear")

clear()

print "ÉQUATIONS LOGIQUES"

print "\n-------------------\n"

print "Vous pouvez utiliser les variables suivantes : \"{}\"".format(allVars)
print "Attention les variables sont sensibles à la casse (A est différent de a) !"
print "Vous pouvez évidemment utiliser les constantes 0 et 1 dans votre équation"
print "Les espaces ne sont pas pris en compte par le programme ('aandb' = 'a and b')"

try :
	raw_input("\nAppuyez sur Entrée")
except SyntaxError:
    pass

print "\n-------------------\n"

print "Les opérateurs logiques utilisables sont les suivants : "
print "(Note : Certains caractères officiels ne sont pas faisables au clavier,"
print "du coup le programme utilise un peu sa propre notation)"
print "Porte ET --> \t\t'and'\t'.'"
print "Porte OU --> \t\t'or'\t'+'"
print "Porte NON --> \t\t'not'\t'~'\t'!'"
print "Porte NAND --> \t\t'nand'\t','"
print "Porte NOR --> \t\t'nor'\t'-'"
print "Porte XOR --> \t\t'xor'\t'*'"
print "Porte NXOR/XNOR --> \t'nxor'\t'xnor'\t'^'"
print "Porte IMPLIQUE --> \t'imp'\t'>'"

try :
	raw_input("\nAppuyez sur Entrée")
except SyntaxError:
    pass

print "\n-------------------\n"

print "Exemples : "
print "a + b . c"
print "(a + b) . c"
print "1 and (a or b)"
print "~(~(a or b).!c)"
print "a-b > b"

try :
	raw_input("\nAppuyez sur Entrée")
except SyntaxError:
    pass

print "\n-------------------\n"

print "Le programme gère la priorité et les parenthèses !"

print "\n-------------------\n"

f = ""

while len(f) < 1 :
	f = raw_input("Entrez une équation (E) : ")

print "\n-------------------\n"

f = f.replace(" ", "")
f = layout(f)
print "E = " + f
f = formatOperation(f)
# print "Équation après formatage : " + f

print "\n-------------------\n"

printInformations(f)
print "\n-------------------\n"

top = "\t\t"
table = {}

for i in range(getVars(f)[0]) :
	top += "------"
	table[i, 0] = getVars(f)[1][i]

table[getVars(f)[0], 0] = "E"

top += "--------"

for i in range(2 ** getVars(f)[0]) :
	values = list()
	binary = decToBin(i)
	finalBinary = ""

	if len(binary) < getVars(f)[0] :
		for a in range(getVars(f)[0] - len(binary)) :
			finalBinary += "0"

	finalBinary += binary

	for c in range(len(finalBinary)) :
		values.append(finalBinary[c])
		table[c, i + 1] = finalBinary[c]

	if getVars(f)[0] == 0 :
		table[0, 1] = f
		continue

	table[len(finalBinary), i + 1] = calculate(f, values)

	# print "Pour {} : {}".format(values, calculate(f, values))
	# print "----------"

print "\t\tTABLE DE VÉRITÉ : \n"

print top

for i in range(2 ** getVars(f)[0] + 1) :
	print "\t\t",
	for j in range(getVars(f)[0] + 1) :
		if j != getVars(f)[0] :
			print "| ", table[j, i], "",
		else :
			print "|| ", table[j, i], "",

	print "|\n" + top
	if i == 0 :
		print top

try :
	raw_input("\n\nAppuyez sur Entrée")
except SyntaxError:
    pass

print "\n-------------------\n"

print "Le programme est toujours à améliorer, évidemment"
print "Si vous avez des idées : "
print "aurelien.rey@alumni.univ-avignon.fr\n"
print "Le programme et son code sont sous licence Creative Common (BY NC SA)"
print "C'est à dire que pour l'utilisation/le partage de ce programme/script vous devez : "
print "\t- Créditer l'auteur (citer son nom)"
print "\t- Qu'aucune utilisation et qu'aucun partage ne peut faire le fruit d'un bénéfice (vente interdite)"
print "\t- Que vous devez partager ce programme/code dans les mêmes conditions que celles dans lesquelles vous l'avez trouvé"
print "Pour en savoir plus : https://creativecommons.org/licenses/by-nc-sa/3.0/fr/\n"

print "Au plaisir de vous revoir ! :)"