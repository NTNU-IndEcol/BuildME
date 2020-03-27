
import subprocess


#Testing how to run energy plus - it works :---)



import os
os.chdir(r'C:\testing-ep\update')
print(os.getcwd())

subprocess.call([r'C:\testing-ep\energyplus.exe', '-w', r'C:\testing-ep\update\try_weather.epw', '-r', r'C:\testing-ep\update\IECC_ApartmentHighRise_STD2006_Chicago_updated_v901.idf'])

#subprocess.call([r'C:\Users\andrenis\gitprojects\BuildME\tmp\USA_SFH_standard_RES0_8_2015\energyplus.exe', '-w', r'C:\Users\andrenis\gitprojects\BuildME\tmp\USA_SFH_standard_RES0_8_2015\in.epw', r'C:\Users\andrenis\gitprojects\BuildME\tmp\USA_SFH_standard_RES0_8_2015\expanded.idf'])

#subprocess.call([r'C:\testing-ep\trysimulation\energyplus.exe', '-w', r'C:\testing-ep\trysimulation\USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw', r'C:\testing-ep\trysimulation\MFH.idf'], stdout ="log.txt", stderr="log.txt")




#subprocess.call([r'C:\testing-ep\trysimulation\energyplus.exe', '-w', r'C:\testing-ep\trysimulation\USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw', r'C:\testing-ep\trysimulation\MFH.idf'])
#with open("log.txt", 'w+') as log_file:
#    subprocess.call([r'C:\testing-ep\trysimulation\energyplus.exe', '-w', r'C:\testing-ep\trysimulation\USA_VA_Sterling-Washington.Dulles.Intl.AP.724030_TMY3.epw', r'C:\testing-ep\trysimulation\MFH.idf'])'''