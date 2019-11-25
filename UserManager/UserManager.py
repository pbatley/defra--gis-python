from arcgis.gis import GIS, User, UserManager, GroupManager, Group, ContentManager
from config import loadConfig
import json, urllib, urllib.parse, csv, os, sys, datetime
time = datetime


        
envURL="https://environment.data.gov.uk/portal"
portalOwner = "portaladmin"
portalPWD = "ArcG!$3nt3rpr!$3Adm!n"
userSearch = None
groupSearch = None
groupSearchWithMembers = None
dataFile = '\\data\\test-dlsm.csv'
grpids = 'Service Owner'
qryItem = 'owner:portaladmin'
uids = {}
#uids = None#'test'
email = 'test.com'

try:
    gis = GIS(envURL, portalOwner, portalPWD, verify_cert=False)
    print("Successfully logged in as: " + gis.properties.user.username)
except Exception as e:     
    print('An Error occurred ' + e.args[0] + ' trying to log in')


def updateUser(userList, userLevel, userGroup, markedForDeletion):
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
                    grpObj = getGroups(None, None, None)
                    addUserToGroup(grpObj)
        except Exception as e:
            print('An error occurred updating user \n' + e.args[0]) 
    try:
        for userID in userList:
            user = User(gis, userID.username)
            if markedForDeletion:
                deleteUser(user)
            if userID.username != portalOwner and not markedForDeletion:                
                runUpdate()
    except Exception as e:
        print('An error occurred retrieving user - ' + e.args[0])


def getUsers(ids):
    try:
        users = gis.users
        userSearch = []

        if isinstance(ids, dict) and len(ids) !=0:
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
            userResults = users.search(query=ids, sort_field='full_name', max_users=1500)        
            userSearch += userResults
            count = 1
            print('Line: / Full name: / User name: / Email: / Level: / Role: / Associate Groups: ')
            for userResult in userResults:                           
                #print(str(count) 
                #      + ' / ' + userResult.fullName
                #      + ' / ' + userResult.username
                #      + ' / ' + userResult.email
                #      + ' / ' + userResult.level
                #      + ' / ' + userResult.role)
                count += 1
                userGrps = ''#'User Groups: \n'
                for grp in userResult.groups:
                    userGrps += grp.title +' | '
                print(str(count) 
                      + ' / ' + userResult.fullName
                      + ' / ' + userResult.username
                      + ' / ' + userResult.email
                      + ' / ' + userResult.level
                      + ' / ' + userResult.role
                      + ' / ' + userGrps)
                #print(userGrps)

        return userSearch
    except Exception as e:
        print('An error occurred: ' + e.args[0] + ' getting user')


def getGroups(grpObj, members, items):
    try:        
        groups = gis.groups
        #if isinstance(grpObj, str):
        #    grpObj = 'title: ' + grpObj + ' AND owner: ' + portalOwner
        #    groupResults = groups.search(query=grpObj, sort_field='title', outside_org=False)
        #else:
        #    grpObj = 'owner: ' + portalOwner
        groupResults = groups.search(query=grpObj, sort_field='title', outside_org=False)
        groupItems = None
        groupMembers = None
        groupResultSet = []
        if not items:
            print('Group Title: ' + ' | Group ID: ' + ' | Group Owner: ' + ' | Group Description: ' + ' | Group Tags: ')
        for groupResult in groupResults:
            if groupResult.owner == portalOwner:
                if not isinstance(groupResult.description, str):
                    groupResult.description = 'None'
                #print('Group Title: ' + ' | Group ID: ' + ' | Group Owner: ' + ' | Group Description: ' + ' | Group Tags: ')
                groupTags = ''
                for groupTag in groupResult.tags:
                    groupTags += groupTag + ' '
                if not items:
                    print(groupResult.title + ' | ' + groupResult.id + ' | ' + groupResult.owner + ' | ' + groupResult.description + ' | ' + groupTags)                
                if members:
                    groupMembers = getGroupMembers(groupResult)
                    print('\n')
                if items:
                    groupItems = getGroupItems(groupResult)
                groupResultSet.append(groupResult)

        return groupResultSet, groupMembers, groupItems                
    except Exception as e:
        print('An Error occurred getting Groups information - ' + e.args[0])


