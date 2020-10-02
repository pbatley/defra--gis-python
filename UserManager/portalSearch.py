##from arcgis.gis import GIS
import datetime as dt
from datetime import datetime
from config import loadConfig
from portalConnection import Connection


def portal_search():
    # Connecting to portal
    target = loadConfig.TST['envURL'] + loadConfig.TST['suffixPub']


    connection = Connection('TST', loadConfig.TST['portalOwner'], loadConfig.TST['portalPWD'], target)
    GIS = connection.set_connection()
    #password = input("Password: ")
    gis = GIS#("https://environment-test.data.gov.uk/portal/home", username="portaladmin", password=password)

    # Input dates to search between
    start = input("Please enter a start date in the format dd.mm.yyyy: ")
    end = input("Please enter an end date in the format dd.mm.yyyy: ")
    print("Searching portal for items created between " + start + " and " + end)
    dt_obj_st = datetime.strptime(start + ' 00:00:00,00', '%d.%m.%Y %H:%M:%S,%f')
    start_timestamp = dt_obj_st.timestamp() * 1000
    dt_obj_en = datetime.strptime(end + ' 23:59:59,99', '%d.%m.%Y %H:%M:%S,%f')
    end_timestamp = dt_obj_en.timestamp() * 1000

    # Searching portal for all items created between the start and end date
    # Max items must be greater than the total number of items in portal
    content_published = [item
                         for item in gis.content.search(query="",
                                                        max_items=5000)
                         if item.created > start_timestamp and item.created < end_timestamp]

    title = "Item Title"
    item_type = "Item Type"
    created = "Created"
    id = "Id"

    # Prints items created during the search period
    if len(content_published) > 0:
        print(f"{title:60}{item_type:25}{created:40}{id:20}")
        for item in content_published:
            print(f"{item.title:<60}{item.type:25}{readable_date(item.created):40}{item.id:20}")
    else:
        print("No items found between " + start + " and " + end)


def readable_date(portal_stamp):
    return dt.datetime.fromtimestamp(portal_stamp / 1000).strftime('%B %d %Y at %I:%M.%S %p')


if __name__ == "__main__":
    portal_search()
