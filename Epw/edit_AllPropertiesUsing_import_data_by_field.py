
import os
from ladybug.epw import EPW
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.datacollection import DataCollection


def create_analysisPeriod(params):
	"""Provide a list of 6 integer.
		
		description: st_month, st_day, st_hour, end_month, end_day, end_hour.
		1 is 1 AM
		0 is 12 PM
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
		index (int): 
				Year (0) –
				Month (1) –
				Day (2) –
				Hour (3) –
				Minute (4) –
				- –
				Dry Bulb Temperature (6) –
				Dew Point Temperature (7) –
				Relative Humidity (8) –
				Atmospheric Station Pressure (9) –
				Extraterrestrial Horizontal Radiation (10) –
				Extraterrestrial Direct Normal Radiation (11) –
				Horizontal Infrared Radiation Intensity (12) –
				Global Horizontal Radiation (13) –
				Direct Normal Radiation (14) –
				Diffuse Horizontal Radiation (15) –
				Global Horizontal Illuminance (16) –
				Direct Normal Illuminance (17) –
				Diffuse Horizontal Illuminance (18) –
				Zenith Luminance (19) –
				Wind Direction (20) –
				Wind Speed (21) –
				Total Sky Cover (22) –
				Opaque Sky Cover (23) –
				Visibility (24) –
				Ceiling Height (25) –
				Present Weather Observation (26) –
				Present Weather Codes (27) –
				Precipitable Water (28) –
				Aerosol Optical Depth (29) –
				Snow Depth (30) –
				Days Since Last Snowfall (31) –
				Albedo (32) –
				Liquid Precipitation Depth (33) –
				Liquid Precipitation Quantity (34) –
		input_list (list float): List of number to use in the new EPW in the specific AnalysisPeriod

    Returns:
        result (bool): True, if it run correctly.
	"""
	
	# Load epw
	epw_data = EPW(file_to_change)
	
	# Extract climate var
	selectedVar = epw_data.import_data_by_field(int(index))
	
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

	inputVar = int(input("3. Write index to change variables you want:\nDry Bulb Temperature (6)\nDew Point Temperature (7)\nRelative Humidity (8)\nAtmospheric Station Pressure (9)\nExtraterrestrial Horizontal Radiation (10)\nExtraterrestrial Direct Normal Radiation (11)\nHorizontal Infrared Radiation Intensity (12)\nGlobal Horizontal Radiation (13)\nDirect Normal Radiation (14)\nDiffuse Horizontal Radiation (15)\nGlobal Horizontal Illuminance (16)\nDirect Normal Illuminance (17)\nDiffuse Horizontal Illuminance (18)\nZenith Luminance (19)\nWind Direction (20)\nWind Speed (21)\nTotal Sky Cover (22)\nOpaque Sky Cover (23)\nVisibility (24)\nCeiling Height (25)\nPresent Weather Observation (26)\nPresent Weather Codes (27)\nPrecipitable Water (28)\nAerosol Optical Depth (29)\nSnow Depth (30)\nDays Since Last Snowfall (31)\nAlbedo (32)\nLiquid Precipitation Depth (33)\nLiquid Precipitation Quantity (34)\n\n"))
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

