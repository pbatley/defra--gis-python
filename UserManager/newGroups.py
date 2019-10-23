import csv
import sys
import os
import json
import traceback
import json
import argparse

from arcgis.gis import GIS

envURL="https://environment-uat.data.gov.uk/portal"
portalOwner = "portaladmin"
portalPWD = "ArcG!$3nt3rpr!$3Adm!n"
dataFile = '\\data\\data.csv'
#group = {'access' : 'private',
#          'description' : 'Group for DEFRA Lead Service Managers',
#          'isFav' : 'FALSE',
#          'isInvitationOnly': 'TRUE',
#          'isViewOnly' : 'FALSE',
#          'phone' : 'null',
#          'snippet' : 'Group for DLSM-restricted data',
#          'sortField' : 'title',
#          'sortOrder' : 'asc',
#          'tags' : 'DLSM',
#          'thumbnail' : '',
#          'title' : 'DEFRA Lead Service Managers'
#}
groups = dict({'DLSM' : 
               {'access' : 'private',
              'description' : 'Group for DEFRA Lead Service Managers',
              'isFav' : 'FALSE',
              'isInvitationOnly': 'TRUE',
              'isViewOnly' : 'FALSE',
              'phone' : 'null',
              'snippet' : 'Group for DLSM-restricted data',
              'sortField' : 'title',
              'sortOrder' : 'asc',
              'tags' : 'DLSM',
              'thumbnail' : '',
              'title' : 'DEFRA Lead Service Managers'
              },
              'Publishers' : {'access' : 'private',
              'description' : 'Group for DEFRA Publishers',
              'isFav' : 'FALSE',
              'isInvitationOnly': 'TRUE',
              'isViewOnly' : 'FALSE',
              'phone' : 'null',
              'snippet' : 'Group for Publishers-restricted data',
              'sortField' : 'title',
              'sortOrder' : 'asc',
              'tags' : 'Publishers',
              'thumbnail' : '',
              'title' : 'DEFRA Publishers'
              }
              }
              )
   

try:
    gis = GIS(envURL, portalOwner, portalPWD, verify_cert=False)
    print("Successfully logged in as: " + gis.properties.user.username)
    i=0
    for group in groups.items():
        try:
            print("\nCreating group: " + group[1]['title'])
            result = True #gis.groups.create_from_dict(group)
            if result:
                print("success")
            i += 1
        except Exception as create_ex:
            print("Error... ", str(create_ex))

except Exception as gen_ex:
    print("Error... ", str(gen_ex))
