from arcgis.gis import GIS, User, UserManager, GroupManager, Group

import json, urllib, urllib.parse, csv, os, sys

        
envURL="https://environment-test.data.gov.uk/portal"
portalOwner = "portaladmin"
portalPWD = "ArcG!$3nt3rpr!$3Adm!n"
userSearch = None
groupSearch = None
groupSearchWithMembers = None
dataFile = '\\data\\level2Migration.csv'
grpids = 'Service'
#uids = {#'joanna.whittle@environment-agency.gov.uk': 'EA',
#        'dan.haigh@environment-agency.gov.uk': 'EA',
#        "huw.buckley@naturalengland.org.uk": 'NE',
#        "mark.rogers@naturalengland.org.uk": 'NE',
#        "linda.edwards@naturalengland.org.uk": 'NE',
#        "adam.tobin@environment-agency.gov.uk": 'EA', #(UAT only)
#        "philip.woodhouse@environment-agency.gov.uk": ['EA', 'DEFRA']
#        "andrew.twigg@environment-agency.gov.uk": 'EA',
#        "mark.saunders@environment-agency.gov.uk": 'EA',
#        "iain.urquhart@environment-agency.gov.uk": 'EA',
#        "andrew.lee@naturalengland.org.uk": 'NE - Pre-Publication',
#        "barbara.kitrys@environment-agency.gov.uk": 'EA - Pre-Publication'
#        "ian.denham@naturalengland.org.uk": 'NE',
#        "finbar.riley@marinemanagement.org.uk": 'MMO',
#        "william.carney@marinemanagement.org.uk": 'MMO',
#        "rupert.waite1@rpa.gov.uk": 'RPA',
#        "brian.o'toole@rpa.gov.uk": 'RPA',
#        "john.joseph@defra.gov.uk": 'DEFRA'
#'adam.tobin@environment-agency.gov.uk': ['EA - Pre-Publication', 'DEFRA - Pre-Publication'],
#'finbar.riley@marinemanagement.org.uk': 'MMO - Pre-Publication',
#'william.carney@marinemanagement.org.uk': 'MMO - Pre-Publication'
#}
uids = {}


try:
    gis = GIS(envURL, portalOwner, portalPWD, verify_cert=False)
    print("Successfully logged in as: " + gis.properties.user.username)
except Exception as e:     
    print('An Error occurred ' + e.args[0] + ' trying to log in')


def updateUser(userList, userLevel, userGroup):
    user = None

    def updateUserLevels():
        try:            
            user.update_level('2')
            user.update_role('org_user')
            print('Full name: ' + userID.fullName)
            print('User name: ' + userID.username)
            print('Email: ' + userID.email)
            print('Applying change to user level: ' + userID.email)
        except Exception as e:
            print('An error occurred: ' + e.args[0] + ' updating user')


    def addUserToGroup(grpObj):
        try:
            UpdateGroup(grpObj, user)
        except Exception as e:
            print('An error occurred adding the user to group: ' + grpObj)


    def runUpdate():
        try:
            if userLevel:
                updateUserLevels()
            if userGroup:
                if isinstance(uids, dict):
                    for id, grps in uids.items():
                        if isinstance(grps, list):
                            for grp in grps:
                                if id == user.email:
                                    addUserToGroup(grp)
                        else:
                            if id == user.email:
                                addUserToGroup(grps) 
                if isinstance(uids, list):
                    grpObj = getGroups(None, None)
                    addUserToGroup(grpObj)
        except Exception as e:
            print('An error occurred updating user \n' + e.args[0]) 
    try:
        for userID in userList:
            user = User(gis, userID.username)
            if userID.username != portalOwner:
                runUpdate()
    except Exception as e:
        print('An error occurred retrieving user - ' + e.args[0])


