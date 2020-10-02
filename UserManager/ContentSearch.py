import datetime
from config import loadConfig
from portalConnection import Connection
env='TST'
config = eval("loadConfig.config."+ env)
time = datetime
"""Change for Portal"""
target = config['envURL'] + config['suffixPub'] 
connection = Connection(env, config['portalOwner'], config['portalPWD'], target)
GIS = connection.set_connection()
contentMgmt = GIS.content

class _SearchCriteria(object):
    def __init__(self, query, filter, order, max):
        self.query = query
        self.filter = filter
        self.order = order
        self.maxRecords = max
        return super().__init__()

def getItems(qryParams):
    itemisedResults = []
    global x
    x=1
    items =[]

    def getItemResults(x):
        try:
            itemResults = contentMgmt.advanced_search(qryParams.query, sort_field=qryParams.filter, sort_order=qryParams.order, start=x, max_items=qryParams.maxRecords)
            return itemResults
        except Exception as err:
            print(str(err))

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

def DeleteItem(itemList):
    try:
        #result = contentMgmt.delete_items(itemList)
        #if not result:
        result = itemList.delete(force=True)
        if result:
            print('All items requested have been deleted successfully')
        else:
            print("Oops, somethings's gone wrong deleting the selected records")
    except Exception as err:
        print(str(err))

def bulkDelete(itemList):
    try:
        result = contentMgmt.delete_items(itemList)
        #if not result:
        #result = itemList.delete(force=True)
        if result:
            print('All items requested have been deleted successfully')
        else:
            print("Oops, somethings's gone wrong deleting the selected records")
    except Exception as err:
        print(str(err))


def main():
    """Change for different Searches"""
    search = _SearchCriteria("title:NativeOysterBedPotential", "title", "asc", 100)
    itemsSearch = getItems(search)
    itemIDs = []
    #for item in itemsSearch:
    #    if '20200626' in item.title:
    #        itemForDeletion = contentMgmt.get(item.id)
    #        DeleteItem(itemForDeletion)
    #    itemIDs.append(item.id)
    #bulkDelete(itemsSearch)
   
if __name__ == "__main__":
    main()