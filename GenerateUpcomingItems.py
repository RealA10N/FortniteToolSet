from FortniteApiCommands import *

api = FortniteUpcomingAPI()
for item in api.get_upcoming_items_json():
    item_class = DrawingUpcomingInfo(item)
    item_class.get_icon_info_image().save(r'F:\Projects\Programming\FortniteToolSet\TestImages\'' + item_class.info_class.get_name() + '.png')
    print(item_class.get_description_string())
