import urllib, json, datetime

# For system tools
import sys
time = datetime
# For reading passwords without echoing
import getpass
# Admin/publisher user name and password 
username = "siteadmin" 
password = "S1teadmin"
portalUser = "portaladmin"
portalPWD = "ArcG!$3nt3rpr!$3Adm!n"
# Server name
serverName = "environment-test.data.gov.uk" 
portalURL = "https://{}/portal".format(serverName)
#waContextPath = "arcgis"
#waAdminPath = "/{}/admin/services".format(waContextPath)
#waServicePath = "/{}/rest/services".format(waContextPath)
#serverPort = 6443
# URL change for target system Standard/Image Server
#baseUrl = "https://{}{}".format(serverName, waAdminPath)
#httpConn = httplib.HTTPSConnection(serverName)
#headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
def searchUser(token):
# Create JSON Object
    data = {"username": "auth0|5c9b46102065f509e3b8349e",
               "firstname": "Adam",
               "lastname": "Sullivan",
               "role": "iAAAAAAAAAAAAAAA",
               "level": 1,
               "email": "adam.sullivan@landmark.co.uk",
               "provider": "enterprise"
               }    

    
    
    #adminSearchURL = '{}/sharing/rest/community/users?'.format(portalURL)
    adminSearchURL = '{}/sharing/rest//portals/self/users?'.format(portalURL)
    #adminSearchURL += 'adam'
    userDict = {}
    #userDict['q'] = 'adam'
    userDict['start'] = 1
    userDict['num'] = 100
    userDict['sortField'] = 'fullname'
    userDict['sortOrder'] = 'asc'
    userDict['username'] = ''
    userDict['fullname'] = 'adam'
    userDict['lastname'] = ''
    userDict['firstname'] = ''    
    userDict['excludeSystemUsers'] = 'true'
    userDict['f'] = 'json'
    userDict['token'] = token
    #https://environment-test.data.gov.uk/portal/sharing/rest/portals/self/users?start=1&num=10&sortField=fullname&sortOrder=asc&username=adam&fullname=adam&lastname=adam&firstname=adam&excludeSystemUsers=true

    refererURL = portalURL + '/home/organization.html'
    try:
        params = urllib.parse.urlencode(userDict)
        params = params.encode('ascii')
        request = urllib.request.Request( adminSearchURL, params, { 'Referer' : refererURL })
        
    # Read service edit response
        response = urllib.request.urlopen(request)
        #resultsJSON = json.loads(response)
        #for result in resultsJSON['results']:
        #    print(result['username'] + ' ' + result['fullName'])
    
        jsonData = assertJsonSuccess(response.read().decode('utf-8'))
    # Check that data returned is not an error object
        if not jsonData[0]:
            print("Error returned while searching" + str(editData))        
        else:
            print("Search successful.\nReturning results below now....")
            resultsJSON = jsonData[1]
            for result in resultsJSON['users']:
                if result['lastLogin'] != -1:
                    loginStmp = result['lastLogin'] /1000
                    #epoc = float(loginStmp)
                    #timestmp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoc))
                    timestmp = time.datetime.fromtimestamp(loginStmp)
                    timestmp = timestmp.strftime('%d-%m-%Y %H:%M:%S')
                else:
                    timestmp = 'Not yet'
                print('Full Name: ' + result['fullName'] + ' Username: ' + result['username'] + ' Last Logged in: ' + timestmp)
        return
    except Exception:
        print("Unknown error")

def getToken(portalUser, portalPWD, portalUrl):
    '''Retrieves a token to be used with API requests.'''
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
    token = getToken(portalUser, portalPWD, portalURL)
    searchUser(token)

if __name__ == '__main__':
    main()