def getUsers(ids):
    try:
        users = gis.users
        userSearch = []

        if isinstance(ids, dict):
            for id in ids:
                userResults = users.search(query=id, sort_field='full_name', max_users=1000)        
                userSearch += userResults
                for userResult in userResults:            
                    if id == userResult.email:
                        print('Full name: ' + userResult.fullName)
                        print('User name: ' + userResult.username)
                        print('Email: ' + userResult.email)
                        print('Level: ' + userResult.level)
                        print('Role: ' + userResult.role)
                        userGrps = 'User Groups: \n'
                        for grp in userResult.groups:
                            userGrps += grp.title +'\n'
                        print(userGrps)            
        else:
            userResults = users.search(query=ids, sort_field='full_name', max_users=1000)        
            userSearch += userResults
            for userResult in userResults:                           
                print('Full name: ' + userResult.fullName)
                print('User name: ' + userResult.username)
                print('Email: ' + userResult.email)
                print('Level: ' + userResult.level)
                print('Role: ' + userResult.role)
                userGrps = 'User Groups: \n'
                for grp in userResult.groups:
                    userGrps += grp.title +'\n'
                print(userGrps)

        return userSearch
    except Exception as e:
        print('An error occurred: ' + e.args[0] + ' getting user')


def getGroups(grpObj, members):
    try:
        groups = gis.groups
        #if isinstance(grpObj, str):
        #    grpObj = 'title: ' + grpObj + ' AND owner: ' + portalOwner
        #    groupResults = groups.search(query=grpObj, sort_field='title', outside_org=False)
        #else:
        #    grpObj = 'owner: ' + portalOwner
        groupResults = groups.search(query=grpObj, sort_field='title', outside_org=False)
        groupMembers = None
        groupResultSet = []
        for groupResult in groupResults:
            if groupResult.owner == portalOwner:
                if not isinstance(groupResult.description, str):
                    groupResult.description = 'None'
                print('Group Title: '  + groupResult.title + '\n' + 
                      ' - Group ID: '  + groupResult.id + '\n' + 
                      ' - Group Owner: ' + groupResult.owner + '\n' + 
                      ' - Group Description: ' + groupResult.description)
                groupTags = ' - Group Tags: '
                for groupTag in groupResult.tags:
                    groupTags += groupTag + ' '
                print(groupTags)
                if members:
                    groupMembers = getGroupMembers(groupResult)
                    print('\n')
                groupResultSet.append(groupResult)

        return groupResultSet, groupMembers                
    except Exception as e:
        print('An Error occurred getting Groups information - ' + e.args[0])


def UpdateGroup(grpObj, user):
    try:
        if isinstance(grpObj, str):
            groupResults = getGroups(grpObj, None)
            i=0
            for groupResult in groupResults[0]:
                #group = Group(gis, groupResult.id)
                groupResult.add_users(user.username)
                i +=1
                print('Adding user: ' + user.email + ' to Group: ' + groupResult.title)
        else:
            groupResults = grpObj
            i=0
            for groupResult in groupResults[0]:
                groupResult.add_users(user.username)
                print('Adding user: ' + user.email + ' to Group: ' + groupResult.title)
                i += 1
    except Exception as e:
        print('An error occurred updating group - ' + e.args[0])


def getGroupMembers(grpObj):
    try:        
        group = grpObj
        grpMembers = group.get_members()
        print('Group Managers: ')
        grpUsers = []
        for grpAdmin in grpMembers['admins']:
            user = User(gis, grpAdmin)
            print('Username: ' + user.username +
                  ' - Full Name: ' + user.fullName +
                  ' - Email: ' + user.email)
            grpUsers.append(user)

        print('Group Users: ')
        for grpUser in grpMembers['users']:
            user = User(gis, grpUser)
            print('Username: ' + user.username +
                  ' - Full Name: ' + user.fullName +
                  ' - Email: ' + user.email)
            grpUsers.append(user)

        return grpUsers
    except Exception as e:
        print('An Error occurred getting Group members - ' + e.args[0])


def updateUIDs(users):
    global uids, userSearch
    uids = users
    userSearch = users
    print('')
    return userSearch, uids
def updateGrpSearch():
    print()

def readDataFile():
    migrationUIDfile = os.getcwd() + dataFile
    with open(migrationUIDfile, 'r') as uidCSV:
        users = csv.DictReader(uidCSV)
        for user in users:
            #print('Email: ' + user['email'] + ' Group: ' + user['publishgroup'])
            updateDict = {user['email']: user['publishgroup']}
            uids.update(updateDict)
    #return uids


def main():
    #groupSearch = getGroups(grpids, False)  
    #groupSearchWithMembers = getGroups(grpids, True) 
    #updateUIDs(groupSearchWithMembers[1])
    #print('')
    readDataFile()
    #print(uids)
    userSearch = getUsers(uids)    
    #if isinstance(userSearch, list):
    #    updateUser(userSearch, True, True)

if __name__=='__main__':
    main()

