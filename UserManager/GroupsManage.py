
from arcgis.gis import GIS
import json, urllib, urllib.parse

#######################
# SET PARAMETERS


# For public access
servicesPublic = {

}

# For partners only
servicesPartner = {
'LIDAR_Tiles_DSM_2016',
'LIDAR_Tiles_DSM_2017',
'DetailedRiverNetwork',
'CatchmentFloodManagementPlanPolicyUnits',
'GroundwaterVulnerability',
'RiskOfFloodingFromSurfaceWaterComplex',
'CoastalOverviewMap',
'FloodMapForPlanningRiversAndSea',
'SensitiveAreas',
'VectorMapLocal',
'Radioactive Substances Register',
'Bathymetry_Coastal_2015',
'Bathymetry_Coastal_2014',
'Bathymetry_Coastal_2016',
'Bathymetry_Coastal_2017',
'Bathymetry_Riverine_2010',
'Bathymetry_Riverine_2011',
'Bathymetry_Riverine_2012',
'Bathymetry_Riverine_2013',
'Bathymetry_Riverine_2015',
'Bathymetry_Riverine_2014',
'Bathymetry_Riverine_2016',
'Bathymetry_Riverine_2017',
'CASI_Multispectral_2014',
'CASI_Multispectral_2013',
'CASI_Multispectral_2012',
'CASI_Multispectral_2015',
'CASI_Multispectral_2016',
'LIDAR_Composite_DSM_1m',
'LIDAR_Composite_DSM_2m',
'LIDAR_Composite_DSM_25cm',
'LIDAR_Composite_DSM_50cm',
'LIDAR_Composite_DTM_25cm',
'LIDAR_Composite_DTM_1m',
'LIDAR_Composite_DTM_50cm',
'LIDAR_Composite_DTM_2m',
'LIDAR_PointCloud_2008',
'LIDAR_PointCloud_2007',
'LIDAR_PointCloud_2005',
'LIDAR_PointCloud_2006',
'LIDAR_PointCloud_2011',
'LIDAR_PointCloud_2012',
'LIDAR_PointCloud_2010',
'LIDAR_PointCloud_2009',
'LIDAR_PointCloud_2014',
'LIDAR_PointCloud_2016',
'LIDAR_PointCloud_2017',
'LIDAR_PointCloud_2013',
'LIDAR_PointCloud_2015',
'Vertical_Photography_IRRGB_2006',
'Vertical_Photography_IRRGB_2007',
'Vertical_Photography_IRRGB_2008',
'Vertical_Photography_IRRGB_2009',
'Vertical_Photography_IRRGB_2010',
'Vertical_Photography_IRRGB_2012',
'Vertical_Photography_IRRGB_2014',
'Vertical_Photography_IRRGBN_2013',
'Vertical_Photography_IRRGBN_2018',
'Vertical_Photography_IRRGBN_2014',
'Vertical_Photography_NightTime_2012',
'Vertical_Photography_NightTime_2009',
'Vertical_Photography_NightTime_2013',
'Vertical_Photography_RGB_2007',
'Vertical_Photography_RGB_2006',
'Vertical_Photography_RGB_2008',
'Vertical_Photography_RGB_2009',
'Vertical_Photography_RGB_2011',
'Vertical_Photography_RGB_2010',
'Vertical_Photography_RGB_2018',
'Vertical_Photography_RGB_2013',
'Vertical_Photography_RGB_2012',
'Vertical_Photography_RGBN_2009',
'Vertical_Photography_RGBN_2008',
'Vertical_Photography_RGBN_2010',
'Vertical_Photography_RGBN_2011',
'Vertical_Photography_RGBN_2013',
'Vertical_Photography_RGBN_2014',
'Vertical_Photography_RGBN_2012',
'Vertical_Photography_RGBN_2015',
'Vertical_Photography_RGBN_2016',
'Vertical_Photography_RGBN_2017',
'LIDAR_Tiles_DSM_1996',
'LIDAR_Tiles_DSM_1998',
'LIDAR_Tiles_DSM_1999',
'LIDAR_Tiles_DSM_2000',
'LIDAR_Tiles_DSM_2001',
'LIDAR_Tiles_DSM_2002',
'LIDAR_Tiles_DSM_2005',
'LIDAR_Tiles_DSM_2004',
'LIDAR_Tiles_DSM_2003',
'LIDAR_Tiles_DSM_2006',
'LIDAR_Tiles_DSM_2007',
'LIDAR_Tiles_DSM_2008',
'LIDAR_Tiles_DSM_2010',
'LIDAR_Tiles_DSM_2012',
'LIDAR_Tiles_DSM_2011',
'LIDAR_Tiles_DSM_2009',
'LIDAR_Tiles_DSM_2013',
'LIDAR_Tiles_DSM_2014',
'LIDAR_Tiles_DSM_2015',
'LIDAR_Tiles_DSM_2018',
'LIDAR_Tiles_DTM_2000',
'LIDAR_Tiles_DTM_1998',
'LIDAR_Tiles_DTM_1999',
'LIDAR_Tiles_DTM_2004',
'LIDAR_Tiles_DTM_2005',
'LIDAR_Tiles_DTM_2002',
'LIDAR_Tiles_DTM_2003',
'LIDAR_Tiles_DTM_2006',
'LIDAR_Tiles_DTM_2009',
'LIDAR_Tiles_DTM_2007',
'LIDAR_Tiles_DTM_2008',
'LIDAR_Tiles_DTM_2012',
'LIDAR_Tiles_DTM_2010',
'LIDAR_Tiles_DTM_2011',
'LIDAR_Tiles_DTM_2013',
'LIDAR_Tiles_DTM_2017',
'LIDAR_Tiles_DTM_2016',
'LIDAR_Tiles_DTM_2015',
'LIDAR_Tiles_DTM_2018',
'LIDAR_Tiles_DTM_2001',
'LIDAR_Tiles_DTM_2014',
'OS25kRaster',
'OS50kRaster',
'VectorMapLocalBlackAndWhiteRaster',
'VectorMapLocalColourRaster',
'VectorMapLocalBackdropRaster',
'Digital_Surface_Data_2m',
'CIR_Imagery_50cm',
'Digital_Terrain_Data_5m',
'FloodDepthGrid20mP',
'FloodDepthGrid20mP',
'OS25kRaster',
'OS50kRaster',
'VectorMapLocalColourRaster',
'VectorMapLocalBackdropRaster',
'VectorMapLocalBlackAndWhiteRaster',
'Contours_5m',
'OSCodePoint',
'Bathymetry_Coastal_2018',
'Bathymetry_Riverine_2018',
'LIDAR_PointCloud_2018',
'Vertical_Photography_IRRGB_2018',
'Vertical_Photography_RGBN_2018',
'Oblique_Photography_IncidentResponse_2018',
'National_LIDAR_Programme_Point_Cloud_2018',
'National_LIDAR_Programme_DSM_2016',
'National_LIDAR_Programme_DSM_2017',
'National_LIDAR_Programme_DSM_2018',
'National_LIDAR_Programme_DTM_2016',
'National_LIDAR_Programme_DTM_2017',
'National_LIDAR_Programme_DTM_2018',
'National_LIDAR_Programme_First_Return_DSM_2016',
'National_LIDAR_Programme_First_Return_DSM_2017',
'National_LIDAR_Programme_First_Return_DSM_2018',
'National_LIDAR_Programme_Intensity_2017',
'National_LIDAR_Programme_Intensity_2018',
'National_LIDAR_Programme_Point_Cloud_2016',
'National_LIDAR_Programme_Point_Cloud_2017',
'National_LIDAR_Programme_Intensity_2016',
'EA_Integrated_Height_Model_Catalogues',
'EA_Integrated_Height_Model',
'EA_SurfZone_DEM',
'LIDAR_PointCloud_2019',
'LIDAR_Tiles_DSM_2019',
'LIDAR_Tiles_DTM_2019',
'National_LIDAR_Programme_First_Return_DSM_2019',
'National_LIDAR_Programme_Intensity_2019',
'National_LIDAR_Programme_Point_Cloud_2019',
'National_LIDAR_Programme_DSM_2019',
'National_LIDAR_Programme_DTM_2019',
'LIDAR_Composite_DTM_2m_2019',
'LIDAR_Composite_DTM_1m_2019'
}
# Add Group names from list of Groups below
# Service Owner added automatically below
allowedGroups = []
#allowedGroups = ['Defra-body Contractors']
# END OF SETTINGS
#######################

