"""
Program: filter.py
Author: Val Booth <vxb4825@rit.edu>
Purpose: Explores the FAFSA data stored in sqlite db HoneyBadgers.db.
This file connects to the db and returns the appropriate data.

HoneyBadgers.db has two tables of the form:

School:
OPE_ID int pkey
Name varchar(40)
State char(2)
Zip char(10)
Type int
Region int

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

And Region is of the form: 
1 : Northeast
2 : Midwest
3 : South
4 : West
5 : Pacific
6 : Other (Out of US)
Regions are determined by the Census Bureau here: 
	https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf

Y_Dependent and Y_Independent will be the total for the entire year if selected in Q6.
Award_YTD_Total is always the sum of Y_Dependent + Y_Independent for each quarter.

NOTE: For Testing, RIT's OPE_ID = 280600
"""
import sqlite3
from formatData import *


'''------------------CONSTANTS-----------------'''


#DB connection
conn = sqlite3.connect('HoneyBadgers.db')
cursor = conn.cursor()


#Sql components that are common across queries
SQL_SUM_STUDENTS = "SUM(f.Y_Dependent) AS allDependents, SUM(f.Y_Independent) as allIndependents"
SQL_SUM_STUDENTS_PER_QUARTER = "SUM(f.Q_Dependent) AS allDependents, SUM(f.Q_Independent) as allIndependents"
SQL_JOIN_TABLES = " FROM FAFSA_Data AS f INNER JOIN School s ON f.OPE_ID=s.OPE_ID"
SQL_Q6 = " Qtr='Q6'"


'''------------------STATE QUERIES-------------'''
#Get the names of all states in the database
#Returns: A list of two character strings of the states
def allStateNames():
	sqlStr = "SELECT DISTINCT State FROM School ORDER BY State"
	cursor.execute(sqlStr)

	res = list(cursor)
	ret = []
	for state in res:
		ret.append(state[0])

	return ret


# Returns a sum of dependents and independents, for each year, in the given state
def stateOnly(state):
	#Note: input to query is of form (state,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		" WHERE " + SQL_Q6 + " AND s.State = ? GROUP BY Year ORDER BY Year"
	cursor.execute(sqlStr, (state,))
	
	return formatForReturn(list(cursor))


#Returns the sum of independents and dependents, for each school type, in
#each year, for the given state.
def typesInState(state):
	sqlStr = "SELECT f.Year, s.Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES +\
		" WHERE " + SQL_Q6 + "AND s.State = ? GROUP BY State, Year, Type"
	cursor.execute(sqlStr, (state,))

	return lookupFormatReturn("type",list(cursor))



#Returns the total independent, and dependent students, per state, in the
#given year
def allStatesYear(year):
	#Note: input to query is of form (year,) because that converts it to a
	#tuple, which the execute function expects even w/1 arg.
	sqlStr = "SELECT s.State, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		" WHERE " + SQL_Q6 + " AND f.Year = ? GROUP BY State, Year"
	cursor.execute(sqlStr, (year,))

	return formatForReturn(list(cursor))


	


'''-----------------REGION QUERIES-------------'''
# Returns independents and dependents, for each year, for one region
# region - string representing the region name, should match lookup table
def region(reg):
	regionTable = lookup["region"]
	#Looks up the key integer for the region string value
	regionNum = regStrToNum(reg)
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		" WHERE " + SQL_Q6 + " AND s.Region = ? GROUP BY Year ORDER BY Year"
	cursor.execute(sqlStr, (regionNum,))
	
	return formatForReturn(list(cursor))


# Returns all of the dependents and independents, for each year, grouped by 
# geographical region
# Returns: an array of tuples where each index is of format: (year, xAxis, yAxis)
def allRegions():
	#NOTE: Add "AND Region <> 6" if you only want US
	#likewise "<> 5" for only continuous US
	sqlStr = "SELECT f.Year as YEAR, s.Region AS Region, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES +\
		" WHERE " + SQL_Q6  + " GROUP BY Year, Region ORDER BY Year, Region"
	cursor.execute(sqlStr)
	

	return lookupFormatReturn("region",list(cursor))


# Returns all of the dependent and independents, for each year, grouped by school
# type, in a particular region
# region - string representing the region name, should match lookup table
# Returns: an array of tuples where each index is of format: (region, xAxis, yAxis)
def typesInRegion(region):
	regionTable = lookup["region"]
	#Looks up the key integer for the region string value
	regionNum = regStrToNum(region)
	sqlStr = "SELECT f.Year AS YEAR, s.Type AS Type, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		" WHERE " + SQL_Q6 + " AND s.Region = ? GROUP BY Year, Type ORDER BY Year, Type"
	cursor.execute(sqlStr, (regionNum,))

	return lookupFormatReturn("type",list(cursor))


# Displays the number of dependents and independents, grouped by school type, for
# each region in a particular year. 
# year - the desired year to break down by
def allRegionsType(year):
	#NOTE: Add "AND Region <> 6" if you only want US
	#likewise "<> 5" for only continuous US
	sqlStr = "SELECT s.Region AS Region, s.Type AS Type, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES +\
		" WHERE " + SQL_Q6  + " AND f.Year = ? "+ " GROUP BY Year, Region, Type ORDER BY Year, Region, Type"
	print(sqlStr)
	cursor.execute(sqlStr,(year,))

	return doubleLookupFormatReturn(list(cursor))



'''-----------------OTHER QUERIES--------------'''

def allYears():
	sqlStr = "SELECT DISTINCT year FROM FAFSA_Data ORDER BY year"
	cursor.execute(sqlStr)

	res = list(cursor)
	ret = []
	for year in res:
		ret.append(str(year[0]))
	return ret



#Returns the sum of all dependents and independents respectively, EVERYWHERE for 
#each year
def total():
	sqlStr = "SELECT f.Year, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES +\
		" WHERE " + SQL_Q6 + " GROUP BY Year ORDER BY Year"
	#print(sqlStr)
	cursor.execute(sqlStr)

	return formatForReturn(list(cursor))



#Compare dependent/independent data across the same qtr in each year, 
#for all of the years that that Qtr exists. 2015 only has Q1-Q3
def qtrYears(Qtr):
	qtrStr = "Q" + Qtr
	sqlStr = "SELECT f.Year AS YEAR, " + SQL_SUM_STUDENTS + " " + SQL_JOIN_TABLES + \
		" WHERE Qtr= ? GROUP BY Year, Qtr ORDER BY Year"
	cursor.execute(sqlStr, (qtrStr,))
	
	return formatForReturn(list(cursor))



#Returns the number of independent and dependent students for every school type,
#Private, public, proprietary, in the given year.
def typePerYear():
	sqlStr = "SELECT f.Year, s.Type AS Type, " + SQL_SUM_STUDENTS + SQL_JOIN_TABLES + \
		" WHERE " + SQL_Q6 + " GROUP BY Type, Year ORDER BY Year"
	cursor.execute(sqlStr)

	return lookupFormatReturn("type",list(cursor))


def regStrToNum(rStr):
	table = lookup["region"]
	return list(table.keys())[list(table.values()).index(rStr)]



