#!/usr/bin/python2.7
#coding:utf-8

#Author : Aurélien REY
#Date : 16th november, 2016

import turtle

allVars = "abcdefghijklmnopqrstuvwxyz"
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
	print "L'équation contient {} variables différentes,".format(vars1[0])
	v = 2 ** vars1[0]
	o = 2 ** v
	print "il y a donc {} états différents donnant {} opérateurs (sorties) possibles,".format(v, o)

def setupTurtle() :
	turtle.setup(width, height)
	turtle.title("Bool ! Made for CERI Agroparc")
	turtle.hideturtle()
	turtle.up()
	turtle.goto(-width / 2 + 5, height / 2 - 5)

def drawSquare(x, y, c, char) :
	turtle.up()
	turtle.goto(x, y)
	turtle.down()
	for i in range(4) :
		turtle.fd(c)
		turtle.right(90)
	turtle.up()
	turtle.goto(x + c / 2 - 5, y - c / 2 - 10)
	turtle.down()
	turtle.write(char, font = ("Arial", 15, "bold"))
	turtle.up()

def operate(op, vars1) :
	if len(vars1) == 1 and op == "!" :
		return not int(vars1[0])
	elif len(vars1) == 1 and op != "!" :
		print "Désolé, le seul opérateur qui n'accepte qu'une variable est l'opérateur 'non' ('!')"

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
				lastValue = lastValue and int(vars1[i])

		if op == '+' :
			lastValue = int(vars1[0]) or int(vars1[1])

			for i in range(2, len(vars1)) :
				lastValue = lastValue or int(vars1[i])
 
	return "Inopérable !"

def calculate(string, *vars1) :
	vars2 = getVars(string)[1]

	for i in range(len(vars2)) :
		string = string.replace(vars2[i], str(vars1[i]))

	toOperateOr = string.split('+')

	for i in range(len(toOperateOr)) :
		if len(toOperateOr[i].split('.')) > 1 :
			toOperateOr[i] = operate('.', toOperateOr[i].split('.'))

	return operate('+', toOperateOr)

def convert(boolean) :
	if boolean :
		return 1
	else :
		return 0

f = raw_input("Entrez une équation : ")
print "\n-------------------\n"
f = f.replace(" ", "")
printInformations(f)
print "\n-------------------\n"

for i in range(2) :
	for j in range(2) :
		for k in range(2) :
			print "Pour [{}, {}, {}] : {}".format(i, j, k, calculate(f, i, j, k))
			print "----------"