#Prompt to set environemt and Checking for allowed prompt values

while True:
    environment = input("Select environment - TEST UAT PROD: ")
    if str.upper(environment) != 'TEST' and str.upper(environment) != 'UAT' and str.upper(environment) != 'PROD':
        print ("Invalid Environment parameter entered")
        continue
    else:
        break

print ("You are working in "  + str.upper(environment))



#Groups and IDs in TEST
#https://environment-test.data.gov.uk/portal/sharing/rest/community/users/portaladmin?f=pjson

groupsTEST = {
'Agriculture & Horticulture Development Board' : 'eddb3184eb1d434ebc588694ff6e346e',
'Animal & Plant Health Agency' : '0fd45dbf001946cdb1bd268f75a5f030',
'Centre for Environment, Fisheries & Aquaculture Science' : '0f12c24a16c24e9399fc7cd804b6a467',
'Consumer Council for Water' : '3646edb71d6e408884e11d9b8fcbda54',
'Data Share Maps and Apps' : 'd6ff4382a0924822b212bdb8c05ad9b7',
'Defra-body Contractors' : 'fbd9d465e8d143eca25b184b91ba379f',
'Defra-body Staff' : '563dd6ed159b4c5a9300cc074343e082',
'Defra Contractor Proxy' : '80234d2c7a504813b66231bc72b4397a',
'Department for Environment, Food & Rural Affairs' : 'a4fbd192a4d84d19bfac719b390b34a8',
'Environment Agency' : '95932043253d4b98b1d817445b577e60',
'Featured Maps and Apps' : 'c36d1045d2524174b9c39365ffc69d80',
'Forestry Commission' : '19526bd0716a44a68b95452b15a289d7',
'Joint Nature Conservation Committee' : '92db05416d644ec6a1df0cd824c9130d',
'Marine Management Organisation' : '7638f894010d4fb3abd62c659902262c',
'National Forest Company' : '87012cf6858c493484862e378081e317',
'Natural England' : '52f85a99716b44ccb7abdd5716a4d5fe',
'PSMA' : 'f30b7df992794c6ebb7750bc05cbba72',
'Royal Botanic Gardens, Kew' : '0d8a1c836c9d40c292a8ad51273a89c4',
'Rural Payments Agency' : 'e4eadf6f71574a1e95f29e441aab74ef',
'Sea Fish Industry Authority' : '435bfac5ce6d4c03966bf22dd100a157',
'Service Owner' : '507c841c900e4b29ac3d4e14d61c7f82',
'Veterinary Medicines Directorate' : 'b3f5bf5b4df741e9ba33e2af884c3127',
'WFD/CaBA/IDB' : '33e1eb8c0bec4cf68270982c43c2d413'
}

