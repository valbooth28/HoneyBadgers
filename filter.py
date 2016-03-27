"""
Program: filter.py
Author: Val Booth <vxb4825@rit.edu>
Purpose: Explores the FAFSA data stored in sqlite db HoneyBadgers.db.
This filter data should be able to be ported into plotly for graphs.

HoneyBadgers.db has two tables of the form:

School:
OPE_ID int pkey
Name varchar(40)
State char(2)
Zip char(10)
Type int

FAFSA_DATA
OPE_ID int pkey
Year int pkey
Qtr varchar(2) pkey
Q_Dependent int
Q_Independent int
Q_Total int
Y_Dependent int
Y_Independent int
Award_YTD_Total int

Where Type is of form:
1 : Public
2 : Private
3 : Proprietary

Y_Dependent and Y_Independent will be the total for the entire year if selected in Q6.
Award_YTD_Total is always the sum of Y_Dependent + Y_Independent for each quarter.
"""
import sqlite3

#Type constants
PUBLIC = 1
PRIVATE = 2
PROPRIETARY = 3

#DB connection
conn = sqlite3.connect('HoneyBadgers.db')
cursor = conn.cursor()

#Prints menu of available options for this program
def help():
	print("Your filtering options are:")
	
	print("'State X' will show you a breakdown of the sum of independents and ")
	print("dependents for state with the acronym X for each year.")
	print("")
	
	print("'All States Year Y' will show you breakdown of the sum of independents")
	print(" and dependents, per state, in Year Y.")
	print("")

	print("'Type Year Y' will show you the breakdown of independents and dependents")
	print("across each school type in year y.")
	print("")

	#TODO more filtering

	print("'Exit' will exit the program.")
	print("'Help' will repeat this menu.")



# Shows a sum of independents and dependents, for each year, in the given state
def stateOnly(state):
	#try:
	
	#Note: input to query is of form (state,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT f.Year AS YEAR, SUM(f.Y_Dependent) AS allDependents, SUM(f.Y_Independent) as allIndependents " + \
		"FROM FAFSA_Data AS f INNER JOIN School S ON f.OPE_ID=S.OPE_ID AND Qtr='Q6' AND S.State = ? GROUP BY Year ORDER BY Year"
	cursor.execute(sqlStr, (state,))
	
	cursorList = list(cursor)
	for row in cursorList:
		#TODO Better formatting.
		print(row)

		
def main():
	print("Welcome to filter.py!")
	help()

	while True:
		option = input("Enter what you'd like to filter by: ")
		if "State" in option:
			state = option[6:]
			stateOnly(state)

		#TODO other commands

		elif option == "Help":
			help()

		elif option == "Exit":
			print("Goodbye!")
			#Note: Cleanly exits without having to import sys
			raise SystemExit

		else:
			print("Please enter a valid command, or type 'Help' to view the menu again.")

main()