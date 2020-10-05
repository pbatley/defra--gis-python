from arcgis.gis import GIS

class Connection(object):
    """Creation of Portal Connection Class"""
    def __init__(self, env, user, passwd, portalUrl):
        self.environment = env
        self.user = user
        self.passwd = passwd
        self.portalUrl = portalUrl
        return super().__init__()

    def set_connection(self):
        try:
            gis = GIS(self.portalUrl, self.user, self.passwd, verify_cert=False)
            print("Successfully logged in to the " + self.environment + " environment, as user: " + gis.properties.user.username)
            return gis
        except Exception as e:     
            print('An Error occurred ' + e.args[0] + ' trying to log in')