#Groups and IDs in UAT
groupsUAT = {
'Agriculture & Horticulture Development Board' : '584aee096ce34e339296f3a88c4cdb45',
'Animal & Plant Health Agency' : 'e452858c64bb4c8ab513138708272b29',
'Centre for Environment, Fisheries & Aquaculture Science' : '9b1a4b29a554488ea8b79cc55803c66f',
'Consumer Council for Water' : '1a074fbf41054ffb8b55a357d88f2ed1',
'DEFRA' : '416c51cd60ee4b999ec4d22ea2e60e12',
'Defra-body Contractors' : '2e748c0cf76c43c59610f6cc1222c93a',
'Defra-body Staff' : '96209181d95e42d2826dc755d4bd9dbb',
'Department for Environment, Food & Rural Affairs' : '2dcbbceff72c4bf983ae8c4c9ee353bd',
'Environment Agency' : 'ee7c0aa43d1e4108b687f224874d5752',
'Featured Maps and Apps' : 'ab387e9ef53648df8d3abd756af24174',
'Forestry Commission' : '60f7fff245f94ac1942a8019b7722f9e',
'Joint Nature Conservation Committee' : 'e490244a77cc4a61a4d796db939cbee5',
'Marine Management Organisation' : '054f24cba30f411992e3027b32951d42',
'National Forest Company' : '947dd33a9c2b41eb81bed8cd1010b8c0',
'Natural England' : '130074ffc9ae4998b29cfe04be24b2e5',
'Pre-Publication Area - DEFRA' : '4270f7b4191e4f5a98ffcf3e0c4ffebe',
'Pre-Publication Area - EA' : 'e2bc9c695cbe48c7af66b3e975b71b86',
'Pre-Publication Area - FC' : 'be3da176f0794ece824ce2d87a9abfb0',
'Pre-Publication Area - HE' : '677305d4cd514595a1829c2903cb28f4',
'Pre-Publication Area - MMO' : 'a4e5e35a80af4986ab76b342a936ed84',
'Pre-Publication Area - NE' : '68dbc465a3574f7e92f6255b239a59a7',
'Pre-Publication Area - RPA' : '06a4d2206400412bbdc2e99c4f79909b',
'PSMA' : '4f97b9e5afa743c18ae942962314d850',
'Royal Botanic Gardens, Kew' : '29ff02595a804c4e92cc05f1b967d567',
'Rural Payments Agency' : '9d2e6f9c4e6d4ac99b82e6e912075318',
'Sea Fish Industry Authority' : '21340c7a49b94cf89be2e7de8cd30fed',
'Service Owner' : '0f771a13934047a79dfbfcb67fc1a630',
'Veterinary Medicines Directorate' : 'ee3fc8826b564c389bc415e4e81a7d81',
'WFD/CaBA/IDB' : '3d885fd62dbd4ef1a640634cfa8d19ef'
}


