import csv
import sys
import os
import json
import traceback
import json
import argparse

from arcgis.gis import GIS

envURL="https://environment.data.gov.uk/portal"
portalOwner = "portaladmin"
portalPWD = "ArcG!$3nt3rpr!$3Adm!n"
dataFile = '\\data\\data.csv'

try:

	gis = GIS(envURL, portalOwner, portalPWD, verify_cert=False)
	print("Successfully logged in as: " + gis.properties.user.username)

	#Now create your groups using the CSV File
	csv_file = os.getcwd() + dataFile
	with open(csv_file, 'r') as groups_csv:
		groups = csv.DictReader(groups_csv)
		for group in groups:
			try:
				print("\nCreating group: "+ group['title'])
				result = gis.groups.create_from_dict(group)
				if result:
					print("success")

			except Exception as create_ex:
				print("Error... ", str(create_ex))

except Exception as gen_ex:
	print("Error... ", str(gen_ex))
