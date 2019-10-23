import urllib, urllib3, json, datetime
# For system tools
import sys

# For reading passwords without echoing
import getpass
# Admin/publisher user name and password 
portalUser = 'portaladmin'
portalPWD = 'ArcG!$3nt3rpr!$3Adm!n'
# Server name
serverName = 'environment-test.data.gov.uk'
portalContextPath = 'portalstg'
portalURL = 'https://{}/{}'.format(serverName, portalContextPath)
waContextPath = 'arcgis'
waAdminPath = '/{}/admin/services'.format(waContextPath)
waServicePath = '/{}/rest/services'.format(waContextPath)
serverPort = 6443
# URL change for target system Standard/Image Server
baseUrl = 'https://{}{}'.format(serverName, waAdminPath)


def addUser(token, data):
# Create JSON Object
    data = {'username': 'auth0|5c9b46102065f509e3b8349e',
            'firstname': 'Adam',
            'lastname': 'Sullivan',
            'role': 'iAAAAAAAAAAAAAAA',
            'level': 1,
            'email': 'adam.sullivan@landmark.co.uk',
            'provider': 'enterprise',
            'idpUsername':  'auth0|5c9b46102065f509e3b8349e'
            }       

    adminCreateURL = '{}/portaladmin/security/users/createUser?'.format(portalURL)
    userDict = data
    userDict['f'] = 'json'
    userDict['token'] = token

    try:
        params = urllib.parse.urlencode(userDict)
        params = params.encode('ascii')
        #http = urllib3.PoolManager()
        
        #response = http.request('POST', adminCreateURL, fields=userDict, headers={ 'Referer' : portalURL }) 
        request = urllib.request.Request(adminCreateURL, data=params, headers={ "Referer" : portalURL })
        #with urllib.request.urlopen(request) as response:
        response = urllib.request.urlopen(request)

    # Read service edit response
        #response = urllib2.urlopen(request).read()    
            
    # Check that data returned is not an error object
        #if not assertJsonSuccess(response):
        if not assertJsonSuccess(response.read().decode('utf-8')):
            print('Error returned while adding user: ' + userDict['username'])        
        else:
            print('User: ' + userDict['email'] + ' added successfully.')

        return
    except Exception as e:
        print("Unknown error " + e.args[0])

def getToken(portalUser, portalPWD, portalUrl):
    '''Retrieves a token to be used with API requests.'''
    
    parameters = {'username' : portalUser,
                'password' : portalPWD,
                'client' : 'referer',
                'referer': portalUrl,
                'expiration': 240,
                'f' : 'json'}

    try:
        http = urllib3.PoolManager()
        response = http.request('POST',
                                portalUrl + '/sharing/rest/generateToken?',
                                fields=parameters)
    
        jsonResponse = json.loads(response.data.decode('utf-8'))
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
    if 'error' in obj :
        print('Error: JSON object returns an error. ' + str(obj))
        return False
    else:
        return True
def createAccount():
    token = getToken(portalUser, portalPWD, portalURL)
    addUser(token, None)

def main():
    createAccount()

if __name__ == '__main__':
    main()
