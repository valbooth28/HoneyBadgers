"""
Program: filter.py
Author: Val Booth <vxb4825@rit.edu>
Purpose: Explores the FAFSA data stored in sqlite db HoneyBadgers.db.
This file returns data in a form that can be used by plotly.

HoneyBadgers.db has two tables of the form:

School:
OPE_ID int pkey
Name varchar(40)
State char(2)
Zip char(10)
Type int

FAFSA_Data
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

NOTE: For Testing, RIT's OPE_ID = 280600
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
SQL_SUM_STUDENTS_PER_QUARTER = "SUM(f.Q_Dependent) AS allDependents, SUM(f.Q_Independent) as allIndependents"
SQL_JOIN_TABLES = " FROM FAFSA_Data AS f INNER JOIN School s ON f.OPE_ID=s.OPE_ID"
SQL_Q6 = " AND Qtr='Q6'"



# Returns a sum of dependents and independents, for each year, in the given state
def stateOnly(state):
	#Note: input to query is of form (state,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		SQL_Q6 + " AND s.State = ? GROUP BY Year ORDER BY Year"
	cursor.execute(sqlStr, (state,))
	
	return formatForReturn(list(cursor))
	


#Compare dependent/independent data across the same qtr in each year, 
#for all of the years that that Qtr exists. 2015 only has Q1-Q3
def qtrYears(Qtr):
	qtrStr = "Q" + Qtr
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS_PER_QUARTER + " " + SQL_JOIN_TABLES + \
		" AND Qtr= ? GROUP BY Year, Qtr ORDER BY Year"
	cursor.execute(sqlStr, (qtrStr,))
	
	return formatForReturn(list(cursor))



#Returns the number of independent and dependent students for every school type,
#Private, public, proprietary, in the given year.
def typePerYear():

	sqlStr = "SELECT f.Year, s.Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		SQL_Q6 + " GROUP BY Type, Year ORDER BY Year"
	cursor.execute(sqlStr)

	return typeFormatForReturn(list(cursor))



#Returns the sum of all dependents and independents respectively, EVERYWHERE for 
#each year
def total():
	sqlStr = "SELECT f.Year, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES +\
		SQL_Q6 + " GROUP BY Year ORDER BY Year"
	#print(sqlStr)
	cursor.execute(sqlStr)

	return formatForReturn(list(cursor))



#Returns the total independent, and dependent students, per state, in the
#given year
def allStatesYear(year):
	#Note: input to query is of form (year,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT s.State, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		SQL_Q6 + " AND f.Year = ? GROUP BY State, Year"
	cursor.execute(sqlStr, (year,))

	return formatForReturn(list(cursor))



#Returns the sum of independents and dependents, for each school type, in
#each year, for the given state.
def typesInState(state):
	sqlStr = "SELECT f.Year, s.Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES +\
		SQL_Q6 + "AND s.State = ? GROUP BY State, Year, Type"
	cursor.execute(sqlStr, (state,))

	return typeFormatForReturn(list(cursor))
	


#Formats query data for use in plotly. Puts the independent variables in
#one array and the dependents in another. Each index of the resulting arrays
#(i.e., index 0 in each array) will correspond to the same data point.
# Returns:
#   xAxis - array of independent variables
#   yAxis - array of dependent variables matching by index w/xAxis
def formatForReturn(cursorTuples):
	#This will contain copies of the independent variable- possibly state, year, etc.
	xAxis = []
	#This will contain copies of the dependent followed by independent data
	yAxis = []
	for row in cursorTuples:
		#we need two copies of the independent var so both dependent and
		#independent can reference it.
		xAxis.extend((row[0], row[0]))
		yAxis.extend((row[1], row[2]))
	
	return xAxis, yAxis



#Converts type integers to their corresponding strings (1 = 'Public', etc)
#before putting it in proper x/y axis format in plotly.
# Returns: an array of tuples where each index is of format: (year, xAxis, yAxis)
def typeFormatForReturn(cursorTuples):
	#This will contain copies of type as a string ('Private', 'Public', etc.)
	xAxis = []
	#This will contain copies of the dependent followed by independent data
	yAxis = [] 	

	allYears = []
	
	for row in cursorTuples:
		#Converting to a list so I can edit it. Types are stored as ints in the db,
		#Making the output more readable.
		row = list(row)
		typeNum = row[1]
		typeStr = typeLookup[row[1]]
		xAxis.extend((typeStr, typeStr))
		yAxis.extend((row[2], row[3]))

		#Each year has a row for types 1, 2, 3. If the type is currently 3,
		#we're done w/this year and can add it to all years/reset x and y
		if typeNum == 3:
			allYears.append((row[0], xAxis,yAxis))
			xAxis = []
			yAxis = []


	return allYears

#Get the names of all states in the database
#Returns: A list of two character strings of the states
def allStateNames():
	sqlStr = "SELECT DISTINCT state FROM School ORDER BY state"
	cursor.execute(sqlStr)

	res = list(cursor)
	ret = []
	for state in res:
		ret.append(state[0])

	return ret


def allYears():
	sqlStr = "SELECT DISTINCT year FROM FAFSA_Data ORDER BY year"
	cursor.execute(sqlStr)

	res = list(cursor)
	ret = []
	for year in res:
                ret.append(str(year[0]))
	return ret
