from FortniteApiCommands import *
from ConsoleFunctions import *

class ItemsContainer:

    def __init__(self, table_size):
        self.__table_width, self.__table_heigt = table_size
        self.__items_table = self.__create_table(table_size, None)
        self.__current_item_index = 0

    def append_item(self, item):
        current_row, current_column = self.__index_to_table_value(self.__current_item_index)
        self.__items_table[current_row][current_column] = item
        self.__current_item_index =+ 1

    def __index_to_table_value(self, index):
        return (self.__table_width // index, self.__table_heigt % index)

    def __table_value_to_index(self, table_value):
        return (table_value[0] * table_width) + table_value[1]

    def __create_table(self, table_size, value=None):
        # generate one line
        line_list = []
        for item in range(table_size[0]): # for item in line
            line_list.append(value)
        # duplicate line
        final_list = []
        for item in range(table_size[1]):
            final_list.append(line_list)
        return final_list


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
