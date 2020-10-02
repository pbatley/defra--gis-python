import urllib, urllib2, json, datetime
# For system tools
import sys

# For reading passwords without echoing
import getpass
# Admin/publisher user name and password 
portalUser = 'portaladmin'
portalPWD = 'AGS3nt3rpr!$3Adm!n'
# Server name
serverName = 'environment-uat.data.gov.uk'
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
    data = {"username": "auth0_5eb3e517d8b5460ccfb4bad2",
            "firstname": "Adam",
            "lastname": "Sullivan",
            "role": "wxrayKGylOIxT935",
            "level": 1,
            "email": "adamtestso@aol.com",
            "provider": "enterprise",
            "idpUsername":  "auth0|5eb3e517d8b5460ccfb4bad2"
            }    

    adminCreateURL = '{}/portaladmin/security/users/createUser?'.format(portalURL)
    userDict = data
    userDict['f'] = 'json'
    userDict['token'] = token

    try:
        params = urllib.urlencode(userDict)
        request = urllib2.Request(adminCreateURL, params, { 'Referer' : portalURL }) 

    # Read service edit response
        response = urllib2.urlopen(request).read()    
            
    # Check that data returned is not an error object
        #if not assertJsonSuccess(response):
        if not assertJsonSuccess(response):
            print("Error returned while adding" + str(editData))        
        else:
            print("User added successfully.")

        return
    except Exception as e:
        print("Unknown error")

def getToken(portalUser, portalPWD, portalUrl):
    '''Retrieves a token to be used with API requests.'''
    
    parameters = urllib.urlencode({'username' : portalUser,
                                   'password' : portalPWD,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 240,
                                   'f' : 'json'})


    response = urllib.urlopen(portalUrl + '/sharing/rest/generateToken?',
                              parameters).read()

    try:
        jsonResponse = json.loads(response)
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
        return True
def createAccount():
    token = getToken(portalUser, portalPWD, portalURL)
    addUser(token, None)

def main():
    createAccount()

if __name__ == '__main__':
    main()
