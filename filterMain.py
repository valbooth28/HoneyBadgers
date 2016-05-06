"""
Program: filterMain.py
Author: Val Booth <vxb4825@rit.edu>
Purpose: Has a main function that allows you to view/print filter.py's result
out to the terminal for easier exploring w/o SQL commands.
"""
from filter import *


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


	print("'Qtr Years Q' will show you the breakdown of independents and dependents")
	print("for Quarter #Q in each year where that data is available")
	print("")

	print("'Total' will show you the total sum of dependents and independents in")
	print("in each available for full year.")
	print("")
	
	#region()
	print("'Region R' will show you the breakdown of dependents and independents")
	print("for region 'R' in every year.")
	print("")
	
	#allRegions()
	print("'All Regions' will show you the breakdown of dependents and independents")
	print("in every region for every year.")
	print("")
	
	#typesInRegion()
	print("'Types Region R' shows the number of dependents and independents, who applied")
	print("to each school type, in region R, in every year.")
	print("")
	
	#allRegionsType()
	print("'Types All Regions Y' shows the number of dependents and independents, in every")
	print("region, who applied to different school types, in year Y")
	print("")

	print("'Exit' will exit the program.")
	print("'Help' will repeat this menu.")


def main():
	print("Welcome to filter.py!")
	help()

	while True:
		#So that way we don't try to print non existant data
		queryCommand = True
		
		option = input("Enter what you'd like to filter by: ")
		if "All State" in option:
			year = option[-4:]
			xAxis, yAxis = allStatesYear(year)


		elif "Types State" in option:
			state = option[-2:]
			allYears = typesInState(state)
			typePrint(allYears)

			#We had our custom printing above, no need to print again
			queryCommand = False
			
		elif "All Regions" == option:
			allReg = allRegions()
			typePrint(allReg)

			#We had our custom printing above, no need to print again
			queryCommand = False

		elif "Types Region" in option:
			reg = option[13:]
			typeRegions = typesInRegion(reg)
			typePrint(typeRegions)

			#We had our custom printing above, no need to print again
			queryCommand = False

		elif "Types All Regions" in option:
			year = option[-4:]
			allRegType = allRegionsType(year)
			typePrint(allRegType)

			#We had our custom printing above, no need to print again
			queryCommand = False

		elif "State" in option:
			state = option[-2:]
			xAxis, yAxis = stateOnly(state)
			

		elif "Type" in option:
			allYears = typePerYear()
			typePrint(allYears)

			#We had our custom printing above, no need to print again
			queryCommand = False

		elif "Region" in option:
			reg = option[7:]
			xAxis, yAxis = region(reg)
			

		elif option == "Help":
			queryCommand = False
			help()


		elif "Qtr" in option:
			qtrNum = option[-1]
			xAxis, yAxis = qtrYears(qtrNum)


		elif option == "Exit":
			print("Goodbye!")
			#Note: Cleanly exits without having to import sys
			raise SystemExit


		elif option == "Total":
			xAxis, yAxis = total()

		else:
			#Don't try to print x/y axis data, they're not there
			queryCommand = False
			print("Please enter a valid command, or type 'Help' to view the menu again.")


		if(queryCommand):
			consolePrint(xAxis,yAxis)



#Converts the x/yAxis data required by plotly to a string, then prints
#out to the command line
def consolePrint(xAxis, yAxis):
	#Note: .join() will join every element in the list together with
	#the character calling the function,\t, separating them. 
	xAxisStr = '\t'.join([str(x) for x in xAxis])
	yAxisStr = '\t'.join([str(y) for y in yAxis])
	print("xAxis=" + '\t' + xAxisStr)
	print("yAxis=" + '\t' + yAxisStr)



#Types will have one row for each type in each year, or 3 rows per year,
# so this function prints out the year then it's corresponding x/y data.
def typePrint(allYears):
	for val in allYears:
		#First, identify the year
		print(val[0])
		xAxis = val[1]
		yAxis = val[2]
		#Note: .join() will join every element in the list together with
		#the character calling the function,\t, separating them. 
		xAxisStr = '\t\t'.join([str(x) for x in xAxis[0::2]])
		yAxisStr = ' '.join([str(y) for y in yAxis])
		print("xAxis=" + '\t' + xAxisStr)
		print("yAxis=" + '\t' + yAxisStr)
		print()

main()