def UpdateGroup(grpObj, user):
    try:
        if isinstance(grpObj, str):
            groupResults = getGroups(grpObj, None, None)
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

def getGroupItems(grpObj):
    try:
        group = grpObj
        items = group.content()
        print('Group Title: | Group ID: | Group Owner: | Group Description:  | Item title: | Item ID: | Item URL: | Item type: | Item Uploaded: | Item Modified: | Item Owner: ')
        for item in items:
            itemCreatedStmp = item.created /1000
            itemModifiedStmp = item.modified /1000
            createdTimestmp = time.datetime.fromtimestamp(itemCreatedStmp)
            createdTimestmp = createdTimestmp.strftime('%d-%m-%Y %H:%M:%S')
            modifiedTimestmp = time.datetime.fromtimestamp(itemCreatedStmp)
            modifiedTimestmp = modifiedTimestmp.strftime('%d-%m-%Y %H:%M:%S')
            print(group.title + ' | ' + group.id + ' | ' + group.owner + ' | ' + group.description + ' | ' + item.title + ' | ' + item.id + ' | ' + str(item.url) + ' | ' + item.type + ' | ' + createdTimestmp + ' | ' + modifiedTimestmp + ' | ' + item.owner)
        #print(items)
        if len(items) == 0:
            print(group.title + ' | ' + group.id + ' | ' + group.owner + ' | ' + group.description + ' | ' + 'No Resource' + ' | ' + 'No Resource' + ' | ' + 'No URL Resource' + ' | ' + 'No Resource' + ' | '+ 'No Resource' + ' | ' + 'No Resource' + ' | ' + 'No Resource')
        return items
    except Exception as e:
         print('An Error occurred getting Group items - ' + e.args[0])


def getItems(qryItem):
    contentMgmt = gis.content
    itemisedResults = []
    global x
    x=1
    items =[]

    def getItemResults(x):
        itemResults = contentMgmt.advanced_search(qryItem, sort_field="title", sort_order="asc", start=x, max_items=100)
        return itemResults

    items = getItemResults(x)
    print('Item title: | Item ID: | Item Description | Item URL: | Item type: | Item Uploaded: | Item Modified: | Item Owner: ')
    while x < int(items['total']):
        for item in items['results']:
            itemCreatedStmp = item.created /1000
            itemModifiedStmp = item.modified /1000
            createdTimestmp = time.datetime.fromtimestamp(itemCreatedStmp)
            createdTimestmp = createdTimestmp.strftime('%d-%m-%Y %H:%M:%S')
            modifiedTimestmp = time.datetime.fromtimestamp(itemCreatedStmp)
            modifiedTimestmp = modifiedTimestmp.strftime('%d-%m-%Y %H:%M:%S')
            print(item.title + ' | ' + item.id + ' | ' + str(item.description) + ' | ' + str(item.url) + ' | ' +  item.type + ' | ' + createdTimestmp + ' | ' + modifiedTimestmp + ' | ' + item.owner)
            itemisedResults.append(item)
            x += 1

        items = getItemResults(x)

    return itemisedResults


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

def deleteUser(userID):
    #user = User(gis, userID.username)
    if email in userID.email:
        userID.delete(reassign_to=portalOwner)
    print('Deleting user: ' + userID.email + ' AND re-assigning users items to ' + portalOwner)


def compundUserSearch(users):
    count = 1
    print('Line: / Full name: / User name: / Email: / Level: / Role: ')      
    for user in users:
        if email in user.email:
            print(str(count) 
                    + ' / Action: Delete / '
                    + ' / ' + user.fullName
                    + ' / ' + user.username
                    + ' / ' + user.email
                    + ' / ' + user.level
                    + ' / ' + user.role)
            count += 1
            #deleteUser(user)  


def main():
    #groupSearch = getGroups(grpids, False, True)  
    #groupSearchWithMembers = getGroups(grpids, True, False) 
    #updateUIDs(groupSearchWithMembers[1])
    itemSearch = getItems(qryItem)
    #for item in itemSearch:
    #    print(item.title)
    print('')
    #readDataFile()
    #print(uids)
    #userSearch = getUsers(uids)
    #compundUserSearch(userSearch)
    #if isinstance(userSearch, list):
    #    updateUser(userSearch, True, True, False)
        #updateUser(userSearch, False, False, True)


if __name__=='__main__':
    main()

