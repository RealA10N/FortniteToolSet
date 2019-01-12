from FortniteApiCommands import *
from ConsoleFunctions import *

class ItemsList:

    def __init__(self, items_list):

        self.__items_list = items_list
        self.__featured_items_list = None
        self.__not_featured_items_list = None

        self.__items_class_list = None
        self.__generate_all_info_classes()

    # generate ShopInfo class for every item
    # save the classes in list
    def __generate_all_info_classes(self):
        wip_items_list = []
        for item_json in self.__items_list:
            wip_item_class = ShopInfo(item_json)
            wip_items_list.append(wip_item_class)
        self.__items_class_list = wip_items_list

    def get_items_list(self):
        return self.__items_list

    def get_items_classes_list(self):
        return self.__items_class_list

    def get_number_of_items(self):
        return len(self.__items_list)

    # generates list with only FEATURED items "ShopInfo" classes
    # generates list with only NOT FEATURED items "ShopInfo" classes
    # saves both lists in 'self' variables
    def __generate_featured_items_list(self):
        wip_featuerd_list = []
        wip_not_featured_list = []

        for item in self.__items_class_list:
            if item.get_if_image_featured():
                wip_featuerd_list.append(item)
            else:
                wip_not_featured_list.append(item)

        self.__featured_items_list = wip_featuerd_list
        self.__not_featured_items_list = wip_not_featured_list

    # returns list with only FEATURED items "ShopInfo" classes
    def get_featured_items(self):
        if self.__featured_items_list is None:
            self.__generate_featured_items_list()
        return self.__featured_items_list

    # returns list with only NOT FEATURED items "ShopInfo" classes
    def get_not_feauterd_items(self):
        if self.__not_featured_items_list is None:
            self.__generate_featured_items_list()
        return self.__not_featured_items_list

    # will return the default number of places that the item shop will take
    # normal item will take 1 place and featured item will take 2
    def get_default_places(self):
        featured_places = len(self.get_featured_items()) * 2
        normal_places = len(self.get_not_feauterd_items())
        return featured_places + normal_places


console = ConsolePrintFunctions()
console.print_one_line_title("Fortnite Item Shop Generator. // Created by @RealA10N", "single heavy square")

fortnite_api = FortniteItemShopAPI()
items_list_class = ItemsList(fortnite_api.get_item_shop_json()['items'])

places_in_small_grid = 12
places_in_large_grid = 20
if items_list_class.get_number_of_items() <= places_in_small_grid:
    if items_list_class.get_default_places() <= places_in_small_grid:
        print("print as default")
    else:
        print("print all small items")
else:
    if items_list_class.get_default_places() <= places_in_large_grid:
        print("print as default in large grid")
    else:
        print('print all small items in large grid, with "might be more items box')


'''
practice script. don't mind for now.
icon_image = Image.open(r'D:\Downloads\icon.png')
feauterd_image = Image.open(r'D:\Downloads\featured.png')
drawing_items = DrawingItems("Arachne", "legendary", 2000, icon_image, feauterd_image)

background_image = drawing_items.get_1on2_image()
drawing_items.generate_info_image(background_image).save("1on2.png")

background_image = drawing_items.get_1on1_image()
drawing_items.generate_info_image(background_image).save("1on1.png")
'''
