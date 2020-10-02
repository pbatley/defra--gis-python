import UserReports, urllib, json, datetime

time = datetime

resultsJSON = UserReports.main()
### Change for Requirements for deletion ###
targetCriteria = {
		'username': 'auth0',
		'fullName': '',
		'firstName': '',
		'lastName': 'surname',
		'preferredView': None,
		'description': None,
		'email': '',
		'userType': 'arcgisonly',
		'idpUsername': '',
		'favGroupId': 'd65b98c08904453294a4ff4a6f82352b',
		'lastLogin': -1,
		'mfaEnabled': False,
		'validateUserProfile': True,
		'access': 'public',
		'storageUsage': 0,
		'storageQuota': 10995116277760,
		'orgId': '0123456789ABCDEF',
		'role': 'org_user',
		'level': '2',
		'disabled': False,
		'tags': [],
		'culture': None,
		'region': None,
		'units': 'english',
		'thumbnail': None,
		'created': 1586450605135,
		'modified': 1586450605135,
		'provider': 'enterprise',
		'groups': []
		}
### Change for Requirements for deletion ###
token = UserReports.main._token

def deleteIDPUser(targetUser, token):
        adminDeleteURL = '{}/sharing/rest/community/users/{}/delete'.format(UserReports.portalURL, targetUser['username'].replace('|', '%7C'))
        userDict = {}
        userDict['f'] = 'json'
        userDict['token'] = token
        
        try:
            params = urllib.parse.urlencode(userDict)
            params = params.encode('ascii')
            request = urllib.request.Request( adminDeleteURL, params, { 'Referer' : UserReports.refererURL })
            response = urllib.request.urlopen(request)
            jsonDataDelete = UserReports.assertJsonSuccess(response.read().decode('utf-8'))
            if jsonDataDelete[1]['success']:
                print('DELETE: ' + targetUser['username'] + ' successfully')
        except Exceptiona as e:
            print('An error occurred executing deletion of user: ' + targetUser['username'])
            print(str(e))

def deleteCriteria(user):
        ### Change for deletion Criteria ###
    if  targetCriteria['lastName'] in user['lastName'] and user['lastLogin'] == targetCriteria['lastLogin'] and targetCriteria['username'] in user['username']:
        ### Change for deletion Criteria ###
        deleteIDPUser(user, token)


for result in resultsJSON['users']:
    if result['lastLogin'] != -1:
        loginStmp = result['lastLogin'] /1000
        timestmp = time.datetime.fromtimestamp(loginStmp)
        timestmp = timestmp.strftime('%d-%m-%Y %H:%M:%S')
    else:
        timestmp = 'Not yet'
    print('Full Name: ' + result['fullName'] + ' Username: ' + result['username'] + ' Last Logged in: ' + timestmp)
    deleteCriteria(result)



