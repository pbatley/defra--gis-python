import urllib.request, json, datetime
### For system tools ###
import sys
time = datetime
### For reading passwords without echoing ###
import getpass
### Admin/publisher user name and password ###
username = "siteadmin" 
password = "S1teadmin"
portalUser = "portaladmin"
portalPWD = "AGS3nt3rpr!$3Adm!n"
### Server name ###
portalSuffix = "portal"
serverName = "environment-test.data.gov.uk" 
portalURL = "https://{}/{}".format(serverName, portalSuffix)
refererURL = portalURL + '/home/organization.html'

def searchUser(token, start):
### Create JSON Object ###
    
    adminSearchURL = '{}/sharing/rest/portals/0123456789ABCDEF/users?'.format(portalURL)
    search = main._search
    userDict = {}
    userDict['start'] = start
    userDict['num'] = 1000
    userDict['sortField'] = 'fullname'
    userDict['sortOrder'] = 'asc'
    userDict['username'] = search
    userDict['fullname'] = search
    userDict['lastname'] = search
    userDict['firstname'] = search    
    userDict['excludeSystemUsers'] = 'true'
    userDict['f'] = 'json'
    userDict['token'] = token

    try:
        params = urllib.parse.urlencode(userDict)
        params = params.encode('ascii')
        request = urllib.request.Request( adminSearchURL, params, { 'Referer' : refererURL })        
    ### Read service edit response ###
        response = urllib.request.urlopen(request)    
        jsonData = assertJsonSuccess(response.read().decode('utf-8'))
    ### Check that data returned is not an error object ###
        if not jsonData[0]:
            print("Error returned while searching" + str(editData))        
        else:
            print("Search successful.\nReturning results below now....")
            resultsJSON = jsonData[1]
            print('Full Name: | Username: | Last Logged in: ')  
            for result in resultsJSON['users']:
                if result['lastLogin'] != -1:
                    loginStmp = result['lastLogin'] /1000
                    timestmp = time.datetime.fromtimestamp(loginStmp)
                    timestmp = timestmp.strftime('%d-%m-%Y %H:%M:%S')
                else:
                    timestmp = 'Not yet'
                print(result['fullName'] + ' | ' + result['username'] + ' | ' + timestmp)        

        return resultsJSON
    except Exception:
        print("Unknown error")

def getToken(portalUser, portalPWD, portalUrl):
    ### Retrieves a token to be used with API requests ###
    parameters = urllib.parse.urlencode({'username' : portalUser,
                                   'password' : portalPWD,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 240,
                                   'f' : 'json'})
    parameters = parameters.encode('ascii')
    
    request = urllib.request.Request(portalUrl + '/sharing/rest/generateToken?', parameters)
    response = urllib.request.urlopen(request)
    try:
        jsonResponse = json.loads(response.read().decode('utf-8'))
        if 'token' in jsonResponse:
            print('Token recieved...')
            return jsonResponse['token']
        elif 'error' in jsonResponse:
            print(jsonResponse['error']['message'])
            for detail in jsonResponse['error']['details']:
                print(detail)
    except ValueError as e:
        print('An unspecified error occurred.')
        print(e)

def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print('Error: JSON object returns an error. ' + str(obj))
        return False
    else:
        return True, obj



def main():
    main._token = getToken(portalUser, portalPWD, portalURL)
    main._search = ''
    cursor = 1
    resultJSON = searchUser(main._token, cursor)
    resultSetJSON = resultJSON
    while resultJSON['nextStart'] < resultJSON['total']:
        if resultJSON['nextStart'] != 101:
            for x in resultJSON['users']:
                resultSetJSON['users'].append(x)
        if resultJSON['nextStart'] == -1:
            break
        resultJSON = searchUser(main._token, resultJSON['nextStart'])
    print('The Search found: ' + str(resultSetJSON['total']) + ' of users')
    return resultSetJSON

if __name__ == '__main__':
    main()

