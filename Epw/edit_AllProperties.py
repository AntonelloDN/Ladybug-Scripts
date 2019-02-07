
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
	
	variables = {
		'0':epw_data.years
		,'1':epw_data.dry_bulb_temperature
		,'2':epw_data.dew_point_temperature
		,'3':epw_data.relative_humidity
		,'4':epw_data.atmospheric_station_pressure
		,'5':epw_data.extraterrestrial_horizontal_radiation
		,'6':epw_data.extraterrestrial_direct_normal_radiation
		,'7':epw_data.horizontal_infrared_radiation_intensity
		,'8':epw_data.global_horizontal_radiation
		,'9':epw_data.direct_normal_radiation
		,'10':epw_data.diffuse_horizontal_radiation
		,'11':epw_data.global_horizontal_illuminance
		,'12':epw_data.direct_normal_illuminance
		,'13':epw_data.diffuse_horizontal_illuminance
		,'14':epw_data.zenith_luminance
		,'15':epw_data.wind_direction
		,'16':epw_data.wind_speed
		,'17':epw_data.total_sky_cover
		,'18':epw_data.opaque_sky_cover
		,'19':epw_data.visibility
		,'20':epw_data.ceiling_height
		,'21':epw_data.present_weather_observation
		,'22':epw_data.present_weather_codes
		,'23':epw_data.precipitable_water
		,'24':epw_data.aerosol_optical_depth
		,'25':epw_data.snow_depth
		,'26':epw_data.days_since_last_snowfall
		,'27':epw_data.albedo
		,'28':epw_data.liquid_precipitation_depth
		,'29':epw_data.liquid_precipitation_quantity
		,'30':epw_data.sky_temperature
	}
	
	selectedVar = variables[str(index)]
	
	
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

	inputVar = int(input("3. Write index to change variables you want:\n0 = years\n1 = dry_bulb_temperature\n2 = dew_point_temperature\n3 = relative_humidity\n4 = atmospheric_station_pressure\n5 = extraterrestrial_horizontal_radiation\n6 = extraterrestrial_direct_normal_radiation\n7 = horizontal_infrared_radiation_intensity\n8 = global_horizontal_radiation\n9 = direct_normal_radiation\n10 = diffuse_horizontal_radiation\n11 = global_horizontal_illuminance\n12 = direct_normal_illuminance\n13 = diffuse_horizontal_illuminance\n14 = zenith_luminance\n15 = wind_direction\n16 = wind_speed\n17 = total_sky_cover\n18 = opaque_sky_cover\n19 = visibility\n20 = ceiling_height\n21 = present_weather_observation\n22 = present_weather_codes\n23 = precipitable_water\n24 = aerosol_optical_depth\n25 = snow_depth\n26 = days_since_last_snowfall\n27 = albedo\n28 = liquid_precipitation_depth\n29 = liquid_precipitation_quantity\n30 = sky_temperature\n\n"))
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

