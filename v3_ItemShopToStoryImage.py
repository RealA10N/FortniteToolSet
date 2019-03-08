from FortniteApiCommands import *
from ConsoleFunctions import *


class ItemsList:

    def __init__(self, items_list):

        self.__items_list = items_list
        self.__featured_items_list = None
        self.__not_featured_items_list = None

        self.__items_class_list = None
        self.__generate_all_info_classes()

        self.__icons_only_drawing_images = None
        self.__featured_only_drawing_images = None
        self.__default_drawing_images = None

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

    def __generate_icons_only_images(self):
        wip_dicts_list = []
        for item_class in self.get_items_classes_list():
            wip_current_dict = {}
            item_drawing = DrawingItems(name=item_class.get_name(),
                         rarity=item_class.get_rarity(),
                         cost=item_class.get_cost(),
                         icon_image=item_class.get_transparent_image())
            wip_current_dict['image'] = item_drawing.generate_info_image(item_drawing.__get_1on1_background_image())
            wip_current_dict['size'] = (1, 1)
            wip_dicts_list.append(wip_current_dict)
        self.__icons_only_drawing_images = wip_dicts_list

    # "icons_only" script. will return only 1on1 images in dict, with the key 'image'
    def get_icons_only_images(self):
        if self.__icons_only_drawing_images is None:
            self.__generate_icons_only_images()
        return self.__icons_only_drawing_images

    def __generate_featured_only_images(self):
        wip_dict_list = []
        for item_class in self.get_featured_items():
            wip_current_dict = {'size': (1, 2)}
            item_drawing = DrawingItems(name=item_class.get_name(),
                                        rarity=item_class.get_rarity(),
                                        cost=item_class.get_cost(),
                                        featured_image=item_class.get_featured_image())
            wip_current_dict['image'] = item_drawing.generate_info_image(item_drawing.__get_1on2_background_image())
            wip_dict_list.append(wip_current_dict)
        self.__featured_only_drawing_images = wip_dict_list

    # will return only 1on2 images in dict, with the key 'image'
    def get_featured_only_images(self):
        if self.__featured_only_drawing_images is None:
            self.__generate_featured_only_images()
        return self.__featured_only_drawing_images

    def __generate_default_images(self):
        wip_dicts_list = []

        for item_class in self.get_items_classes_list():
            wip_current_dict = {}

            if item_class.get_if_image_featured():
                wip_current_dict['size'] = (1, 2)
                item_drawing = DrawingItems(name=item_class.get_name(),
                                            rarity=item_class.get_rarity(),
                                            cost=item_class.get_cost(),
                                            featured_image=item_class.get_featured_image())
                wip_current_dict['image'] = item_drawing.generate_info_image(item_drawing.__get_1on2_background_image())
            else:
                wip_current_dict['size'] = (1, 1)
                item_drawing = DrawingItems(name=item_class.get_name(),
                                            rarity=item_class.get_rarity(),
                                            cost=item_class.get_cost(),
                                            icon_image=item_class.get_transparent_image())
                wip_current_dict['image'] = item_drawing.generate_info_image(item_drawing.__get_1on1_background_image())

            wip_dicts_list.append(wip_current_dict)

        self.__default_drawing_images = wip_dicts_list

    # "default" script. will return list of dictionaries.
    # 'image' key in every dictionary will return the item image, featured if possible.
    # 'size' key in every dictionary will return the size of the image. for example: (1, 1) or (1, 2)
    def get_default_images(self):
        if self.__default_drawing_images is None:
            self.__generate_default_images()
        return self.__default_drawing_images

    def get_images_by_sorting_method(self, sorting_type):
        if sorting_type == 'default':
            return self.get_default_images()
        elif sorting_type == 'icons_only':
            return self.get_icons_only_images()


console = ConsolePrintFunctions()
console.print_one_line_title("Fortnite Item Shop Generator. // Created by @RealA10N", "single heavy square")

fortnite_api = FortniteItemShopAPI()
items_list = fortnite_api.get_item_shop_json()['items']

for item_dict in items_list:
    item_class = DrawingShopItem(item_dict)
    item_class.get_deafult_info_image().show()


'''
fortnite_api = FortniteItemShopAPI()
items_list_class = ItemsList(fortnite_api.get_item_shop_json()['items'])

# algorithm that decides how to sort the items in the final image.
places_in_small_grid = 12
places_in_large_grid = 20
sorting_method = (None, None)
# first index is "default" sorting (with big featured images) or "icons_only" (small only) sorting.
# second index is the grid size, in tuple.
if items_list_class.get_number_of_items() <= places_in_small_grid:
    if items_list_class.get_default_places() <= places_in_small_grid:
        sorting_method = ('default', (3, 4))
    else:
        sorting_method = ('icons_only', (3, 4))
else:
    if items_list_class.get_default_places() <= places_in_large_grid:
        sorting_method = ('default', (4, 5))
    else:
        sorting_method = ('icons_only', (4, 5))

for image in items_list_class.get_default_images():
    print(image['size'])
    image['image'].show()
'''
