"""
Program: formatData.py
Author: Val Booth <vxb4825@rit.edu>
Purpose: Formats data returned from the SQL connection in filter.py
	so that it can be more easily turned into a plotly graph. plotly
	expects arrays of X/dependent variables and Y/independent variables
	with corresponding indices.
"""


#String constants for int school type and region.
#Covert to string for better readability
lookup = {
	"type" : {
		1 : "PUBLIC",
		2 : "PRIVATE",
		3 : "PROPRIETARY"
	},
	"region" : {
		1 : "NE",
		2 : "MW",
		3 : "S",
		4 : "W",
		5 : "PAC",
		6: "OTHER"
	}
}



# Formats query data for use in plotly, seperating cursorTuples into X and Y data
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


	

# Used for SQL queries using regions and school types, which are stored in the 
# db as ints but are easier understood as strings. This function converts db ints
# to readable strings before X and Ying them.
# version - which version of lookup we're doing. Is either "region" or "type"
# cursorTuples - the data returned by the SQL call
# Returns: an array of tuples where each index is of format: (year, xAxis, yAxis)
def lookupFormatReturn(version, cursorTuples):
	table = lookup[version]
	#This will contain copies of type or version as a string
	xAxis = []
	#This will contain copies of the dependent followed by independent data
	yAxis = [] 	

	allYears = []
	previousYear = None

	for row in cursorTuples:
		#Converting to a list so I can edit it. Either version is in db as an
		#int, so I'm converting it to string so it's more readable
		row = list(row)
		currYear = row[0]
		#If we've changed years, we need to add the previous year to allYears
		#and start a new year
		if previousYear and previousYear != currYear:
			allYears.append((previousYear, xAxis,yAxis))
			xAxis = []
			yAxis = []
		
		versionNum = row[1]
		versionStr = table[row[1]]
		xAxis.extend((versionStr, versionStr))
		yAxis.extend((row[2], row[3]))

		previousYear = currYear
			
	allYears.append((previousYear, xAxis,yAxis))
	return allYears

# Used for the allRegionsType() function, which groups further breaks down every 
# region by the number of applications per school type, hence two lookups. 
# allRegionsType only looks at one year.
# Returns: an array of tuples where each index is of format: (region, xAxis, yAxis)
def doubleLookupFormatReturn(cursorTuples):
	types = lookup["type"]
	regions = lookup["region"]
	#This will contain copies of type as a string
	xAxis = []
	#This will contain copies of the dependent followed by independent data
	yAxis = [] 	

	allRegions = []
	previousReg = None

	for row in cursorTuples:
		#Converting to a list so I can edit it. Either version is in db as an
		#int, so I'm converting it to string so it's more readable
		row = list(row)
		currReg = row[0]
		
		#If we've changed regions we need to add the previous year to allYears
		#and start a new year
		if previousReg and previousReg != currReg:
			regStr = regions[previousReg]
			allRegions.append((previousReg, xAxis,yAxis))
			xAxis = []
			yAxis = []
		
		typeNum = row[1]
		typeStr = types[row[1]]
		xAxis.extend((typeStr, typeStr))
		yAxis.extend((row[2], row[3]))

		previousReg = currReg
			
	allRegions.append((previousReg, xAxis,yAxis))
	return allRegions