#Groups and IDs in PROD
groupsPROD = {
'Agriculture & Horticulture Development Board' : '6e700e77844144fd9ee391b59310f322',
'Animal & Plant Health Agency' : '29cc6b9743b340999c094707f7c4da71',
'Centre for Environment, Fisheries & Aquaculture Science' : 'cd59819cb8564ddbb7cc9e5c99d065fb',
'Consumer Council for Water' : '5e6325cac2104947b95cef3fd2b71406',
'Data Share Maps and Apps' : '145abc3997e2433ca62c7b0e63b899f8',
'Defra-body Contractors' : '553e77d681394518904c544599ded458',
'Defra-body Staff' : '422c2d6662154d22b3fbeff47704c87f',
'Department for Environment, Food & Rural Affairs' : '876fb83b9000457f84cecd4e1c28550f',
'Environment Agency' : '564ec34edc50486dabccd5504a71d74d',
'Featured Maps and Apps' : '09065e5f72da4e18bafa4bf1945df52e',
'Forestry Commission' : '1a035856899e4977a47c17f733917e1d',
'Joint Nature Conservation Committee' : '9da328aa2eb2445ba5de196921c49dce',
'Marine Management Organisation' : 'c071a22fa0424cd7a170b05cb4703cbb',
'National Forest Company' : 'd7e636a519a14add8672b29829ef4fef',
'Natural England' : '1cf0a379189746a3bcc6e0a94449e9a7',
'PSMA' : '8b3830101e7b493eaeb1498fe710ea62',
'Royal Botanic Gardens, Kew' : '752927f7b0644fed8ffd37b926f1a59d',
'Rural Payments Agency' : '6a070f63981744c19e5ee0df56417cea',
'Sea Fish Industry Authority' : '2d96d751bc4f4c8183c80134434236f2',
'Service Owner' : '48c318fc8faf4bcb9cec735e9a4de93e',
'Veterinary Medicines Directorate' : '139e05a3ee3d42b69447b8f7a4f63548',
'WFD/CaBA/IDB' : '713ebfcd8b1744c39f7987a9579ea88b'
}

