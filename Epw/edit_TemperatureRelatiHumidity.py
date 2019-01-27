
import os
from ladybug.epw import EPW
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.datacollection import DataCollection


def create_analysisPeriod(params):
	"""Provide a list of 6 integer.
		
		description: st_month, st_day, st_hour, end_month, end_day, end_hour.
		1 is 1 AM
		0 is 12 AM
		Eg. JAN 1st [1,1,1,1,2,0]
	
    Args:
        params (list): list of 6 integer Eg.[1,1,1,1,2,0]

    Returns:
        result (AnalysisPeriod): AnalysisPeriod obj.
	"""
	params = list(map(str, params))
	
	return AnalysisPeriod(params[0],params[1],params[2],params[3],params[4],params[5])


def modify_epw(file_to_change, output_full_path, analysis_period, index, input_list):
	"""Provide an EPW and change some values of temperature OR relative humidity.
	
    Args:
        file_to_change (string): Absolute path of the file.  E.g. C:\\...\\StartExample.epw
		output_full_path (string): Absolute path of the new EPW to write. E.g. C:\\...\\OutExample.epw
		analysis_period (AnalysisPeriod): AnalysisPeriod that indicate the interval where replace values
		index (int): 0 for temperature OR 1 for relative_humidity
		input_list (list float): List of number to use in the new EPW in the specific AnalysisPeriod

    Returns:
        result (bool): True, if it run correctly.
	"""
	
	# Load epw
	epw_data = EPW(file_to_change)
	
	# Extract climate var
	selectedVar = epw_data.dry_bulb_temperature if (index == 0) else epw_data.relative_humidity

	# Create AnalysisPeriod and DataCollection
	data_collection = DataCollection(selectedVar)
	
	# Check inputs length
	if (len(analysis_period.hoys) == len(input_list)):
		data_collection.update_data_for_analysis_period(input_list, analysis_period) 
		epw_data.save(file_path = output_full_path)
		return True

		
def main():
	
	print("1. Write: st_month,st_day,st_hour,end_month,end_day,end_hour. E.g. 1,1,1,1,2,0")
	inputInterval = input("").split(',')
	
	# AnalysisPeriod
	analysisPeriod = create_analysisPeriod(inputInterval)
	lenInterval = len(analysisPeriod.hoys)
	
	print("n. values = {}".format(lenInterval))
	print("")
	
	inputFile = input("2. Write the absolute path of the EPW file to change:\n")
	outputPath = os.path.join(os.path.dirname(inputFile), "mod" + os.path.split(inputFile)[1])
	print("")

	inputVar = int(input("3. Write 0 for temperature OR write 1 for relative humidity:\n"))
	print("")
	
	print("4. Write {} numbers that you want to apply in your new EPW: E.g. 15.4,23.4,24.0,25.7\n".format(lenInterval))
	inputValues = input("").split(',')
	inputVal = [float(num.replace(" ", "")) for num in inputValues]
	print("")
	
	writeNewEpw = modify_epw(inputFile, outputPath, analysisPeriod, inputVar, inputVal)
	
	if writeNewEpw:
		print("OK! Check {}".format(outputPath))
	else:
		print("Please, connect a list of values with the same length of the analysis period")

	
if __name__ == '__main__':

	# Run
	main()

