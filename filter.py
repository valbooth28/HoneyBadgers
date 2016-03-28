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
typeLookup = {
	1 : "PUBLIC",
	2 : "PRIVATE",
	3 : "PROPRIETARY"
}


#DB connection
conn = sqlite3.connect('HoneyBadgers.db')
cursor = conn.cursor()


#Sql components that are common across queries
SQL_SUM_STUDENTS = "SUM(f.Y_Dependent) AS allDependents, SUM(f.Y_Independent) as allIndependents"
SQL_JOIN_TABLES = " FROM FAFSA_Data AS f INNER JOIN School s ON f.OPE_ID=s.OPE_ID"
SQL_Q6 = " AND Qtr='Q6'"



#Prints menu of available options for this program
def help():
	print("Your filtering options are:")
	
	print("'State X' will show you a breakdown of the sum of independents and ")
	print("dependents for state with the acronym X for each year.")
	print("")

	print("'Types State X' will show you a breakdown of the sum of independents and ")
	print("dependents for each school type in the state with the acronym X for each year.")
	print("")
	
	print("'All States Y' will show you breakdown of the sum of independents")
	print(" and dependents, per state, in Year Y.")
	print("")

	print("'Type Years' will show you the breakdown of independents and dependents")
	print("across each school type for each year.")
	print("")

	#TODO more filtering

	print("'Exit' will exit the program.")
	print("'Help' will repeat this menu.")



# Shows a sum of independents and dependents, for each year, in the given state
def stateOnly(state):
	#Note: input to query is of form (state,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		+ SQL_Q6 + " AND s.State = ? GROUP BY Year ORDER BY Year"
	cursor.execute(sqlStr, (state,))
	
	cursorTuples = list(cursor)
	for row in cursorTuples:
		#TODO Better formatting.
		print(row)



#Shows the number of independent and dependent students for every school type,
#Private, public, proprietary, in the given year.
def typePerYear():
	sqlStr = "SELECT f.Year, s.Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		SQL_Q6 + " GROUP BY Type, Year ORDER BY Year"
	cursor.execute(sqlStr)
	
	cursorTuples = list(cursor)
	for row in cursorTuples:
		#Converting to a list so I can edit it. Types are stored as ints in the db,
		#Making the output more readable.
		row = list(row)
		row[1] = typeLookup[row[1]]
		print(row)



#Prints out the total independent, and dependent students, per state, in the
#given year
def allStatesYear(year):
	#Note: input to query is of form (year,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT s.State, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		SQL_Q6 + " AND f.Year = ? GROUP BY State, Year"
	cursor.execute(sqlStr, (year,))

	cursorTuples = list(cursor)
	for row in cursorTuples:
		print(row)



#Prints out the sum of independents and dependents, for each school type, in
#each year, for the given state.
def typesInState(state):
	sqlStr = "SELECT f.Year, s.Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES +\
		SQL_Q6 + "AND s.State = ? GROUP BY State, Year, Type"
	cursor.execute(sqlStr, (state,))

	cursorTuples = list(cursor)
	for row in cursorTuples:
		#Converting to a list so I can edit it. Types are stored as ints in the db,
		#Making the output more readable.
		row = list(row)
		row[1] = typeLookup[row[1]]
		print(row)



def main():
	print("Welcome to filter.py!")
	help()

	while True:
		option = input("Enter what you'd like to filter by: ")
		if "All State" in option:
			year = option[-4:]
			allStatesYear(year)

		elif "Types State" in option:
			state = option[-2:]
			typesInState(state)
			
		elif "State" in option:
			state = option[-2:]
			stateOnly(state)

		elif "Type" in option:
			typePerYear()

		elif option == "Help":
			help()

		elif option == "Exit":
			print("Goodbye!")
			#Note: Cleanly exits without having to import sys
			raise SystemExit

		else:
			print("Please enter a valid command, or type 'Help' to view the menu again.")

main()