# Admin/publisher user name and password
if str(environment) == 'TEST':  
    portalUser = "portaladmin"
    portalPWD = "AGS3nt3rpr!$3Adm!n"
    envURL = "https://environment-test.data.gov.uk/portal"
    groupsInPortal = groupsTEST
if str(environment) == 'UAT':  
    portalUser = "portaladmin"
    portalPWD = "AGS3nt3rpr!$3Adm!n"
    envURL = "https://environment-uat.data.gov.uk/portal"
    groupsInPortal = groupsUAT
if str(environment) == 'PROD':  
    portalUser = "portaladmin"
    portalPWD = "AGS3nt3rpr!$3Adm!n"
    envURL = "https://environment.data.gov.uk/portal"
    groupsInPortal = groupsPROD   


##token = getToken(portalUser, portalPWD, envURL)
#Log into ArcGIS Online by making a GIS connection to ArcGIS Online using your developer account. Replace username and password with your own credentials.
gis = GIS(envURL, portalUser, portalPWD, verify_cert=False)
print("Successfully logged in as: " + gis.properties.user.username)



			

#Search for specific dataset or type.
if len(servicesPublic) == 0:
    print("No Public Services")
else:    
    for service in servicesPublic:
        resultsItems = gis.content.search(query='owner:portaladmin title:' + service, max_items=1000, outside_org=False, sort_field="title", sort_order="asc")

        #Retrieve the Item collection item from the list of results.
        for resultItem in resultsItems:    
        ##    for item in resultItem:
        ##        print(item)
            try:
                resultItem.share(everyone=True,org=True)
                print ("Permissions changed to Everyone " + resultItem.title)
            except:
                print ("An Error occurred whilst trying to change permissions")

if len(servicesPartner) == 0:
    print("No Partner Services")
else:
    #Get Portal Groups.
    groupNames = []
    groupIDs = []
    allowedGroups.append('Service Owner')
    for key,val in groupsInPortal.items():
        if key in allowedGroups:
            groupNames.append(key)
            groupIDs.append(val)
    allowedGroupNames = ';'.join(groupNames)
    allowedGroupsIDs = ','.join(groupIDs)

    for service in servicesPartner:
        #resultsItems = gis.content.search(query='owner:portaladmin title:' + service, max_items=1000, outside_org=False, sort_field="title", sort_order="asc")
        resultsItems = gis.content.search(query='owner:portaladmin title:' + service)
        #Retrieve the Item collection item from the list of results.
        for resultItem in resultsItems:    
        ##    for item in resultItem:
        ##        print(item)
            try:
        ##        resultItem.share(everyone=False,org=True)
        ##        for public datasets
        ##        resultItem.share(everyone=True,org=True)	
        ##        resultItem.share(org=False)
        ##        resultItem.share(groups='96209181d95e42d2826dc755d4bd9dbb,0f771a13934047a79dfbfcb67fc1a630,2e748c0cf76c43c59610f6cc1222c93a,3d885fd62dbd4ef1a640634cfa8d19ef,4f97b9e5afa743c18ae942962314d850')
        ##        print ("Permissions changed to the following groups -  Defra-body Staff;Service Owner;Defra-body Contractors;WFD/CaBA/IDB;PSMA; successfully for service: " + resultItem.title)
        ##        resultItem.share(groups='96209181d95e42d2826dc755d4bd9dbb,0f771a13934047a79dfbfcb67fc1a630,2e748c0cf76c43c59610f6cc1222c93a')
        ##        print ("Permissions changed to the following groups -  Defra-body Staff;Service Owner;Defra-body Contractors; successfully for service: " + resultItem.title)
                resultItem.share(groups=allowedGroupsIDs)
                #resultItem.unshare(allowedGroupsIDs)
                print ("Permissions changed to the following groups - "  + allowedGroupNames + " successfully for service: " + resultItem.title)
            except:
                print ("An Error occurred whilst trying to change permissions")
            #resultItem.unshare('054f24cba30f411992e3027b32951d42')
print('Script execution complete')

