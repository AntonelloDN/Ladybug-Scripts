# Ladybug-Scripts: Example of components that use Ladybug[+] module started by Mostapha Sadeghipour Roudsari
# This file is part of Ladybug-Scripts - Antonello Di Nunzio (antonellodinunzio@gmail.com)
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
    Inputs:
        runIt: Run the component
        _epwFile: Absolute path of the file.
        _analysisPeriod: AnalysisPeriod that indicate the interval where replace values
        _index: 0 for temperature OR 1 for relative_humidity
        _listValues: List of number to use in the new EPW in the specific AnalysisPeriod
    Output:
        newFile: new Epw file
"""
ghenv.Component.Name = "LadybugPlus_Edit Temperature Relative Humidity"
ghenv.Component.NickName = 'edit_TemperatureRelatiHumidity'
ghenv.Component.Message = 'VER 0.0.04\nFEB_16_2018'
ghenv.Component.Category = "LadybugPlus"
ghenv.Component.SubCategory = '04 :: LadybugPlus-Scripts'
ghenv.Component.AdditionalHelpFromDocStrings = "1"

import os
from ladybug.epw import EPW
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.datacollection import DataCollection

print("1. Index 0 for temperature OR Index 1 for relative humidity")

if runIt:
    # Load epw
    epw_data = EPW(_epwFile)
    
    # Extract climate var
    selectedVar = epw_data.dry_bulb_temperature if (_index == 0) else epw_data.relative_humidity
    
    # Create AnalysisPeriod and DataCollection
    data_collection = DataCollection(selectedVar)
    
    # Folder and file
    my_folder = os.path.dirname(_epwFile)
    my_file = "mod" + os.path.split(_epwFile)[1]
    
    # Check inputs length
    if (len(_analysisPeriod.hoys) == len(_listValues)):
        data_collection.update_data_for_analysis_period(_listValues, _analysisPeriod) 
        epw_data.save(folder=my_folder, file_name=my_file)
        newFile = os.path.join(my_folder, my_file)
