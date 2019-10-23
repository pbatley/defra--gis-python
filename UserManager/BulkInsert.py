#!/usr/bin/env python
# Requires Python 2.7+

# Demonstrates how to add users to the ArcGIS Enterprise portal in bulk

# For Http calls
import urllib2, urllib, json
# For system tools
import sys, os
# For reading passwords without echoing
import getpass
# Other utilities
import Queue

# Defines the entry point into the script
def main(argv):

    print "This script adds users in bulk into a portal. \n"

    #Get parameters
    parameters = getParametersFromUser ()

    portalURL = parameters['portalURL']
    provider = parameters['provider']
    userName = parameters['userName']
    password = parameters['password']
    inUserFile = parameters['inUserFile']


    #Get user data from file
    usersData = getUserDataFromFile(inUserFile,provider)

    #Create users
    createUsers (userName,password, portalURL,provider, usersData)

    raw_input('Press ENTER to close the script.')

    return


# This function loads all the user data in the input text file into a Python Queue.
# This usersQueue can be later passed to the createUsers function
def getUserDataFromFile(inUserFile,provider):

    usersQ = Queue.Queue()
    inFileHandle = open(inUserFile, 'r')
    userCount = 0
    print '...Processing input users file at: ' + inUserFile
    entryCount = 1
    roleID = {'admin':'org_admin', 'publisher':'org_publisher', 'user':'org_user', 'viewer':'iAAAAAAAAAAAAAAA'}
    for line in inFileHandle.readlines():
        userParams = line.strip('\n').split('|')
        userParamDict = {}
        if provider=="enterprise":
            keyParams = ['username', 'email', 'fullname', 'role', 'userLicenseTypeId', 'description', 'idpUsername', 'firstname', 'lastname']
            if len(userParams) == len(keyParams):
                for i, param in enumerate(keyParams):
                    userParamDict[param] = userParams[i]
                if userParamDict['role'] in roleID.keys():
                    userParamDict['role'] = roleID[userParamDict['role']]
                else:
                    print('The value for the user role "{}" in users text file is invalid.'.format(userParamDict['role']))
                    print('Accepted values are viewer, user, publisher, or admin.')
                    raise SystemExit('Invalid user role')
                usersQ.put(userParamDict)
                userCount = userCount + 1
            else:
                print('The format for entry "{}" is invalid.\nThe format for enterprise accounts is:'.format(line.strip('\n')))
                print(' <login>|<email address>|<full name>|<role>|<user type id>|<description>|<idp username>|<first name>|<last name>')
                raise SystemExit('Invalid format')
        elif provider=="arcgis":
            keyParams = ['username', 'password', 'email', 'fullname', 'role', 'userLicenseTypeId', 'description', 'firstname', 'lastname']
            if len(userParams) == len(keyParams):
                for i, param in enumerate(keyParams):
                    userParamDict[param] = userParams[i]
                if userParamDict['role'] in roleID.keys():
                    userParamDict['role'] = roleID[userParamDict['role']]
                else:
                    print('The value for the user role "{}" in users text file is invalid.'.format(userParamDict['role']))
                    print('Accepted values are viewer, user, publisher, or admin.')
                    raise SystemExit('Invalid user role')
                usersQ.put (userParamDict)
                userCount = userCount + 1
            else:
                print('The format for entry "{}" is invalid.\nThe format for built-in accounts is:'.format(line.strip('\n')))
                print(' <account>|<password>|<email address>|<full name>|<role>|<description>|<first name>|<last name>|<level>')
                raise SystemExit('Invalid format')
        else:
            raise SystemExit( 'The value for the user type is invalid. ')
        entryCount = entryCount +1
    inFileHandle.close()
    # Create users and report results
    print '...Total members to be added: ' + str(userCount)

    return usersQ


# This function connects to the portal and adds members to it from a collection
def createUsers(username,password, portalUrl, provider,userParamsQ):

    print '...Connecting to ' + portalUrl
    token = generateToken(username,password, portalUrl)
    print '...Adding users '
    usersLeftInQueue = True
    while usersLeftInQueue:
        try:
            userDict = userParamsQ.get(False)
            userDict['f'] = 'json'
            userDict['token'] = token
            userDict['provider'] = provider
            params = urllib.urlencode(userDict)

            request = urllib2.Request(portalUrl + '/portaladmin/security/users/createUser?',params, { 'Referer' : portalUrl })

            # POST the create request
            response = urllib2.urlopen(request).read()
            responseJSON = json.loads(response)

            # Log results
            if responseJSON.has_key('error'):
                errDict = responseJSON['error']
                if int(errDict['code'])==498:
                    message = 'Token Expired. Getting new token... Username: ' + userDict['username'] + ' will be added later'
                    token = generateToken(username,password, portalUrl)
                    userParamsQ.put(userDict)
                else:
                    message =  'Error Code: %s \n Message: %s' % (errDict['code'], errDict['message'])
                print '\n' + message
            else:
                # Success
                if responseJSON.has_key('status'):
                    resultStatus = responseJSON['status']
                    print 'User: %s account created' % (userDict['username'])
        except Queue.Empty:
              usersLeftInQueue = False

# This function gets a token from the portal
def generateToken(username, password, portalUrl):
    parameters = urllib.urlencode({'username' : username,
                                   'password' : password,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 60,
                                   'f' : 'json'})
    try:
        response = urllib.urlopen(portalUrl + '/sharing/rest/generateToken?',
                              parameters).read()
    except Exception as e:
        raise SystemExit( 'Unable to open the url %s/sharing/rest/generateToken' % (portalUrl))
    responseJSON =  json.loads(response.strip(' \t\n\r'))
    # Log results
    if responseJSON.has_key('error'):
        errDict = responseJSON['error']
        if int(errDict['code'])==498:
            message = 'Token Expired. Getting new token... '
            token = generateToken(username,password, portalUrl)
        else:
            message =  'Error Code: %s \n Message: %s' % (errDict['code'],
            errDict['message'])
            raise SystemExit(message)
    token = responseJSON.get('token')
    return token

# This function gets gets parameters from the user in interactive mode
def getParametersFromUser():

    parameters = {}
    # Get Location of users file
    inUserFile = raw_input ("Enter path to users text file: ")
    if not os.path.exists(inUserFile):
        raise SystemExit( 'Input file: %s does not exist' % (inUserFile))
    parameters['inUserFile'] = inUserFile

    # Enteprise logins or built-in accounts?
    userInput = raw_input ("What type of users do you want to add to the portal?  Accepted values are built-in or enterprise: ")
    if userInput.lower()=="built-in":
        parameters['provider'] = 'arcgis'
        print '   Built-in accounts will be added to the portal. \n'
    elif userInput.lower()=="enterprise":
        parameters['provider'] = 'enterprise'
        print '   Enterprise accounts will be added to the portal. \n'
    else:
        raise SystemExit( 'The value entered for the user type %s is invalid.  Accepted values are built-in or enterprise. ' % (userInput))

    # Get Portal URL
    hostname = raw_input("Enter the fully qualified portal hostname (for example myportal.acme.com): ")
    parameters['portalURL'] = 'https://' + hostname + ':7443/arcgis'
    print '   Users will be added to portal at: ' + parameters['portalURL'] + '\n'

    # Get a username and password with portal administrative privileges
    parameters['userName'] = raw_input("Enter a built-in user name with portal administrative privileges: ")

    parameters['password'] = getpass.getpass("Enter password: ")
    print '\n'

    return  parameters

# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
